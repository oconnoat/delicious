#!/usr/bin/python

import requests
import time
import re
import logging

from collections import defaultdict
from collections import Set


logging.basicConfig(filename='example.log',level=logging.DEBUG)

alltags = set() 
urlwithtags = {}

with open('delicious2.html') as f:
    rh = re.compile(r'HREF="(.*?)"')
    rx = re.compile(r'TAGS="(.*)"')
    

    for line in f:
        try:
            urlregex = rh.search(line)
            url = urlregex.group(1)
            r = requests.get(url)
            print r.status_code
            if r.status_code == 200:
                match = rx.search(line)
                taggrp = match.group(1)
                tags = taggrp.split(',')
                alltags.update(tags)
                urlwithtags[url] = tags
                logging.debug('url %s', url)
                logging.debug('tags %s', tags)

        except Exception as e:
            logging.error("Exception: %s", e)

with open('tags.txt','w') as f:
    f.write(str(alltags))

with open('urls.txt','w') as f:
    f.write(str(urlwithtags))
