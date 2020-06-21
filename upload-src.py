#!/usr/bin/env python
"""
example code for setting integration src_code, environment, secrets via public_api

Copyright (C) 2020 Cogniac Corporation
"""
import cogniac
import os
import sys


if "APP_ID" not in os.environ:
    print "Set APP_ID environment variable"
    sys.exit(1)
    
APP_ID = os.environ['APP_ID']

ENV = []
SECRETS = []

env = [{'name': k, 'value': v} for k, v in ENV]
secrets = [{'name': k, 'value': v} for k, v in SECRETS]


# find our source filename
src_fn = [x for x in sys.argv[1:] if x[-3:] == ".py"]

if len(src_fn) != 1:
    print "Specify '.py' src code filename on command line"
    sys.exit(1)

# read requirements.txt 
try:
    requirements = open('requirements.txt').read().split('\n')
except:
    requirements = None


src_config = {'environment': env,
              'secrets': secrets,
              'requirements': requirements,
              'src_code': open(src_fn[0]).read()}


cc = cogniac.CogniacConnection()

app = cc.get_application(APP_ID)

app.app_type_config = src_config

if not app.active:
    app.active = True

print cc.get_application(APP_ID).app_type_config
