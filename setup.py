# install sudo apt-get install python-dev for python.h

from distutils.core import setup, Extension

module1 = Extension('exmod',
                    sources = ['exmodmodule.c'],
					include_dirs = ['/usr/local/include'], 
					libraries = ['pthread']
					)

setup (name = 'PackageExmod',
       version = '1.0',
       description = 'This is a example python to c package',
       ext_modules = [module1])