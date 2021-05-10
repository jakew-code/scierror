from setuptools import setup
import pathlib

DIR = pathlib.Path(__file__).parent
README = (DIR / 'README.md').read_text()

VERSION = '0.0.3'
DESCRIPTION = 'Laboratory report tools in Python.'

setup(
    name='scierror',
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/segFault15/scierror',
    author='segFault15',
    packages=['scierror'],
    install_requires=['numpy', 'matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License"
    ]
)
