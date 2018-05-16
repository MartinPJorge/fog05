#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='fog05',
    version='0.1.3',
    python_requires='>=3',
    author='ADLINK_ATO',
    packages=['fog05', 'fog05/interfaces'],
    install_requires=['networkx', 'jsonschema','websockets','colorama', 'urllib3', 'requests', 'psutil', 'flask'],
    scripts=['bin/fos', 'bin/fos-http','bin/fos-get','bin/fos.bat', 'bin/fos-get.bat','bin/f05ws','bin/f05log.bat',
             'bin/f05log','bin/f05ws.bat','bin/f05wc','bin/f05wc.bat' , 'bin/f05api', 'bin/f05api.bat'],
    include_package_data=True
)