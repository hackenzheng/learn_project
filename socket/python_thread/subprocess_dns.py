#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import time
import logging as log
import struct
import copy
import socket
import re
import hashlib
import subprocess
#import dns.resolver

import settings as st
from pymongo import MongoClient

CF_DB_CONN = None
SERVER_IP = []


def init_log():
    fname = st.PROCESS_NAME
    cur_day = time.strftime("%Y%m%d", time.localtime(time.time()))
    log_dir = ''.join([st.LOG_PATH, cur_day, '/', st.PROCESS_NAME, '/', 'log', '/'])
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)
    init_logger(log_dir, fname, level=log.INFO)


def ip2long(ip):
    try:
        nip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0])
    except Exception, e:
        print "translate ip to long failed: %s error: %s" % (ip, e)
        return False
    return nip


def init_server_list():
    global SERVER_IP
    for item in env.CLOUD_WAF_IP_GROUP:
        if isinstance(item, basestring):
            nip = ip2long(item)
            if not nip:
                sys.exit(1)
            SERVER_IP.append(nip)
        elif isinstance(item, dict) and 'start_ip' in item and 'end_ip' in item:
            start_ip = ip2long(item['start_ip'])
            end_ip = ip2long(item['end_ip'])
            if not start_ip or not end_ip:
                sys.exit(1)
            ip_group = {
                'start_ip': start_ip,
                'end_ip':   end_ip
            }
            SERVER_IP.append(ip_group)
    return True


def connect_db():
    """
    连接数据库
    """
    global CF_DB_CONN
    try:
        CF_DB_CONN = MongoClient(env.CLOUD_WAF_DB_CFG["host"], env.CLOUD_WAF_DB_CFG["port"])
        db_auth = CF_DB_CONN[env.CLOUD_WAF_DB_CFG["auth_db"]]
        db_auth.authenticate(env.CLOUD_WAF_DB_CFG["user"], env.CLOUD_WAF_DB_CFG["passwd"])
    except Exception, e:
        log.error('connect db failed, error: ' + str(e))
        sys.exit(1)


def disconnect_db():
    """
    关闭数据库连接
    """
    global CF_DB_CONN
    CF_DB_CONN.close()


def get_db_data(conn, db, table, query):
    """
    执行sql语句
    :param conn: 数据库连接
    :param db: 数据库名
    :param table: 表名
    :param query: 查询语句
    :return: int,array(array) 数据条数，数据
    """
    try:
        coll = (conn[db])[table]
        data = (list(coll.find(query)))
    except Exception, e:
        log.error(str(e).replace("\n", "\\n"))
        return -1, {}

    return data


def update_one(conn, db, table, update_data, match, **kwargs):
    """
    更新数据库数据
    :param conn: 数据库连接
    :param db: 数据库名
    :param table: 表名
    :param update_data: 更新数据
    :param match: 匹配数据
    :return: BOOL 成功时返回True
    """
    try:
        coll = (conn[db])[table]
        coll.update_one(match, update_data, **kwargs)
    except Exception, e:
        log.error(str(e).replace("\n", "\\n"))
        return False
    return True


def get_websites_data():
    """
    获取已配置的ns数据
    """
    query = {
        "is_deleted":   0,
        "status":       st.WEBSITE_STATUS_PROTECT,
        'is_offline': {'$ne':1},  # 下线的不做判断
        '$and':[   # 暂时回源的不更新
            {
                'fc_bypass_status': {'$ne': 1},
            },
            {
                '$or':[
                    {'dns_bypass_status': {'$exists': False}},
                    {'dns_bypass_status': 0}
                ]
            },
            {
                '$or': [
                    {'dnspod_bypass_status': {'$exists': False}},
                    {'dnspod_bypass_status': 0}
                ]
            }
        ],
        # "end_time":      {"$gte": int(time.time())},
    }
    #return get_db_data(CF_DB_CONN, 'product_data_zhg', 'FCWebsite_v3_update_test', query)
    return get_db_data(CF_DB_CONN, env.CLOUD_WAF_DB_NAME, st.TABLE_FC_WEBSITE, query)



