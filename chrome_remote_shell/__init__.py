"""Client for the Google Chrome browser's remote debugging shell.

This library makes it easy to communicate with the Google Chrome remote
debugging shell from Python.  To make the shell available, start Chrome
with this option::

    google-chrome --remote-shell-port=9222

Then you can connect from Python through code like this:

>>> import chrome_remote_shell
>>> shell = chrome_remote_shell.open(port=9222)
>>> shell.request('DevToolsService', command='ping')
{u'data': u'ok', u'command': u'ping', u'result': 0}

The protocol is described in detail at:

http://code.google.com/p/chromedevtools/wiki/ChromeDevToolsProtocol

As a convenience, the shell connection object offers a method that, by
injecting JavaScript into the first tab, commands Chrome to open a URL
in a new tab::

    shell.open_url('http://www.aldaily.com/')

CHANGELOG
---------

*2009 Feb 26.* Added a conditional import of `simplejson` so that the
module runs under Python 2.5.

"""
try:
    import json
except ImportError:
    import simplejson as json
import socket

HANDSHAKE = 'ChromeDevToolsHandshake\r\n'
RESPONSELESS_COMMANDS = ['evaluate_javascript']

class Shell(object):
    """A remote debugging connection to Google Chrome."""

    def __init__(self, host='localhost', port=9222):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.send(HANDSHAKE)
        assert self.socket.recv(len(HANDSHAKE)) == HANDSHAKE

    def request(self, tool, destination=None, **kw):
        """Send a command to a tool supported by Google Chrome.

        `tool` - 'DevToolsService' or 'V8Debugger'
        other arguments - Combined to form the JSON request object

        """
        j = json.dumps(kw)
        request = 'Content-Length:%d\r\nTool:%s\r\n' % (len(j), tool)
        if destination:
            request += 'Destination:%s\r\n' % (destination,)
        request += '\r\n%s\r\n' % (j,)
        self.socket.send(request)
        if kw.get('command', '') not in RESPONSELESS_COMMANDS:
            response = self.socket.recv(30000) # ugh
            j = response.split('\r\n\r\n', 1)[1]
            return json.loads(j)

    def open_url(self, url):
        """Open a URL in a new tab."""
        response = self.request('DevToolsService', command='list_tabs')
        tabs = response['data']
        first_tab = tabs[0]
        tab_id = first_tab[0]
        javascript = "window.open(%r, '_blank');" % (url,)
        self.request('V8Debugger', destination=tab_id,
                     command='evaluate_javascript', data=javascript)

# Convenience function

def open(host='localhost', port=9222):
    """Open a connection to the Google Chrome remote debugger."""
    return Shell(host, port)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
