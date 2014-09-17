"""Client for the Google Chrome browser's remote debugging api.

#fixme - new example
>>> import chrome_remote_shell
>>> shell = chrome_remote_shell.open(port=9222)
>>> shell.request('DevToolsService', command='ping')
{u'data': u'ok', u'command': u'ping', u'result': 0}


As a convenience, the shell connection object offers a method that, by
injecting JavaScript into the first tab, commands Chrome to open a URL
in a new tab::

    shell.open_url('http://www.aldaily.com/')
"""
try:
    import json
except ImportError:
    import simplejson as json

import requests
import websocket

class Shell(object):
    """A remote debugging connection to Google Chrome."""

    def __init__(self, host='localhost', port=9222):
        self.host = host
        self.port = port
        self.soc = None
        self.tablist = None
        self.find_tabs()


    def connect(self, tab=None):
        if not self.tablist:
            find_tabs()
        if not tab:
            tab = 0
        wsurl = self.tablist[tab]['webSocketDebuggerUrl']
        self.soc = websocket.create_connection(wsurl)
        return self.soc


    def close(self):
        if self.soc:
            self.soc.close()


    def find_tabs(self):
        """Connect to host:port and request list of tabs
             return list of dicts"""
        # find websocket endpoint
        response = requests.get("http://%s:%s/json" % (self.host, self.port))
        self.tablist  = json.loads(response.text)
        return self.tablist


    def open_url(self, url):
        """Open a URL in the default tab."""
        if not self.soc:
            self.connect(tab=0)
        navcom = json.dumps({"id":0,
                              "method":"Page.navigate",
                              "params":{"url":url}})
        self.soc.send(navcom)
        return self.soc.recv()


if __name__ == '__main__':
    import doctest
    doctest.testmod()


