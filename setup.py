from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-fab',
version='1.0',
description='Common fabric tools for django projects',
long_description=read('README.rst'),
author='Harley Bussell',
author_email='modmac@gmail.com',
url='http://github.com/hbussell/django-fab',
classifiers=[
  "License :: OSI Approved :: GNU General Public License (GPL)",
  "Programming Language :: Python",
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Framework :: Django",
  "Environment :: Console",
  "Topic :: Software Development",
  "Topic :: System :: Software Distribution"

],
keywords='django fabric deployment',
zip_safe=False
license='GPL',
install_requires=[
'setuptools',
],
packages = find_packages(),
include_package_data = True,
)
