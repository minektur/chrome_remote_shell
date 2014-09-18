#NAME
chrome_remote_shell - Client for the Google Chrome browser's remote debugging api.


#DESCRIPTION
`a = Shell(host='localhost', port=92222)`

a.tablist has a list of details on open tabs.

`a.connect(tab=index, updateTabs=True)`

will connect `a.soc` to the webservice endpoint for `tablist[index]`'th
tab.  index is an integer, and updateTabs is True or False. Both `tab`
and `update_tabs` are optional, defaulting to 0 and True respectively.

At this point `a.soc.send()` and `a.soc.recv()` will synchronously write
commands and read responses.  The api is semi-asynchronous with
responses for commands, but also spontaneous events will be
send by the browser. For this kind of advance usage, select/poll
on soc is advised.

As a convenience, the shell connection object offers a method that, by
injecting JavaScript into the first tab, commands Chrome to open a URL
in a new tab::

`a.open_url('http://www.aldaily.com/')`

You can also optionally specify a different tab to operate on.



    class Shell(__builtin__.object)
     |  A remote debugging connection to Google Chrome.
     |
     |  > a = Shell(host='localhost', port=92222)
     |
     |  a.tablist has a list of details on open tabs.
     |
     |  > a.connect(tab=index, update_tabs=True)
     |
     |  will connect a.soc to the webservice endpoint for tablist[index]'th
     |  tab.  index is an integer, and update_tabs is True or False. Both tab
     |  and updateTabs are optional, defaulting to 0 and True respectively.
     |
     |  At this point a.soc.send and a.soc.recv will synchronously write
     |  commands and read responses.  The api is semi-asynchronous with
     |  responses for commands, but also spontaeneous events will be
     |  send by the browser. For this kind of advance usage, select/pol
     |  on soc is advised.
     |
     |  Methods defined here:
     |
     |  __init__(self, host='localhost', port=9222)
     |
     |  close(self)
     |      Close websocket connection to remote browser.
     |
     |  connect(self, tab=None, update_tabs=True)
     |      Open a websocket connection to remote browser, determined by
     |      self.host and self.port.  Each tab has it's own websocket
     |      endpoint - you specify which with the tab parameter, defaulting
     |      to 0.  The parameter update_tabs, if True, will force a rescan
     |      of open tabs before connection.
     |
     |  find_tabs(self)
     |      Connect to host:port and request list of tabs
     |      return list of dicts of data about open tabs.
     |
     |  open_url(self, url)
     |      Open a URL in the oldest tab.
     |
