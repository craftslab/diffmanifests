#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

from diffmanifests.cmd.version import VERSION


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Define runtime dependencies directly
requirements = [
    'colorama',
    'openpyxl',
    'requests',
    'xmltodict',
]

# Development dependencies (not needed for installation)
dev_requirements = [
    'coverage',
    'coveralls',
    'pytest',
    'setuptools',
    'twine',
    'wheel',
]

setuptools.setup(
    author='Jia Jia',
    author_email='angersax@sina.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    description='Diff Manifests via Gitiles API',
    download_url='https://github.com/craftslab/diffmanifests/archive/v%s.tar.gz' % VERSION,
    entry_points={'console_scripts': ['diffmanifests=diffmanifests.main:main']},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    keywords=['diff', 'manifests', 'gitiles', 'api'],
    license='Apache-2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='diffmanifests',
    packages=setuptools.find_packages(exclude=['examples', 'ez_setup', 'release', 'script', 'tests', 'tests.*']),
    package_data={'diffmanifests': ['config/*.json']},
    url='https://github.com/craftslab/diffmanifests',
    version=VERSION,
    zip_safe=False)
