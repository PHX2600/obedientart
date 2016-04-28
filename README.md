# obedientart
Mandatory Art. State Sponsored Fun.

Set Up
------

### Install prerequisites

    sudo apt install mysql-server python-mysqldb
    sudp pip install -r requirements.txt

### Setup the database

    echo "CREATE DATABASE obedientart" | mysql -u root -p
    mysql -u root -p -D obedientart < schema.sql

Running the Server
------------------

    python /path/to/obediantart.py
