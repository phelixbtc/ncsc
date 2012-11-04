#!/usr/bin/env python

# toDo
#  add escaping (os dependant)
#  linux support

"""
pynamecoin v0.4
alpha stage wrapper around namecoind 0.3.50
phelix / 2012 / nx.bit
GPL License - http://www.gnu.org/licenses/gpl.html - no guarantees

based on bitcoind python wrapper:
    Wrapper around bitcoind 0.3.
    Written by Daniel Berntsson, db@lysator.liu.se .
    In the public domain. No copyright.
"""

# new in v0.4
# sendtoname instead of name_send (now via the new rpc command)
# name_show

# new in v0.3
# deletetransaction
# listtransactions repariert

# new in v0.2
# params external file
# name_history
# escape


#######

import re
import subprocess as sub
import time
class BitcoinError(Exception):
    pass
import json

from params import *

# namecoin -------------------------
def name_new(name):   # cost: 0.01NC + txfee
    return _cmd('name_new %s' % name)
    
def name_firstupdate(name, shortString, longString="", jsonString=defaultJsonString):  # cost: 0.01NC + txfee
    if jsonString and (jsonString[0] != '"' and jsonString[-1] != '"'):
        jsonString = '"' + jsonString + '"'
    return _cmd_raw('name_firstupdate ' + name + ' ' 
                        + shortString + ' ' + longString + ' ' + jsonString).strip()

def name_update(name, jsonString=defaultJsonString, transferTarget=None):  # cost: 0NC  + txfee
    if jsonString and (jsonString[0] != '"' and jsonString[-1] != '"'):
        jsonString = '"' + jsonString + '"'
    if not transferTarget:
        s ='name_update ' + name + ' ' + jsonString
        return _cmd_raw(s).strip()
    else:
        cmdString = 'name_update ' + name + ' ' + jsonString + ' ' + transferTarget
#        print "Attention: domain " + name + " will be transfered to " + transferTarget
#        print "cmdString:", cmdString
#        print "Proceed? y/n + <enter>"
#        answer = raw_input()
#        if answer == "y":            
        return _cmd_raw(cmdString).strip()
#        else:
#            return "cancelled"
def name_history(name):
    return _cmd("name_history %s" % name)    

def name_list():
    """list own names"""
    return _cmd('name_list')

def sendtoname(name, amount, comment="", comment_to=""):
    return _cmd_raw("sendtoname %s %f %s %s" % (name, amount, comment, comment_to)).strip()

def name_show(name):
    """display current value for name"""
    return _cmd('name_show %s' % name)

def escape(s):
    """escape string (for windows)"""
    return s.replace('"', '\\"')

def quote(s):
    """put string inside quotation marks (for windows)"""
    return '"' + s + '"'
    

# namecoin complex functions ------------------

def name_available(name):
    """checks only if the name has ever been registered - not if it has expired since"""
    r = _cmd("name_scan %s 1" % name)
    if r[0]["name"] == (name):
        return 0
    else:
        return 1
    
def name_expires_in(name):
    """does not work, negative values e.g. 'a'"""
    r = _cmd("name_scan %s 1" % name)
    if r[0]["name"] == (name):
        return r[0]["expires_in"]
    else:
        return None

#~ def name_send(domain, amount, comment="", comment_to=""):
    #~ """experimental simple send nmc to name - may go to old address if name is transfered"""
    #~ global L
    #~ L = _cmd("name_history %s 1" % domain) # raises error if name not found
    #~ address = L[-1]["address"]
    #~ r = sendtoaddress(address, amount, comment, comment_to)
    #~ return r
    

# bitcoin --------------------

def getaddressesbylabel(label):
    return _cmd('getaddressesbylabel "%s"' % label)

def getbalance():
    return _cmd("getbalance")

def getblockcount():
    return _cmd("getblockcount")

def getblocknumber():
    return _cmd("getblocknumber")

def getconnectioncount():
    return _cmd("getconnectioncount")

def getdifficulty():
    return _cmd("getdifficulty")

def getgenerate():
    return _cmd("getgenerate")

def getinfo():
    return _cmd("getinfo")

def getlabel(bitcoinaddress):
    return _cmd_raw("getlabel %s" % bitcoinaddress).strip()

def getnewaddress(label):
    return _cmd_raw('getnewaddress "%s"' % label).strip()

def getreceivedbyaddress(bitcoinaddress, minconf=1):
    return _cmd("getreceivedbyaddress %s %d" % (bitcoinaddress, minconf))

def getreceivedbylabel(label, minconf=1):
    return _cmd('getreceivedbylabel "%s" %d' % (label, minconf))

