Installation
~~~~~~~~~~~~~~~~
first step :
~~~~~~~~~~
notice : first make sure your system has postgresql or install it

add commands below =>

$sudo -i -u postgres

postgres@server$ createuser --interactive

notice : (username : ombre)
notice : (password : ombre123)

postgres@server$ createdb ombre

postgres@server$ psql -U ombre

ombre=> \i /home/your_path_to_project/source.sql

second step :
~~~~~~~~~~~~~~~~

notice : make sure your system has virtualenv or install it

notice : we require python eg 3.7

$virtualenv venv

$source /venv/bin/activate

(venv)$pip3 install -r requirement.txt

third step :
~~~~~~~~~~~~~~~~
(venv)$uvicorn app.main:app --reload