#!/usr/bin/env python

"""
nmcautoupdate v0.2
phelix / 2012 / nx.bit
MIT License - no guarantees
"""

randomDelayMax = 10  # make it a little more difficult to recognize the domains are from one wallet

updateAll = False  # update all or only soon expiring
soonDays = 62


import pynamecoin as pnc
import time
import random

info = pnc.getinfo()
for k in info:
    print ("%s: " % k) + str(info[k])
print

print "Getting list of own domains. May take a while."
nameDictList = pnc.name_list()

print "Total number of own domains in wallet: ", len(nameDictList)

earliest = 999999
earliestNd = {}
for nd in nameDictList:
    if nd["expires_in"] < earliest:
        earliest = nd["expires_in"]
        earliestNd = nd
print "next expiry in %d blocks, %.2f days (1 block ~~~10min)" % (earliest, earliest * 10.0 / 60.0 / 24.0)
print "(" + earliestNd["name"] + " and maybe others)"
print

# Names expiring soon
soonBlocks = soonDays * 24.0 * 60.0 / 10.0
soonCount = 0
nameDictListSoon = []
for nd in nameDictList:
    if nd["expires_in"] < soonBlocks:
        soonCount += 1
        nameDictListSoon.append(nd)
print "Number of names expiring within %d days: %d" % (soonDays, soonCount)
if not updateAll:
    nameDictList = nameDictListSoon

updateCost = len(nameDictList) * 0.005
print "Updating will cost at most %.6f namecoins" % updateCost
if info["balance"] < updateCost:
    print "Balance too low to update all domains. Quitting."
    raise Exception("Balance too low.")
print "random delay between updates: %d seconds" % randomDelayMax
print "press enter to proceed; ctrl-c to stop"
try:
    raw_input()
except KeyboardInterrupt:
    raise SystemExit("manual interruption")

print "updating..."

for nd in nameDictList:
    print nd["name"], pnc.escape(nd["value"])
    try:
        r = pnc.name_update(nd["name"], pnc.quote(pnc.escape(nd["value"])))
    except pynamecoin.BitcoinError as e:
        message = e.args[0]
        if "pending operations" in message:
            print "Pending operations on %s - skipping." % nd["name"]
            pass
        raise
    print r
    print
    time.sleep(random.randint(0, randomDelayMax))
print "done. remember it will take 1 block until the update will be reflected."
