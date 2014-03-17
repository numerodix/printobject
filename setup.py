from setuptools import setup

import printobject


setup(
    name='printobject',
    version=printobject.__version__,
    description='Generic pretty printer of python objects',
    author='Martin Matusiak',
    author_email='numerodix@gmail.com',
    url='https://github.com/numerodix/printobject',

    packages=[
        'printobject',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    # don't install as zipped egg
    zip_safe=False,
)
