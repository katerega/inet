===
inet
===

.. image:: https://travis-ci.org/nestauk/inet.png?branch=master
   :target: https://travis-ci.org/nestauk/inet

.. image:: https://coveralls.io/repos/Nesta/inet/badge.svg?branch=master&service=github
    :target https://coveralls.io/r/Nesta/inet

Innovation Network Expansion Tool (inet) - Expand a seed list of actors, adding edges and nodes to create a network of innovators. Nodes are added selectively, based on the behavioural characterisitcs of actors in multiple data sources.

Usage
=====

The inet Application Programming Interface is designed to be simple to use. Import inet to your Python program:
```Python
import inet
```
Create an `Inet` class to access the needed functions:
```Python
network = Inet()
```
To load the data:
```Python
network.load(datafile_path)
```
To begin a crawl:
```Python
network.expand()
```

See the [docs](docs/)
Installation
============

Get the Code
------------

inet is available on `GitHub <https://github.com/nestauk/inet>`_.

You can either clone the public repository::

    $ git clone git://github.com/nestauk/inet.git

Download the `tarball <https://github.com/nestauk/inet/tarball/master>`_::

    $ curl -OL https://github.com/nestauk/inet/tarball/master

Or, download the `zipball <https://github.com/nestauk/inet/zipball/master>`_::

    $ curl -OL https://github.com/nestauk/inet/zipball/master

Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install
