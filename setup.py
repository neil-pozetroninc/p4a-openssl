'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 24, 2017

@author: jrm
'''
from setuptools import setup, find_packages


setup(
    name="p4a-openssl",
    version="1.0.2n",
    author="frmdstryr",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url='https://github.com/frmdstryr/p4a-openssl/',
    description="openssl recipes for python-for-android",
    long_description=open("README.md").read(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'p4a_recipe': [
            'openssl = p4a_openssl.__init__:get_recipe',
        ]
    }
)
