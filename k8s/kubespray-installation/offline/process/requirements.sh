#!/usr/bin/env bash
cd ../requirements
sudo pip2.7 install \
    netaddr/netaddr-0.7.19-py2.py3-none-any.whl \
    pbr/pbr-4.0.4-py2.py3-none-any.whl \
    hashvault/idna-2.7-py2.py3-none-any.whl \
    hashvault/certifi-2018.4.16-py2.py3-none-any.whl \
    hashvault/enum34-1.1.6-py2-none-any.whl \
    hashvault/ipaddress-1.0.22-py2.py3-none-any.whl \
    hashvault/urllib3-1.23-py2.py3-none-any.whl \
    hashvault/chardet-3.0.4-py2.py3-none-any.whl \
    hashvault/requests-2.19.1-py2.py3-none-any.whl \
    hashvault/hvac-0.6.0.tar.gz \
    hashvault/MarkupSafe-1.0.tar.gz \
    hashvault/Jinja2-2.10-py2.py3-none-any.whl \
    hashvault/pycparser-2.18.tar.gz \
    hashvault/cffi-1.11.5-cp27-cp27mu-manylinux1_x86_64.whl \
    hashvault/asn1crypto-0.24.0-py2.py3-none-any.whl \
    hashvault/six-1.11.0-py2.py3-none-any.whl \
    hashvault/pyasn1-0.4.3-py2.py3-none-any.whl \
    hashvault/PyNaCl-1.2.1-cp27-cp27mu-manylinux1_x86_64.whl \
    hashvault/bcrypt-3.1.4-cp27-cp27mu-manylinux1_x86_64.whl \
    hashvault/setuptools-39.2.0-py2.py3-none-any.whl \
    hashvault/cryptography-2.2.2-cp27-cp27mu-manylinux1_x86_64.whl \
    hashvault/paramiko-2.4.1-py2.py3-none-any.whl \
    hashvault/PyYAML-3.12.tar.gz \
    hashvault/ansible-2.6.0.tar.gz \
    hashvault/ansible-modules-hashivault-3.9.5.tar.gz
