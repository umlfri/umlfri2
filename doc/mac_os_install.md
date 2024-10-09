Dependency installation for Mac OS X
====================================

Minimum required version of Mac Os X is 10.10 (Yosemite).

Install Xcode
-------------

Xcode tool is required for the UML .FRI installation. You can find it in the apple store.

    https://itunes.apple.com/us/app/xcode/id497799835

Install packaging system brew
-----------------------------

Homebrew is required for installing binary dependencies onto Mac machine.

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Install prerequisites - Qt and Python3
--------------------------------------

UML .FRI tool is written using Python3 language. You can install it using brew.

    brew install python3

UML .FRI is using the QT library for creating GUI. The library is needed to be installed before
the application can be used.

    brew install qt5

Downloading sources using GIT
-----------------------------

GIT version control is used to store source code of UML .FRI application.

You can download your copy of UML .FRI for the first time by using the following commands:

    git clone https://github.com/umlfri/umlfri2.git

If you only want to update existing source code to the newest version, use the following commands inside
the working copy:

    git pull

Install other dependencies
--------------------------

UML .FRI needs the pyparsing library for parsing ufl expressions, lxml library for reading and writing XML, and
some others. You can install it using pip.

Just start following command inside the UML .FRI working directory:

    pip3 install -r doc/dependencies.pip

Download the icon pack
----------------------

You can continue by starting the application if you want. But it looks too weird without installed
icon pack. You can download and install it automatically by starting the download_icons script.

    ./tools/icons/download_icons.py

Starting the application
------------------------

After that, you can start UML .FRI by executing this inside the working directory:

    ./main.py

And now, it is completely upon you, what you want to do and what you will do.
