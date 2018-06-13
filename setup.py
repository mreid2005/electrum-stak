#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-stak.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum.png'])
    ]

setup(
    name="Electrum-STAK",
    version=version.ELECTRUM_VERSION,
    install_requires=[
        'pyaes>=0.1a1',
        'ecdsa>=0.9',
        'pbkdf2',
        'requests',
        'qrcode',
        'lyra2re2_hash',
        'protobuf',
        'dnspython',
        'jsonrpclib-pelix',
        'PySocks>=1.6.6',
        'cython',
    ],
    packages=[
        'electrum_stak',
        'electrum_stak_gui',
        'electrum_stak_gui.qt',
        'electrum_stak_plugins',
        'electrum_stak_plugins.audio_modem',
        'electrum_stak_plugins.cosigner_pool',
        'electrum_stak_plugins.email_requests',
        'electrum_stak_plugins.greenaddress_instant',
        'electrum_stak_plugins.hw_wallet',
        'electrum_stak_plugins.keepkey',
        'electrum_stak_plugins.labels',
        'electrum_stak_plugins.ledger',
        'electrum_stak_plugins.trezor',
        'electrum_stak_plugins.digitalbitbox',
        'electrum_stak_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_stak': 'lib',
        'electrum_stak_gui': 'gui',
        'electrum_stak_plugins': 'plugins',
    },
    package_data={
        'electrum_stak': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
            'target*.*',
        ]
    },
    scripts=['electrum-stak'],
    data_files=data_files,
    description="Lightweight STRAKS Wallet",
    author="STRAKS",
    author_email="support@straks.tech",
    license="MIT Licence",
    url="https://github.com/straks/electrum-stak",
    long_description="""Lightweight STRAKS Wallet"""
)
