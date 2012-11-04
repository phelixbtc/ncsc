#!/usr/bin/env python

info = """
Namecoin Stock Control v0.1beta
issuing and handling of multiple names
phelix / 2012 / nx.bit
GPL License - http://www.gnu.org/licenses/gpl.html - no guarantees

"""

import time
import traceback
import sys

try:
    import params
except NameError:
    traceback.print_exc()
    time.sleep(3)
    sys.exit()

import pynamecoin as pnc

class NCS(object):
    def __init__(self, prefix, stockName):
        self.stockName = stockName
        self.prefix = prefix
        self.baseName = prefix + stockName
        self.nameDictDict = None

    def display_info(self):
        self.display_wallet_info()
        print
        self.get_own_names()
        self.count_names()
        print
        self.display_stock_info()
        print

    def display_stock_info(self):
        info = pnc.name_show(self.baseName)        
        print "data in", self.baseName + ":"
        print info["value"]
        print
        
    def get_own_names(self):
        print "Getting list of own domains. May take a while."
        nameDictList = pnc.name_list()
        self.nameDictDict = {}
        for d in nameDictList:
            self.nameDictDict[d["name"]] = d        
        print "Names found in current wallet:", len(nameDictList)
        
    def display_wallet_info(self):
        info = pnc.getinfo()
        for k in ["blocks", "difficulty", "version", "balance"]:
            print ("%s: " % k) + str(info[k])

    def count_names(self):
        if self.nameDictDict == None:
            print "get_own_names first"
            return
        c = 0
        for name in self.nameDictDict:
            if (name[:-params.CHARS - 1] == self.baseName and
                name[-params.CHARS:].isdigit() and
                len(name) == len(self.get_template())
                and name[-params.CHARS - 1] == params.CONNECTOR):
                c += 1
        print "number of", self.get_template(), "found:", c

    def transfer_names_to_address(self, quantity, address):
        if self.nameDictDict == None:
            print "get_own_names first"
            return
        print "About to transfer", quantity, self.get_template(), "to:", address
        print "proceed? (y/n)"
        read = raw_input()
        if read != "y":
            print "transfer stopped by user"
            return
        c = 1
        for i in range(params.PIECES - 1, -1, -1):
            name = self.get_name(i)
            if name in self.nameDictDict:
                r = pnc.name_update(name, transferTarget=address)
                print "transfer(" + str(c) + "/" + str(quantity) + "):", name, "done:\n ", r
                self.nameDictDict.pop(name)
                if c == quantity:
                    break                
                c += 1
        print "transfer: done"

    def get_name(self, number):
        if number < 0 or number >= params.PIECES:
            raise Exception("number too high")
        return self.baseName + params.CONNECTOR + ("%0" + str(params.CHARS) + "d") % number
    
    def get_template(self):
        return self.baseName + params.CONNECTOR + params.CHARS * params.PLACEHOLDER
        
    def pay_single_dividend(self, nmcAmount, number):
        name = self.get_name(number)
        r = pnc.sendtoname(name, nmcAmount)
        return r
        
    def pay_dividends(self, nmcAmount):
        balance = pnc.getbalance()
        if params.PIECES * (nmcAmount + params.TXFEE) > balance:
            print "pay_dividends: not enough coins"
            return
        for i in range(params.PIECES):
            self.pay_single_dividend(nmcAmount, i)
            print "pay_dividends:", name, "done:", r
        print "pay_dividends: all done"
                           
    def update_names(self):
        import nmcautoupdate

    def cast_vote(self, pollName, value):
        pass
    def vote_result(self, pollName):
        pass
    def offer(self, nmcPerStock):
        pass


def print_help():
    print """
available commands:
 print_help()
 display_info() 
 pay_dividends(nmcAmount)
 transfer_names_to_address(quantity, "address")
 update_names()  # will update all names in wallet
 <ctrl-c>  # exit
 """


if __name__ == "__main__":
    print info
    ncs = NCS(params.PREFIX, params.stockName)
    ncs.display_info()

    display_info = ncs.display_info
    pay_dividends = ncs.pay_dividends
    transfer_names_to_address = ncs.transfer_names_to_address
    update_names = ncs.udpate_names

    print_help()
    
    while 1:
        try:
            r = input()
            if r != None:
                print r
        except KeyboardInterrupt:
            print "user break"
            break
        except:
            traceback.print_exc()
            

##{
##    import
##    vote
##    info
##    offer  quantity  price
##    swap
##    message
##}
##
    
#def transfer_names_to_name(baseName, address):
 #   pass

#def offer_names(baseName, amount, price):
 #   pass

# swap tx

#N1URdrwV5xd8NUhFXBQZpbujbPfEMLaBNE
