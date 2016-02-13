import os
import time
import requests
import json
from neb.plugins import Plugin

class MonitorPlugin(Plugin):
    """Monitors your smart home
    monitor snap : Get a snapshot from your smart home camera
    monitor stream : Get a live stream from your smart home camera
    """
    name = "monitor"

    def cmd_snap(self, event, *args):
        # capture image from the camera module
        rnd = "%s.jpg" % long(time.time())
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
        return mxc['content_uri']

    def cmd_stream(self, event, *args):
        return "cmd_stream"
