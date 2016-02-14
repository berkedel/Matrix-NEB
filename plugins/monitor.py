import os
import time
import requests
import json
from websocket import create_connection
from neb.plugins import Plugin

class MonitorPlugin(Plugin):
    """Monitors your smart home
    monitor snap : Get a snapshot from your smart home camera
    monitor stream [start|stop]: Get a live stream from your smart home camera
    """
    name = "monitor"

    def cmd_snap(self, event, *args):
        # capture image from the camera module
        t = long(time.time() * 1000)
        rnd = "%s.jpg" % t
        fname = "/tmp/%s" % rnd
        cmd = "raspistill -o %s" % fname
        os.popen(cmd)

        # upload image file to home server
        uri = "%s/upload" % self.config.base_url.replace('client/api', 'media')
        res = requests.request('POST',
                               uri,
                               params={
                                   'access_token': self.config.token,
                                   'filename': rnd
                               },
                               data=open(fname, 'rb'),
                               headers={
                                   'Content-Type': 'image/jpeg'
                               }
                            )
        mxc = res.json()
        content = {
            'body': rnd,
            'msgtype': 'm.image',
            'url': mxc['content_uri']
        }
        self.matrix.send_message_event(event['room_id'], event['type'], content)
        return "Snapshot at %s" % t

    def cmd_stream(self, event, mode):
        if mode == "start":
            room = "r%s" % long(time.time() * 1000)
            cmd = "curl -s 'http://127.0.0.1:8080/xmpp?server=meet.jit.si&port=5222&muc=conference.meet.jit.si&room=%s&room_password=&username=tadhack&password=&bosh_enable=1&bosh_tls=1&bosh_server=meet.jit.si&bosh_port=443&bosh_hostname=meet.jit.si&reconnect=1&action=Start' > /dev/null" % room
            os.popen(cmd)
            return "Open http://meet.jit.si/%s" % room
        elif mode == "stop":
            cmd = "curl -s 'http://127.0.0.1:8080/xmpp?action=Stop' > /dev/null"
            os.popen(cmd)
            return "Streaming was stopped"
        return "Mode is not recognized"

    def on_event(self, event, event_type):
        print(event_type)
        return event_type
