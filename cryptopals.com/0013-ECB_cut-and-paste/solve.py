#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Write a k=v parsing routine, as if for a structured cookie. The routine should take: 
foo=bar&baz=qux&zap=zazzle

... and produce: 
{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}

(you know, the object; I don't care if you convert it to JSON). 

Now write a function that encodes a user profile in that format, given an email address. You should have something like: 
profile_for("foo@bar.com")

 ... and it should produce: 
{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}

 ... encoded as: 
email=foo@bar.com&uid=10&role=user

Your "profile_for" function should not allow encoding metacharacters (& and =). Eat them, quote them, whatever you want to do, but don't let people set their email address to "foo@bar.com&role=admin". 

Now, two more easy functions. Generate a random AES key, then: 
Encrypt the encoded user profile under the key; "provide" that to the "attacker".
Decrypt the encoded user profile and parse it.

Using only the user input to profile_for() (as an oracle to generate "valid" ciphertexts) and the ciphertexts themselves, make a role=admin profile.
 

Solution
========

In: foo123@baradminPPPPPPPPPPP.cz
P = padding

Enc:|    block 0    |   block 1     |  block 2      |               |
    email=foo123@baradminPPPPPPPPPPP.cz&uid=11&role=userPPPPPPPPPPPP

Mitm|   block0      |               |   block 2     |  block 1      |
    email=foo123@bar                .cz&uid=11&role=
                                                    adminPPPPPPPPPPP
'''

import sys

sys.path.append("../toolbox")
import tools
import crypto

HEADER=b"email="
TRAILER=b"&uid=11&role=user"


def profile_for(email):
    
    data = email.replace(b'%', b'%25')
    data = data.replace(b'&', b'%26')
    data = data.replace(b'=', b'%3d')

    data = HEADER + data + TRAILER
    
    return data


def attack(data):
    blocks = tools.split(data, 16)
    
    return blocks[0] + blocks[2] + blocks[1]

def adminCheck(data):
    
    pairs = tools.toStr(data).split('&')
    pairs = [x.split('=') for x in pairs]

    return (['role','admin'] in pairs)

    
def main(a=1):
    key = crypto.genKey()
    print("*** Client")
    #message = envelope(b"this is a regular message")
    message = profile_for(b'foo123@bar' + tools.addPadding('admin', 16)+b'.cz')
    print(['encoded', len(message), message])
    cipherMsg = crypto.encryptECB(key, message)
    print(['encrypted', len(cipherMsg), cipherMsg])

    #decMsg=decryptCBC(key, cipherMsg)
    #print(decMsg)

    print("*** Mitm")
    receivedMsg = attack(cipherMsg)
      
    print(['tampered', len(receivedMsg), receivedMsg])

    print("*** Server")
    decMsg=crypto.decryptECB(key, receivedMsg)
    if adminCheck(decMsg):
      print("You are ADMIN")
    else:
      print("You are regular user")
    print(decMsg)


if __name__ =='__main__':
  tools.run(main)
