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

For further details, see the documentation at `<http://packages.python.org/Poulda>`_ (or in the ``docs/`` folder in the source).