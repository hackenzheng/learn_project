#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2018/12/5
# @Author  : Sally
import dns.resolver
from urllib.parse import urlparse
from tornado.log import gen_log


def get_ips_by_domain(domain):
    # 通过域名查找ip列表
    ips = []
    all = dns.resolver.query(domain)
    for ip in all:
        ips.append(ip.address)
    return ips


def extract_domain_from_url(url):
    parsed_uri = urlparse(url)
    return parsed_uri.hostname


def resolve_urls_from_domain(url):
    # 通过url获取域名下面的所有的ip
    try:
        parsed_uri = urlparse(url)
        domain = parsed_uri.hostname
        port = parsed_uri.port
        ips = get_ips_by_domain(domain)
        urls = []

        for ip in ips:
            urls.append("http://%s:%s%s"%(ip, port, parsed_uri.path))
        return urls
    except Exception as e:
        gen_log.exception(e)
        return [url]


if __name__ == "__main__":
    url = "http://www.baidu.com:8080/reset"
    print(resolve_urls_from_domain(url))