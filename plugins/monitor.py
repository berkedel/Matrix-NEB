from neb.plugins import Plugin

class MonitorPlugin(Plugin):
    """Monitors your smart home
    monitor snap : Get a snapshot from your smart home camera
    monitor stream : Get a live stream from your smart home camera
    """
    name = "monitor"
    def cmd_snap(self, event, *args):
        return "cmd_snap"

    def cmd_stream(self, event, *args):
        return "cmd_stream"
