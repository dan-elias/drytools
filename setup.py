from setuptools import setup, find_packages
from codecs import open
from os import path

from drytools import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='drytools',
    version=__version__,
    description='Tools for reducing repetition in Python code',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/dan-elias/drytools',
    download_url='https://github.com/dan-elias/drytools/tarball/' + __version__,
    license='GPLv3',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Dan Elias',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='daniel@elias-family.com'
)
