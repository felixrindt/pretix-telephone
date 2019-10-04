import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1)
        build.run(self)


cmdclass = {
    'build': CustomBuild
}


setup(
    name='pretix-telephone',
    version='2.2.0',
    description='This pretix plugin adds a contact question asking for the telephone number.',
    long_description=long_description,
    url='https://github.com/felixrindt/pretix-telephone',
    author='Felix Rindt',
    author_email='felix@rindt.me',
    license='Apache Software License',
    keywords='pretix plugin telephone',

    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_telephone=pretix_telephone:PretixPluginMeta
""",
)
