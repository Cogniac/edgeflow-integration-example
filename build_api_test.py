#!/usr/bin/env python
"""


Copyright (C) 2020 Cogniac Corporation
"""
import cogniac
import sys
from time import time
import os

cc = cogniac.CogniacConnection()


print cc._get('/builds/version').content

#cc._get("/builds/%s" % build['build_id'])
#cc._delete("/builds/%s" % build['build_id'])

url = "/builds?name=foo-bar&limit=17&reverse=True"
while True:
    res = cc._get(url).json()
    for i in res['data']:
        print "%s %3d  %f"  % (i['name'], i['version'], i['created_at'])
    if 'next' in res['paging']:
        url = res['paging']['next']
        print url
    else:
        break

res = cc._get("/builds?name=foo-bar&limit=1&reverse=True").json()['data'][0]
print res['name'], res['version'], res['image']

print cc._get("/builds/names").json()



