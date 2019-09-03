#!/usr/bin/env python3

import requests
import urllib3.request
from itertools import islice

def send_data_to_script(head):
    new = ""

    for x in head:
        new += x

    return new

response = requests.get('https://docs.docker.com/release-notes/docker-compose/')

for lines in response:
    if b"<li><a href=" in lines:
        if b"class=\"nomunge\"" in lines:
            head = list(islice(lines.decode(), 27, 33))
            break

print(send_data_to_script(head))