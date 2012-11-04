#!/usr/bin/env python

# user params ---------------------------
enter_your_data_below_and_remove_this_line  #file: params.py
namecoind = 'namecoind.exe'
namecoinPath = "c:/program files/namecoin"
rpcUser = "user"
rpcPassword = "password"

# stock params ---------------------------
jsonStringIssuer = '{"info":"namecoin stock exchange - test"}'  # can be changed later; for "ncs/baseName" and ncs/baseName_xxx
stockName = "test"  # PREFIX will be added up front; must be all lower case

# system params ---------------------------
defaultJsonString = ""
CHARS = len(str(PIECES - 1))
PREFIX = "ncs/"
CONNECTOR = "-"  # must be      one char long
PLACEHOLDER = "x"  # for issuer name2
BLOCKWAITTIME = 12 + 2
TXFEE = 0.001  # only for calculations

PIECES = 1000  # maximum recommended value: 1000 - keep the blockchain clean. 
                      # Values above 1000 might run danger to be squatted by other people during the name_firstupdate loop.
                      # High values might make people angry. If more than 50% become angry they could theoretically remove your entries.                    
