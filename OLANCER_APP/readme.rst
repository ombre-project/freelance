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


FILES
****************

app -> api -> deps.py
-----------------

this py file keep methods that use for dependencies of endpoints files

app -> api -> api_v1 -> api.py
-----------------

this py file keep pre url path of routers

app -> api -> api_v1 -> endpoints -> Repositories -> repositories.py
-----------------

this py file keep contexts of templates for the methods that response the requests of the client

app -> api -> api_v1 -> endpoints -> landing.py
-----------------

this py file handle the request of pre path /api/v1/home

app -> api -> api_v1 -> endpoints -> login.py
-----------------

this py file handle the request of pre path /api/v1/login

app -> api -> api_v1 -> endpoints -> users.py
-----------------

this py file handle the request of pre path /api/v1/users

app -> core -> config.py
-----------------

this py file keep basic setting of app for running

app -> core -> read_json.py
-----------------

this py file keep method that read json values of values.json file in the project for the static value we need in all over this app

app -> core -> security.py
-----------------

this py file keep methods that handle the access token of any user

app -> crud -> base.py
-----------------

this py file keep parent class of any other crud files that need to execute query of db

app -> crud -> crud_project.py
-----------------

this py file keep child class of CRUDBase from base.py file that contain query use for the project item of db

app -> crud -> crud_user.py
-----------------

this py file keep child class of CRUDBase from base.py file that contain query use for the user item of db

app -> db
-----------------

this directory contain some files to create engine of sqlalchemy and some other extra code to develop in the future

app -> models -> project.py
-----------------

this py file keep model of project item

app -> models -> user.py
-----------------

this py file keep model of user item

app -> schemas -> user.py
-----------------

this py file keep schemas classes of user item

app -> schemas -> project.py
-----------------

this py file keep schemas classes of project item

app -> schemas -> token.py
-----------------

this py file keep schemas classes of token item

app -> main.py
-----------------

this py file keep scripts and method we need to run app

app -> utils.py
-----------------

this py file keep utils and methods need in all over app and classes to connect the ombre node

statics -> css -> style.css
-----------------

this css file keep css attr to use in ui of app

statics -> image
-----------------

this directory keep images they use in ui of this app

statics -> js
-----------------

this directory keep js files to use in client side of this app


statics -> projects
-----------------

this directory , app saving image of profile and files of each user that we need to save in all over project

templates -> include
-----------------

this directory keeps headers of the app ui html files

templates -> *.html
-----------------

this files are html files they use in the ui of the client side of this app

requirement.txt
-----------------

the python packages we need to install before running the app

source.sql
-----------------

the queries need to create tables in the postgres db

values.json
-----------------

the static words and string and ... we need to use all over app and we access to them in the (app -> core -> read_json.py => obj = ReadJson() ; obj.call_access_method() )