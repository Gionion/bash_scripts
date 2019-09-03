#!/usr/bin/env python3

import requests
import urllib3.request
from itertools import islice

def print_compose_version(head):
    string = ""

    for letter in head:
        string += letter

    return string

response = requests.get('https://docs.docker.com/release-notes/docker-compose/')

for lines in response:
    if b"<li><a href=" in lines:
        if b"class=\"nomunge\"" in lines:
            head = list(islice(lines.decode(), 27, 33))
            break

print(print_compose_version(head))
