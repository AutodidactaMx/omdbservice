# omdbservice

## Comenzando 🚀

These instructions allow you to get a working copy of the project on your local machine for development and testing purposes._

### Pre-requisitos 📋

For the operation of this application it is required to have the following tools installed and configured:

- _[Python 3.8.5](https://www.python.org/downloads/release/python-385/)_
- _Some development environment : [Pycharm](https://www.jetbrains.com/es-es/pycharm/download/ "Pycharm")_

### Installation 🔧

_We need to install the required libraries for the application to work.
For this we need to install the libraries that are inside
from the requirements.txt file.
Simply run the following command in the terminal:_

```
$ pip install -r requirements.txt
```

_The previous command must be executed in the directory where it is located
the requirements.txt file.
Doing this, they will be installed in the system or in the virtualenv that we have
enabled, the packages noted in the requirements.txt_ file

### Running the project 🔩
_In order to start with the server installation and configuration steps, it is necessary to have the ".env" file that contains all the sensitive information necessary to start the server, such as database connections, passwords and users. For more information about this file contact:

* **Jesus Gutierrez Lopez** 

_To run the project it is necessary to have installed the dependencies included in the requirements file._
_Once everything is installed and configured, it is positioned in the path where the project is, and a command line console is opened where the following command will be entered:_

```
python manage.py runserver
```

_The project will be displayed in the following url:_
```
http://127.0.0.1:8000/
```