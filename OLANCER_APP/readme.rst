Installation
****************
Run ombred
============
./ombred --confirm-external-bind

first step
===============
$ sudo apt install postgresql

Check it is installed

$ sudo -i -u postgres

postgres@server$ createuser --interactive --pwprompt

notice : (username : ombre)
notice : (password : ombre123)

postgres@server$ createdb ombre

Do one of the followings
---------------------------
1
^^^^
postgres@server$ psql --username ombre --host 127.0.0.1 --db ombre --password

ombre=> \i /your_path_to_project/source.sql

or 

2
^^^
psql --username ombre --host 127.0.0.1 --db ombre --password -f /your_path_to_project/source.sql

second step
=================
notice : make sure your system has virtualenv or install it

$ sudo apt install python3-virtualenv

notice : The project requires python 3.7 or above

$virtualenv venv

$source /venv/bin/activate

(venv)$pip3 install -r requirement.txt

third step
=================
(venv)$uvicorn app.main:app --reload
