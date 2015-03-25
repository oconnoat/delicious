#!/usr/bin/python

import requests
import time
import re
import logging

from collections import defaultdict
from collections import Counter

import csv
import json

logging.basicConfig(filename='delicious.log',level=logging.DEBUG)

alltags = Counter()
urlwithtags = {}

with open('delicious.html') as f:
    rh = re.compile(r'HREF="(.*?)"')
    rx = re.compile(r'TAGS="(.*)"')


    for line in f:
        try:
            urlregex = rh.search(line)
            url = urlregex.group(1)
            r = requests.get(url, timeout=1)

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

with open('tags.csv','w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow( ['tag','count'])
    for tag, count in alltags.iteritems():
        csvwriter.writerow([tag, count])

with open('urls.json','w') as f:
    json.dump(urlwithtags, f)
