import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-feature-toggle',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPLv3',
    description='A simple Django app based on Feature Toggle described by Martin Fowler.',
    long_description=README,
    url='https://github.com/thulasi-ram/django-feature-toggle',
    author='Damodharan Thulasiram',
    author_email='thulasi503@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0+',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=1.8',
        'djutil',
    ],
)