import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='sui-etl',
    version='2.3.1',
    description='Tools for exporting Sui blockchain data to CSV or JSON',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blockchain-etl/sui-etl',
    packages=find_packages(exclude=['schemas', 'tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='sui',
    python_requires='>=3.7.2,<4',
    install_requires=[
        'web3>=5.29,<6',
        'eth-utils==1.10',
        'blockchain-etl-common==1.6.1',
        'eth-abi>=2.2.0,<3.0.0',
        'python-dateutil>=2.8.0,<3',
        'click>=8.0.4,<9',
        'urllib3<2',
        'base58',
        'requests'
    ],
    extras_require={
        'dev': [
            'pytest~=4.3.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'suietl=suietl.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockchain-etl/sui-etl/issues',
        'Chat': 'https://gitter.im/sui-etl/Lobby',
        'Source': 'https://github.com/blockchain-etl/sui-etl',
    },
)
