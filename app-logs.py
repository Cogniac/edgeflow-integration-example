#!/usr/bin/env python
"""
Use the Cogniac SDK and the CloudCore embedded k8s management API
to stream the logs for the specified integration app_id

usage:  app-logs.py app_id [edgeflow_id]

Must set COG_USER, COG_PASS, and COG_TENANT environment variables.

XXXX Only shows first pod/container for workloads with more than 1 pod or container

This depends on https://github.com/websocket-client/websocket-client
Note, there are other websocket libs which are the wrong ones.
pip install websocket-client

Copyright (C) 2020 Cogniac Corporation
"""

import cogniac
import requests
import websocket     # pip install websocket-client
import sys
from time import sleep


cc = cogniac.CogniacConnection()
print cc.tenant


def usage():
    print "usage:  app-logs.py app_id [edgeflow_id]"
    sys.exit(1)


try:
    app_id = sys.argv[1]
except:
    usage()


try:
    app = cc.get_application(app_id)
except:
    print "unable to get app %s for tenant %s" % (app_id, cc.tenant)
    usage()

print app


def show_edgeflows(all_ef):
    """ display all edgeflows and exit after usage info """
    print
    print "Found EdgeFlows:\n"
    for ef in all_ef:
        print "%10s   %s" % (ef.gateway_id, ef.name)
    print
    usage()


def app_logs(app):
    """
    Stream app's logs from a specific edgeflow via rancher
    """
    all_ef = app._cc.get_all_edgeflows()

    if len(all_ef) == 1:
        edgeflow = all_ef[0]
    else:
        # find which of multiple edgeflow from which to access logs for the specified app
        if len(sys.argv) != 3:
            show_edgeflows(all_ef)
        edgeflow_id = sys.argv[2]
        print edgeflow_id
        for edgeflow in all_ef:
            if edgeflow.gateway_id == edgeflow_id:
                break
        if edgeflow.gateway_id != edgeflow_id:
            print "Invalid EdgeFlow", edgeflow_id
            show_edgeflows(all_ef)
        assert(edgeflow.gateway_id == edgeflow_id)

    # form canonical edgeflow cluster name based on tenant_id and gateway_id
    CLUSTER_NAME = "ef-%s-%s" % (app._cc.tenant_id, edgeflow.gateway_id)

    # get tenant-specific read-only rancher token
    RANCHER_TOKEN = app._cc.tenant.edgeflow_rancher_user_token

    # extract from rancher api the cluster, project, workload, container and pod objects
    session = requests.session()
    session.headers.update({"Authorization": "Bearer %s" % RANCHER_TOKEN})

    links = session.get(app._cc.tenant.edgeflow_rancher_endpoint).json()['links']
    cluster = session.get(links['clusters'] + "?name=" + CLUSTER_NAME).json()['data'][0]
    project = session.get(cluster['links']['projects'] + "?name=Default").json()['data'][0]
    workload = session.get(project['links']['workloads'] + "?name=app-%s" % app.application_id.lower()).json()['data'][0]
    container = workload['containers'][0]
    pod = session.get(project['links']['pods'] + "?workloadId=" + workload['id']).json()['data'][0]
    
    print "Showing logs for", cluster['name'], workload['name'], pod['name'], container['name']

    # stream logs via secure websocket proxy
    print
    url = 'wss://api.cogniac.io:5001/k8s/clusters/' + cluster['id'] + '/api/v1/namespaces/default/pods/' + pod['name'] + '/log?container=' + container['name'] + '&tailLines=500&follow=true&timestamps=true&previous=false'

    def on_message(ws, message):
        print message,

    def on_error(ws, error):
        print error

    def on_close(ws):
        print("### closed ###")

    while True:
        # this depends on websocket-client
        ws = websocket.WebSocketApp(url,
                                    header={"Authorization": "Bearer %s" % RANCHER_TOKEN},
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)

        gotexcept = ws.run_forever(ping_interval=20, ping_timeout=5)
        if not gotexcept:  # KeyboardInterrupt
            break
        sleep(2)


app_logs(app)

