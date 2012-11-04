info = """
Namecoin Stock Control v0.1beta
issuing and handling of multiple names
phelix / 2012 / nx.bit
GPL License - http://www.gnu.org/licenses/gpl.html - no guarantees

"""


import params
import os
import cPickle as pickle
import time
import pynamecoin as pnc

import ncsc

dbFilename = "ncsc_issue.pickle"
dbBackupPath = "./dbBackup/"

if not os.path.exists(dbBackupPath):
    os.makedirs(dbBackupPath)
        
def save(data, filename):
    f = open(filename,"w")
    pickle.dump(data,f)
    f.close()

class NcscIssue(object):
    def __init__(self, prefix=params.PREFIX, stockName="mystock", dbFilename=dbFilename,
                 dbBackupPath=dbBackupPath, jsonStringIssuer=""):
        self.dbFilename = dbFilename
        self.dbBackupPath = dbBackupPath
        self.jsonStringIssuer = jsonStringIssuer
        
        baseName = params.PREFIX + stockName
        self.baseName = baseName.lower()

        self.ncs = ncsc.NCS(prefix=prefix, stockName=stockName)
        
        try:
            self.db_load()
        except IOError:
            print "Creating new database:", self.dbFilename
            self.db = {}
            self.db_save()
            
    def db_save(self):
        """also saves a backup on every save"""
        print "saving db:", self.dbFilename
        save(self.db, self.dbFilename)
        s = self.dbBackupPath + time.strftime("%Y-%m-%d_%H'%M'%S_backup")
        print "saving db backup: ", s
        save(self.db, s + ".pickle")

    def db_load(self):
        print "loading db:", self.dbFilename
        f = open(self.dbFilename,"r")
        self.db = pickle.load(f)
        f.close()        

    def db_prep_name(self, name):
        if not name in self.db:
            self.db[name] = {}
    
    def db_name_new(self, name):
        print "db_name_new:", name,
        r = None
        self.db_prep_name(name)
        try:
            r = pnc.name_new(name)
            self.db[name]["name_new"] = r
            print "ok"
            self.db[name]["name_new_time"] = time.time()
            self.db[name]["name_new_height"] = pnc.getblockcount()
        except pnc.BitcoinError:
            print "db_name_new failed"
            raise

    def db_name_firstupdate(self, name, jsonString=""):
        first = True        
        while (((self.db[name]["name_new_height"] + params.BLOCKWAITTIME) > pnc.getblockcount()) and
              ((self.db[name]["name_new_time"] + params.BLOCKWAITTIME * 15 * 60 )> time.time())):  # conservative guess
            if first:
                print "Too early for name_firstupdate - wait at least 12 blocks after name_new (~2 hours)"
                print "Waiting for previous name_new to settle...",
                first = False
            else:
                print ".",
            time.sleep(60)
        jsonString = pnc.escape(jsonString)
        print "name_firstupdate:", name,
        try:
            pnc.name_firstupdate(name, self.db[name]["name_new"][1], self.db[name]["name_new"][0],
                                     jsonString)
            print "done"
        except pnc.BitcoinError, e:
            print "failed"
            raise

    def name_new_all(self):
        self.db_name_new(self.baseName)  # issuer name1   these two should always have the same value
        self.db_name_new(self.baseName + params.CONNECTOR + params.CHARS * params.PLACEHOLDER)  # issuer name2  

        for i in range(params.PIECES):
            self.db_name_new(self.ncs.get_name(i))

    def name_firstupdate_all(self):
        self.db_name_firstupdate(self.baseName, self.jsonStringIssuer)  # issuer name1   these two should always have the same value
        self.db_name_firstupdate(self.baseName + params.CONNECTOR + params.CHARS * params.PLACEHOLDER, self.jsonStringIssuer)  # issuer name2  
        
        for i in range(params.PIECES):
            self.db_name_firstupdate(self.ncs.get_name(i), jsonString="")  # no need to bloat the blockchain with an initial value

    def run(self):
        self.name_new_all()
        self.name_firstupdate_all()

    def run_save(self):
        try:
            self.run()
        except:
            self.db_save()
            raise
        

if __name__ == "__main__":
    print "Namecoin Stock Control v0.1beta"
    info = pnc.getinfo()
    for k in ["blocks", "difficulty", "version", "balance"]:
        print ("%s: " % k) + str(info[k])
    print

    cost = params.PIECES * (0.005 + 0.01) * 2

    if cost <= info["balance"]:
        ncscIssue = NcscIssue(prefix=params.PREFIX, stockName=params.stockName,
                              jsonStringIssuer=params.jsonStringIssuer)
        print
        print "About to register " + str(params.PIECES) + " + 2 namecoin names. Approximate maximum cost %.3fNMC" % cost
        print "This can easily take a couple of hours (at least two)!"
        print "Proceed? <enter> / <ctrl-c>"
        raw_input()
        ncscIssue.run_save()
        print "done"
    else:
        print "Not enough coins. Need at least: %.3fNMC" % cost

