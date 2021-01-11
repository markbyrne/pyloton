 from setuptools import setup

 setup(
   name='Pyloton',
   version='0.1.0',
   author='Mark Byrne',
   author_email='MarkByrne2015@gmail.com',
   packages=['Pyloton'],
   scripts=[],
   url='http://pypi.python.org/pypi/Pyloton/',
   license='LICENSE.txt',
   description='Peloton API Python Integration',
   long_description=open('README.txt').read(),
   install_requires=[
       "requests",
       "json",
	   "os"
   ],
)