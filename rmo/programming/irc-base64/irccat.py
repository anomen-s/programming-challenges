#! /usr/bin/env python
#
# Example program using irc.client.
#
# This program is free without restrictions; do anything you like with
# it.
#
# Joel Rosdahl <joel@rosdahl.net>

# respond with base64 decoded message

import sys
import argparse
import itertools
import re
import base64

import irc.client
import irc.logging

target = None
"The nick or channel to which to send messages"

STATE = [0, None, False]

def on_connect(connection, event):
    print 'connect'
    if irc.client.is_channel(target):
        connection.join(target)
        return

def on_join(connection, event):
    print 'join'

def on_disconnect(connection, event):
    raise SystemExit()

def on_all_raw_messages(connection, event):
        print(event.type)
        print event.arguments

def requestTask(connection, event):
    print(event.type)
    print event.arguments
    global STATE
    if not STATE[2]:
        STATE[2] = True
        connection.privmsg(target, "!ep2")
    else:
        print 'already sent'


def solve(connection, event):
    print(event.type)
    print event.arguments

    input = event.arguments[-1:][0]
    input = input.encode('ascii','ignore')
    print ('input = ', input)
    p = re.compile('[A-Za-z0-9+/=]{18,}')
    match = p.search(input)
    if match:
        encoded = match.group()
        decoded = base64.b64decode(encoded)

        connection.privmsg(target, '!ep2 -rep ' + decoded)


def main():
    global target

    server = 'irc.root-me.org'
    port = 6667
    nickname = 'anomen-s'
    target = 'candy'

#    irc.logging.setup(args)

    reactor = irc.client.Reactor()
    try:
        c = reactor.server().connect(server, port, nickname)
    except irc.reactor.ServerConnectionError:
        print(sys.exc_info()[1])
        raise SystemExit(1)

    c.add_global_handler("welcome", on_connect)
    c.add_global_handler("join", on_join)
    c.add_global_handler("disconnect", on_disconnect)
    c.add_global_handler("all_raw_messages", on_all_raw_messages)
    c.add_global_handler("mode", requestTask)
    c.add_global_handler("ping", requestTask)
    c.add_global_handler("umode", requestTask)
    c.add_global_handler("privmsg", solve)

    while 1:
        print 'loop'
        reactor.process_once(1)

if __name__ == '__main__':
    main()
