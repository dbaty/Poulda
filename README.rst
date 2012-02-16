Poulda - a simple file upload web service
=========================================

Poulda is a simple file upload web service. It comes from a need I
have to receive large files from friends and family who would not be
bothered to use FTP or anything more complex than a web browser
interface. Amongst its features are such diverse elements as:

- only authenticated users may upload a file;

- user accounts (login and password) are configured in the WSGI
  configuration file;

- a progress bar appears during the upload (unless you disabled
  JavaScript);

- relatively old browsers should be supported relatively well;

- the user interface is in English or French, hopefully not both at
  the same time.


Requirements
============

Poulda requires Python 2.7 and an RDBMS. SQLite will do very well
unless you expect a large number of simultaneous users (in which case
you may want to think twice anyway, since Poulda has not been
developed and tested to scale up).


Installation
============

1. It is highly recommended that you install Poulda in a `virtual
   environment`_. Once you have one, you may install Poulda and its
   dependencies::

       $ easy_install Poulda

3. Download the development `WSGI configuration file`_ and make
   appropriate changes (see the `Configuration`_ section below). [#]_

4. Install Waitress (or use your preferred WSGI server and tweak the
   WSGI configuration file)::

       $ easy_install waitress

5. And finally start the application::

       $ pserve production.ini

.. _virtual environment: http://pypi.python.org/pypi/virtualenv

.. _WSGI configuration file: https://raw.github.com/dbaty/poulda/master/development.ini

.. [#] The source repository also provides a more production-ready
       configuration file: `<https://raw.github.com/dbaty/poulda/master/production.ini>`_.


Configuration
=============

The WSGI configuration file should be modified to fit your system and
your needs:

``poulda.accounts``
  A space (or new line) separated list of user accounts. Each user
  account is composed by the login, followed by a colon, followed by
  the password. Passwords must not contain the space character.

  Examples::

    poulda.accounts = jsmith:secret jane.doe:mYp3ssWord
    poulda.accounts = jsmith:secret
                      jane.doe:mYp3ssWord

``poulda.db_url``
  The database connection string.

  Examples::

    poulda.db_url = sqlite:///%(here)s/Poulda.db
    poulda.db_url = postgresql://poulda:secret_password@localhost/poulda

``poulda.enabled``
  The string "true" if you wish to enable the service. If any other
  value is provided, all pages will show a message that indicates that
  the service is disabled (and users will not be able to do anything).

``poulda.secret``
  A secret string that will be used to encrypt authentication tokens.

``poulda.upload_dir``
  The path to the directory where uploaded files will be stored.


Meta
====

Poulda is hosted on GitHub: `<https://github.com/dbaty/poulda>`_. Feel
free to report bugs and contribute there.

Poulda is based on the `Pyramid web framework`_.

Poulda is written by Damien Baty and is licenced under the 3-clause
BSD license, a copy of which is included in the source.

.. _Pyramid web framework: http://www.pylonsproject.org/