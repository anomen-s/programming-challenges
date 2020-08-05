#! /usr/bin/env python
#
# Example program using irc.client.
#
# This program is free without restrictions; do anything you like with
# it.
#
# Joel Rosdahl <joel@rosdahl.net>

# respond with ROT13 decoded message

import sys
import argparse
import itertools
import re
import base64
import zlib
import irc.client
import irc.logging
import math

target = None
"The nick or channel to which to send messages"

STATE = [0, None, False, False]

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
        connection.privmsg(target, "!ep3")
    else:
        print 'already sent'
        exit()


def codec():
    result = map(chr,range(256))
    for i in range(13):
        i_a = ord('a')
        i_A = ord('A')
        i_n = ord('n')
        i_N = ord('N')
        result[i_a + i] = chr(i_a+13+i)
        result[i_n + i] = chr(i_n-13+i)
        result[i_A + i] = chr(i_A+13+i)
        result[i_N + i] = chr(i_N-13+i)
    return result

def decode(str):
    tab = codec()
    result = ''
    for c in str:
        result = result + tab[ord(c)]
    return result

def solve(connection, event):
    print(event.type)
    print event.arguments
    global STATE
    if not STATE[3]:
        STATE[3] = True
    else:
	print 'already solved'
	exit()

    input = event.arguments[-1:][0]
    input = input.encode('ascii','ignore')
    print ('input = ', input)
    resstr = decode(input)
    print resstr
    connection.privmsg(target, '!ep3 -rep ' + str(resstr))


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
