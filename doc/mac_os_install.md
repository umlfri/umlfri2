Dependency installation for Mac OS X
====================================

1. Install Python for Mac
-------------------------

Version required for the UML .FRI project is **3.4**. Version 3.5 is not yet supported by the PySide library.
You can download correct Python version from this link:
https://www.python.org/downloads/release/python-343/

2. Install packaging systems - brew and pip
-------------------------------------------

Homebrew is required for installing binary dependencies onto Mac machine. Pip, on the other hand, is used to install
Python libraries.

    curl https://bootstrap.pypa.io/get-pip.py | python3
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

3. Install QT library
---------------------

UML .FRI is written using the QT library. The library is needed to be installed before the application can be used.

    brew install qt

Python wrapper for QT library used in UML .FRI is PySide. It can be installed using pip package manageer.

    brew install cmake
    pip install PySide

4. Install other dependencies
-----------------------------

UML .FRI needs the pyparsing library for parsing ufl expressions and lxml library for reading and writing XML.

    pip install pyparsing
    pip install lxml

5. Downloading sources using mercurial
--------------------------------------

Mercurial version control is used to store source code of UML .FRI application.

You can download your copy of UML .FRI for the first time by using the following commands:

    brew install mercurial
    hg clone http://hg.janik.ws/public/umlfri2

If you only want to update existing source code to the newest version, use the following commands inside the working copy:

    hg pull && hg update

6. Starting the application
---------------------------

I have to say, I have no idea why the following is required, but it is. PySide is not working without the following
command executed before the application start:

    export DYLD_LIBRARY_PATH=/Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/PySide

After that, you can start UML .FRI by executing this inside the working directory:

    ./main.py

And now, it is completely upon you, what you want to do and what you will do.
