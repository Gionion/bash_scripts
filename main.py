import requests
import urllib3.request
import re
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--parameter',
    help='Chosen function, centos-gpg/docker-compose', required=False)
args = parser.parse_args()

if args.parameter == 'compose':
    def print_compose_version(head):
        string = ""

        for letter in head:
            string += letter

        return string

    response = requests.get('https://docs.docker.com/release-notes/docker-compose/')
    regex = re.compile(r'.*nomunge\"\>(.*)</a.*')

    for lines in response:
        if b"<li><a href=" in lines:
            if b"class=\"nomunge\"" in lines:
                version = lines.decode()
                break

    m = regex.match(version)
    v = m.group(1)

    print(print_compose_version(v))

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
    rpm = "{0}/extras/x86_64/Packages/".format(baseurl)
    osurl= "{0}/os/x86_64".format(baseurl)
    gpgurl= "{0}/RPM-GPG-KEY-CentOS-{1}".format(osurl, v)

    if args.parameter == 'rpm':
        response = requests.get("http://mirror.centos.org/centos/7/extras/x86_64/Packages/?C=M;O=D")
        regex = re.compile(r'.*(container.*rpm).*')

        for lines in response:
                if b"container-selinux" in lines:
                    version = lines.decode()
                    break
        m = regex.match(version)
        v = m.group(1)

        rpmurl = "{0}{1}".format(rpm, v)
        print(centos_version(rpmurl))
    elif args.parameter == 'os':
        print(centos_version(osurl))
    elif args.parameter == 'gpg':
        print(centos_version(gpgurl))
    else:
        sys.exit(0)
    