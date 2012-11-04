NCSC
====

Namecoin Stock Control v0.1beta
Issuing and handling of multiple Namecoin names
phelix / 2012 / https://github.com/phelixbtc/ncsc
GPL License - http://www.gnu.org/licenses/gpl.html - no guarantees

PLEASE NOTE
-----------

These scripts are in beta state and were thrown together quickly. They have only been tested superficially and are based on beta software (Namecoin) that is based on an old branch of some other beta software (Bitcoin). Just don't blame me if something goes wrong.

TRUST NO ONE
------------

Remember the Pirateat40 ponzi desaster. Don't trust people on the internet. They will run away laughing with all your hard earned money.

HOWTO
-----

* Modify params_default.py with your data and save it as params.py
* Run namecoind / namecoind.exe
* Issue names yourself with ncsc_issue.py or have someone else send them to you (second namecoind instance: namecoind getnewaddress).
* Transfer names (stocks, shares, bonds, votes), pay dividends.

TODO
----

* logging
* voting
* offer
* swap txs

KNOWN ISSUES
------------

Stock holders will have to update their names every 36000 blocks (~~eight months) or they will expire. It is possible to tell the address that held the name when it expired.
