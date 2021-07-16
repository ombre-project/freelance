==============
ombred
==============

--------------
install ombred:
--------------

1-Install Ubuntu 18.0.4 LTS

    ``https://releases.ubuntu.com/18.04.5/``

2-install dependencies

    ``sudo apt update && sudo apt install build-essential cmake pkg-config libboost-all-dev libssl-dev libzmq3-dev libunbound-dev libsodium-dev libunwind8-dev liblzma-dev libreadline6-dev libldns-dev libexpat1-dev doxygen graphviz libpgm-dev``

3-clone rep from git

    ``git clone https://github.com/ombre-project/ombre.git``

4-make and compile source
    ``cd ombre``
    ``make``

5-The resulting executables can be found in ``build/release/bin``

6- Add ``PATH="$PATH:$HOME/ombre/build/release/bin"`` to ``.profile``

7-download ombre-blockchain from torrent

8-run:
    ``./ombre-blockchain-import --input-file blockchain.raw  --guard-against-pwnage 0``
update and sync blockchain

9-is ready to use

for more information check https://github.com/ombre-project/ombre

===============================================
ombred flags:
===============================================

+ --help : show help and flags of ombred
+ --log-level arg : arg 0-4 minimum to maximum logging
+ --log-file arg : full path for the log file
+ --rpc-bind-port arg: arg 19744 for rpc protocol
+ --rpc-bin-bind arg : arg 127.0.0.1 for rpc protocol

============================
ombred commands :
============================

- help : show help and commands
- exit : exit the ombred
- sync_info : show blockchain sync progress and connected peers alog with download/upload state
- print_height : show local blockchain height
- status : show status
- version : show version

for more info check https://monerodocs.org/interacting/monerod-reference/
