"""Client for the Google Chrome browser's remote debugging shell.

This library makes it easy to communicate with the Google Chrome remote
debugging shell from Python.  To make the shell available, start Chrome
with this option::

    google-chrome --remote-shell-port=9222

Then you can connect from Python through code like this::

>>> import chrome_remote_shell
>>> shell = chrome_remote_shell.open()
>>> shell.command('DevToolsService', command='ping')
{u'data': u'ok', u'command': u'ping', u'result': 0}

The protocol is described in detail at:

  http://code.google.com/p/chromedevtools/wiki/ChromeDevToolsProtocol

"""
import json
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

    def command(self, tool, destination=None, **kw):
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
            result = self.socket.recv(30000) # ugh
            j = result.split('\r\n\r\n', 1)[1]
            return json.loads(j)

def open(host='localhost', port=9222):
    """Open a connection to the Google Chrome remote debugger."""
    return Shell(host, port)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