def listreceivedbyaddress(minconf=1, includeempty=False):
    ie = _bool_to_str(includeempty)
    l = _cmd("listreceivedbyaddress %d %s" % (minconf, ie))
    d = {}
    for item in l:
        d[item["address"]] = item
    return d

def listreceivedbylabel(minconf=1, includeempty=False):
    ie = _bool_to_str(includeempty)
    l = _cmd('listreceivedbylabel "%d" %s' % (minconf, ie))
    d = {}
    for item in l:
        d[item["label"]] = item
    return d

def listtransactions(account='""', count=10, from_=0):
    return _cmd("listtransactions %s %d %d" % (account, count, from_))

def deletetransaction(txid):
    return _cmd("deletetransaction %s" % txid)

def sendtoaddress(bitcoinaddress, amount, comment="", comment_to=""):
    return _cmd_raw("sendtoaddress %s %f %s %s" % (bitcoinaddress, amount, comment, comment_to)).strip()

def setgenerate(generate, genproclimit=-1):
    gen = _bool_to_str(generate)
    _cmd_raw("setgenerate %s %d" % (gen, genproclimit))

def setlabel(bitcoinaddress, label):
    _cmd_raw('setlabel %s "%s"' % (bitcoinaddress, label))

def stop():
    _cmd_raw("stop")

def _cmd(args):
    return _parse(_cmd_raw(args))[0]

def _cmd_raw(args):
    return _cmd_raw_list([args])

def _cmd_raw_list(arglist):
    c = [namecoind,
            '-rpcuser=' + rpcUser, '-rpcpassword=' + rpcPassword]
                         
    c.append(arglist)
    lstr = sub.list2cmdline(c)
    #print lstr
                                       
    p = sub.Popen(lstr, stdout=sub.PIPE, stderr=sub.PIPE, shell=True, cwd=namecoinPath)
    output, errors = p.communicate()
    if errors != "":
        #print "output: ", output
        raise BitcoinError(errors)
    return output


def _bool_to_str(b):
    if b:
        s = "true"
    else:
        s = "false"
    return s

def _parse(string):
    start_char = re.search('([\\[\\]{}"0-9\\.-tf])', string).group(1)
    if start_char == "[":
        return _parse_list(string)
    elif start_char == "{":
        return _parse_dict(string)
    elif start_char == '"':
        return _parse_string(string)
    elif start_char in ".-0123456789":
        return _parse_number(string)
    elif start_char == "t" or start_char == "f":
        return _parse_bool(string)
    else:
        return None, string

def _parse_bool(string):
    match = re.match("[^tf]*(true|false)(.*)", string, re.DOTALL)
    b = match.group(1) == "true"
    rest = match.group(2)
    return b, rest

def _parse_number(string):
    match = re.match("[^0-9\\.-]*([0-9\\.-]*)(.*)", string, re.DOTALL)
    try:
        n = int(match.group(1))
    except ValueError:
        n = float(match.group(1))
    rest = match.group(2)
    return n, rest

def _parse_string(string):
    s = ""
    i = string.find('"') + 1
    done = string[i] == '"'
    while not done:
        if string[i] == "\\":
            i += 1
        s += string[i]
        i += 1
        done = string[i] == '"'
    return s, string[i + 1:]

def _parse_list(string):
    l = []
    rest = string[string.find("[") + 1:]
    item, rest = _parse(rest)
    while item is not None:
        l.append(item)
        item, rest = _parse(rest)
    rest = string[string.find("]") + 1:]
    return l, rest

def _parse_dict(string):
    d = {}
    rest = string[string.find("{") + 1:]
    entry, rest = _parse_entry(rest)
    while entry is not None:
        d[entry[0]] = entry[1]
        entry, rest = _parse_entry(rest)
    rest = rest[rest.find("}") + 1:]
    return d, rest

def _parse_entry(string):
    key, rest = _parse(string)
    if key is None:
        return None, rest
    rest = rest[rest.find(":") + 1:]
    value, rest = _parse(rest)
    return (key, value), rest


if __name__ == '__main__':
    print "standalone!"
    print "getinfo:\n", getinfo()
    print "\ndomain 'nx' name_expires_in: ", name_expires_in("nx")
    #print "\ndomain 'asdfadsfasdfadf' name_available: ", name_available("asdfadsfasdfadf")


    if 0:
        r = sendtoaddress("N3Eq7cV1nxG7zoXyLFN4meVeUuApNmzHub", 0.1)
        print "sendtoaddress result:", r
     
        #~ r = name_send("d/nx", 0.1)
        #~ print "name_send result:", r



