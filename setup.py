import os
from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
LONG_DESCRIPTION = README + '\n\n' + CHANGES

requires = ('pyramid',
            'sqlalchemy',
            'pyramid_tm',
            'zope.sqlalchemy')

setup(name='Poulda',
      version='0.8',
      description='Poulda - a simple upload service',
      long_description=LONG_DESCRIPTION,
      classifiers=(
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Framework :: Pylons',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Programming Language :: Python :: 2.7',
        ),
      author='Damien Baty',
      author_email='damien.baty.remove@gmail.com',
      url='http://packages.python.org/Poulda',
      keywords='web wsgi pyramid file upload',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='poulda',
      install_requires=requires,
      entry_points='''\
      [paste.app_factory]
      main = poulda.app:make_app
      ''',
      message_extractors={'.': (
            ('**.py', 'lingua_python', None),
            ('**.pt', 'lingua_xml', None),
            )}
      )
