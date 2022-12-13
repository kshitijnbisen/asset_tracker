# asset_tracker
Managing all these assets of organization

# Technologies Used:

Python
Django
Bootstrap
JavaScript

# Requirements (Prerequisites):

asgiref==3.5.2
backports.zoneinfo==0.2.1
Django==4.1.4
django-crispy-forms==1.14.0
mysqlclient==2.1.1
Pillow==9.3.0
sqlparse==0.4.3


# Installation:

## clone this respository first-
(https://github.com/kshitijnbisen/asset_tracker.git)

## create virtual environment and activate-
python3 -m venv venv
source venv/bin/activate

## Install requirements-
pip install -r requirements.txt

## Setup Database-
**MySQL**
If you want to use MySQL, the following apt commands will get you the packages you need:

'sudo apt-get update'
'sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev'
<sub>
You will be asked to select and confirm a password for the administrative MySQL account.
After the installation, you can create the database directory structure by typing:
</sub>
'sudo mysql_install_db'

You can then run through a simple security script by running:

sudo mysql_secure_installation
You’ll be asked for the administrative password you set for MySQL during installation. Afterwards, you’ll be asked a series of questions. Besides the first question which asks you to choose another administrative password, select yes for each question.

## create database-

We can start by logging into an interactive session with our database software by typing the following (the command is the same regardless of which database software you are using):

mysql -u root -p
You will be prompted for the administrative password you selected during installation. Afterwards, you will be given a prompt.

First, we will create a database for our Django project. Each project should have its own isolated database for security reasons. We will call our database myproject in this guide, but it’s always better to select something more descriptive. We’ll set the default type for the database to UTF-8, which is what Django expects:

CREATE DATABASE assetdb CHARACTER SET UTF8;
Remember to end all commands at an SQL prompt with a semicolon.

Next, we will create a database user which we will use to connect to and interact with the database. Set the password to something strong and secure:

CREATE USER myprojectuser@localhost IDENTIFIED BY 'password';
Now, all we need to do is give our database user access rights to the database we created:

GRANT ALL PRIVILEGES ON assetdb.* TO myprojectuser@localhost;
Flush the changes so that they will be available during the current session:

FLUSH PRIVILEGES;
Exit the SQL prompt to get back to your regular shell session:

exit

## Configure the Django Database Settings

Now that we have a project, we need to configure it to use the database we created.

Open the main Django project settings file located within the child project directory:

nano ~/myproject/myproject/settings.py

Towards the bottom of the file, you will see a DATABASES section that looks like this:

. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

. . .

This is currently configured to use SQLite as a database. We need to change this so that our MySQL/MariaDB database is used instead.

First, change the engine so that it points to the mysql backend instead of the sqlite3 backend. For the NAME, use the name of your database (myproject in our example). We also need to add login credentials. We need the username, password, and host to connect to. We’ll add and leave blank the port option so that the default is selected:

. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'assetdb',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

. . .

When you are finished, save and close the file.
Migrate the Database and Test your Project

Now that the Django settings are configured, we can migrate our data structures to our database and test out the server.

We can begin by creating and applying migrations to our database. Since we don’t have any actual data yet, this will simply set up the initial database structure:

cd ~/myproject
python manage.py makemigrations
python manage.py migrate

After creating the database structure, we can create an administrative account by typing:

python manage.py createsuperuser

You will be asked to select a first_name,last_name provide an email address, and choose and confirm a password for the account.

Once you have an admin account set up, you can test that your database is performing correctly by starting up the Django development server:

python manage.py runserver 0.0.0.0:8000

In your web browser, visit your server’s domain name or IP address followed by :8000 to reach default Django root page:

http://server_domain_or_IP:8000

You should see the default index page:

Django index

Append /admin to the end of the URL and you should be able to access the login screen to the admin interface:

Django admin login

Enter the username and password you just created using the createsuperuser command. You will then be taken to the admin interface:

Django admin interface

When you’re done investigating, you can stop the development server by hitting CTRL-C in your terminal window.

By accessing the admin interface, we have confirmed that our database has stored our user account information and that it can be appropriately accessed.



# Authors:

This project is created by kshitij bisen during his Assessment.