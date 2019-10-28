import requests
import urllib3.request
import re
from itertools import islice
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--parameter',
    help='Chosen function, centos-gpg/docker-compose', required=False)
args = parser.parse_args()

if args.parameter == 'compose':
    def print_compose_version():
        response = requests.get('https://docs.docker.com/release-notes/docker-compose/')
        regex=re.compile(r'nomunge\".(.*)</a.')
        
        for lines in response:
            if b"<li><a href=" in lines:
                if b"class=\"nomunge\"" in lines:
                    version = lines.decode()
                    break
        
        m = str(regex.findall(version))

        result = m[2:-2]
        print(result)

    print_compose_version()

else:
    def centos_version(head):
        string = ""

        for letter in head:
            string += letter
        
        return string

    response = requests.get('http://mirror.centos.org/')
    regex = re.compile(r'\".*centos-(.).*')  

    for lines in response:
        if b"centos-" in lines:
            version = lines.decode()
    
    m = regex.match(version)
    v = m.group(1)

    baseurl = "http://mirror.centos.org/centos-{0}/{1}".format(v, v)
    rpmurl = "{0}/extras/x86_64/Packages/container-selinux-2.68-1.el7.noarch.rpm".format(baseurl)
    osurl= "{0}/os/x86_64".format(baseurl)
    gpgurl= "{0}/RPM-GPG-KEY-CentOS-{1}".format(osurl, v)

    if args.parameter == 'rpm':
        print(centos_version(rpmurl))
    elif args.parameter == 'os':
        print(centos_version(osurl))
    elif args.parameter == 'gpg':
        print(centos_version(gpgurl))
    else:
        sys.exit(0)
    
