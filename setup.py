import os
import re
import shutil
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('isomorphic')

if sys.argv[-1] == 'publish':
    if os.system('pip freeze | grep wheel'):
        print('wheel not installed.\nUse `pip install wheel`.\nExiting.')
        sys.exit()
    if os.system('pip freeze | grep twine'):
        print('twine not installed.\nUse `pip install twine`.\nExiting.')
        sys.exit()
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    print('You probably want to also tag the version now:')
    print('  git tag -a {} -m \'version {}\''.format(version, version))
    print('  git push --tags')
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_isomorphic.egg-info')
    sys.exit()


setup(
    name='django-isomorphic',
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description=('A Django template backend for JavaScript.'),
    # long_description=README,
    url='https://github.com/wildfish/django-isomorphic',
    author='Jonas Hagstedt',
    author_email='jonas@wildfish.com',
    keywords='django isomorphic',
    install_requires=[
        'Django >= 1.8, <= 1.9'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
