#!/usr/bin/env python
"""
example code for setting integration src_code, environment, secrets via public_api

Copyright (C) 2020 Cogniac Corporation
"""
import cogniac
import sys
from time import time
import os

t0 = time()

##
#  Create Build
##


# read requirements.txt
try:
    requirements = open('requirements.txt').read()
except:
    requirements = None
    
src_fn = "integration.py"
name = src_fn.split('.')[0].lower()

src_config = {'name': name,
              'description': 'test code',
              'requirements': requirements,
              'src_code': open(src_fn).read()}


cc = cogniac.CogniacConnection()

print "Building", src_fn

try:
    res = cc._post("/builds", json=src_config)
except cogniac.ClientError as e:
    print e.message
    sys.exit(1)
except cogniac.ServerError as e:
    print e.message
    sys.exit(2)

build = res.json()
image = build['image']
print image

print "\nElapsed Build time: %.1f seconds" % (time() - t0)
print


##
# Create Deployment from build
##

print "Deploy", image

if "APP_ID" not in os.environ:
    print "Set APP_ID environment variable"
    sys.exit(1)

APP_ID = os.environ['APP_ID']

app = cc.get_application(APP_ID)

# get current deployment so we can report when it has changed
old_deploy_status = app.app_type_status
                                       
ENV = [('FOO', 'BAR')]
SECRETS = []       # Note: recommend to set these here from specific environment variables

env = [{'name': k, 'value': v} for k, v in ENV]
secrets = [{'name': k, 'value': v} for k, v in SECRETS]

deploy_config = {'environment': env,
                 'secrets': secrets,
                 'image': image}

app.app_type_config = deploy_config

print '------------------------'
print "Deployment Config:"
from pprint import pprint
app = cc.get_application(APP_ID)
pprint(app.app_type_config)
print


# wait for deploy status to change and complete

while True:
    app = cc.get_application(APP_ID)
    deploy_status = app.app_type_status
    if deploy_status and deploy_status != old_deploy_status:
        if deploy_status.get('status') == "deploy in progress":
            print "."
            continue
        break

print '------------------------'
print "Deployment Status:"
pprint(app.app_type_status)
print

