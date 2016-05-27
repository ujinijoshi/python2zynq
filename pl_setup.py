# install sudo apt-get install python-dev for python.h

from distutils.core import setup, Extension

module1 = Extension('py2pl',
                    sources = ['py2plmodule.c'],
					include_dirs = ['/usr/local/include'], 
					libraries = ['pthread']
					)

setup (name = 'Packagepy2plmod',
       version = '1.0',
       description = 'This is a example python to pl data transfer package',
       ext_modules = [module1])