#!/usr/bin/env python3

import subprocess
import requests
import re
import argparse

class Install():
    def __init__(self, parameter):
        self.parameter = parameter
        self.COMPOSE_URL = 'https://docs.docker.com/release-notes/docker-compose/'

    def run(self):
        if self.parameter == 'compose':
            response = requests.get(self.COMPOSE_URL)
            regex=re.compile(r'nomunge\".(.*)</a.')
            
            for lines in response:
                if b"<li><a href=" in lines:
                    if b"class=\"nomunge\"" in lines:
                        version = lines.decode()
                        break
            
            m = str(regex.findall(version))

            result = m[2:-2]
            print(result)

class Import_Packages():
    def __init__(self, packages):
        self.packages = packages

    def Download(self):        
        for package in self.packages:
            try:
                __import__(package)
            except ImportError:
                subprocess.run(['/bin/bash', '-O', 'extglob', '-c', 'pip3', 'install', package])        
        
if __name__ == '__main__':
    packages = Import_Packages(packages = ['requests', 're', 'argparse'])
    packages.Download()

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameter',
        help='Chosen function, centos-gpg/docker-compose', required=False)
    args = parser.parse_args()

    install = Install(parameter=args.parameter)
    install.run()