def get_ip(domain):
    """
    通过ping方法获取ip
    :param domain: 域名
    :return: string ping得出的ip
    """
    str_ip = ''
    pingcmd = u'ping -c 1 -i 0.5 -t 3 %s' % domain
    try:
        p_ret = subprocess.Popen(
            pingcmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        (stdoutput, erroutput) = p_ret.communicate()
        stdoutput = stdoutput.strip()
        if not stdoutput:
            return None
    except Exception, e:
        log.error("ping domain failed: " + str(e))
        return False
    regex = re.compile(r'\(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\)')
    ping_ip = regex.findall(stdoutput)
    if ping_ip != []:
        str_ip = (ping_ip[0])[1:-1]
        return str_ip
    else:
        return None


def get_join_status(domain):
    ip = get_ip(domain)
    if not ip:
        log.warn("get domain %s ip failed" % (domain,))
        return st.JOIN_STATUS_NOT_IN
    nip = ip2long(ip)
    if not nip:
        log.error("translate ip(%s) to long failed" % (ip,))
        return st.JOIN_STATUS_NOT_IN
    for item in SERVER_IP:
        if (isinstance(item, (int, long)) and item == nip) or \
                (isinstance(item, dict) and item['start_ip'] <= nip and nip <= item['end_ip']):
            return st.JOIN_STATUS_IN
    return st.JOIN_STATUS_NOT_IN


def get_pure_domain(domain):
    start_match = '://'
    domain_start = domain.find(start_match)
    if domain_start > 0:
        domain = domain[(domain_start + len(start_match)):]
    domain_end = domain.find('/')
    port_pos = domain.find(':')
    if port_pos > 0:
        domain_end = min(domain_end, port_pos) if domain_end > 0 else port_pos
    if domain_end > 0:
        domain = domain[:domain_end]
    return domain

def get_event_key(in_time):
    today = time.strftime('%Y%m%d', time.localtime(in_time))
    key_data = '|'.join((today, str(st.EVENT_TYPE_BUSINESS_JOIN)))
    lib_hash = hashlib.md5()
    lib_hash.update(bytes(key_data))
    return lib_hash.hexdigest()


def insert_alert_event(user, domain, in_time):
    key = get_event_key(in_time)
    match = {
        'key':    key
    }
    update_data = {
        '$push': {
            'review_desc.domain':   domain
        },
        '$set': {
            'record_time':          in_time,
            'handle_time':          in_time
        },
        '$setOnInsert': {
            'domain':              domain,
            'url':                 None,
            'title':               '新业务防护',
            'rank':                3,
            'ref_clouduser':       user,
            'type':                st.EVENT_TYPE_BUSINESS_JOIN,
            'status':              st.AE_STATUS_PASSED,
            'handle_result':       None,
            'insert_time':         in_time,
            'wechat':              None,
            'email':               None,
            'report':              None,
            'metadata':            None,
            'review_time':         None,
            'wechat_status':       st.WECHAT_STATUS_NOT_PUSH,
            'wechat_push_time':    None,
            'email_status':        st.EMAIL_STATUS_NOT_PUSH,
            'email_push_time':     None,
            'read_cloud_user':     [],
            'read_wechat_user':    [],
            'event_status':        st.EVENT_STATUS_FINAL_STATE
        }
    }
    return update_one(CF_DB_CONN, env.CLOUD_WAF_DB_NAME, st.TABLE_ALERT_EVENT, update_data, match, upsert=True)


def dig_domain():
    data = get_websites_data()
    join_status = {}
    for row in data:
        if 'domain' not in row or not row['domain'].strip():
            continue
        domain = copy.deepcopy(row['domain'])
        if domain not in join_status:
            join_status[domain] = get_join_status(domain)
        new_status = join_status[domain]
        #print domain, new_status
        # if new_status is False:
        #     continue

        update_data = {
            '$set': {}
        }
        if new_status != row['is_in']:
            update_data['$set']['is_in'] = new_status
            now = int(time.time())
            #print domain, new_status, now
            # 只在第一次检测到接入时更新
            if 'in_time' not in row and new_status == st.JOIN_STATUS_IN:
                row['in_time'] = now
                update_data['$set']['in_time'] = now
                ret = insert_alert_event(row['ref_clouduser'], domain, now)
                if not ret:
                    log.error('insert %s  %d alert event failed...', domain, now)
                    continue
            update_data['$set']['update_time'] = now

            #添加接入方式
            if new_status == st.JOIN_STATUS_IN:
                dns_type = get_dns_type(domain)
                update_data['$set']['dns_type'] = dns_type
            else:
                update_data['$set']['dns_type'] = 0
        elif new_status == st.JOIN_STATUS_IN and new_status == row['is_in'] and 'in_time' not in row:  # 这里为了兼容老数据,给老数据更新一个字段
            update_data['$set']['in_time'] = row['update_time']
            #print domain, new_status, row['update_time']
        elif new_status == st.JOIN_STATUS_IN :   #更新老数据及之前判断失败的域名的接入方式
            dns_type = get_dns_type(domain)
            if row['dns_type'] != dns_type:
                update_data['$set']['dns_type'] = dns_type


        if update_data['$set']:
            match = {"_id": row['_id']}
            if not update_one(CF_DB_CONN, env.CLOUD_WAF_DB_NAME, st.TABLE_FC_WEBSITE, update_data, match, upsert=False):
                log.error("update row %s failed" % (row, ))

def get_dns_type(domain):
    """
    通过dig方法解析接入方式, 默认5s超时, 只有对已经接入的域名判断接入方式是有效的，不然A记录接入是错误的
    :param domain: 域名
    :return: interger:0:未知(判断出错或失败) 1:NS, 2:CNAME, 3:A记录
    """
    digcmd = u'dig %s +trace' % domain
    try:
        p_ret = subprocess.Popen(
            digcmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        (stdoutput, erroutput) = p_ret.communicate()
        stdoutput = stdoutput.strip()
        if not stdoutput:
            return 0
    except Exception, e:
        log.error("dig domain failed: " + str(e))
        return 0

    try:
        dns_regex = re.compile(r'IN\s+NS\s+dns2\.sangfordns\.com')
        cname_regex = re.compile(r'IN\s+CNAME\s+.+sangfordns\.com')
        a_regex_str = u'%s.+\s+.+\s+IN\s+A\s+'% domain    #空格等空白符号得用\s， 若域名是中文要用u
        a_regex = re.compile(a_regex_str)
        dns_check = dns_regex.findall(stdoutput)
        cname_check = cname_regex.findall(stdoutput)
        a_check = a_regex.findall(stdoutput)
        if dns_check != []:
            return 1
        elif dns_check == [] and cname_check !=[]:
            return 2
        elif dns_check == [] and cname_check ==[] and a_check !=[]:
            return 3
        else:
            return 0
    except Exception, e:
        log.error("analysis dns type failed: " + str(e))
        return 0


def main():
    init_log()
    init_server_list()
    connect_db()
    dig_domain()
    disconnect_db()


if __name__ == '__main__':
    main()
    """
    #get_dns_type('www.hzls.gov.cn')   #单个域名接入方式的测试
    result = []
    with open('domain.txt', 'r') as f:    #多个域名接入方式的测试
        for line in f.readlines():
            if line.startswith('#'):
                continue
            array = line.split()
            if array:
                domain = eval(array[0])
            else:
                continue
            ret = get_dns_type(domain)
            if ret ==1:
                result.append(domain +'   ' + 'NS\n')
            elif ret == 2 :
                result.append(domain + '   ' + 'cname\n')
            else:
                result.append(domain + '   ' + 'A\n')

    fp = open('result_dns_type.txt', 'w')
    fp.writelines(result)
    fp.close()
    """