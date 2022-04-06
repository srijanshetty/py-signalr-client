#!/usr/bin/python

from setuptools import setup, find_packages

install_requires = ["requests>=2.18.4", "websockets>=4.0.1"]

setup(
    name="py-signalr-client",
    version="0.0.2",
    author="Srijan R Shetty",
    author_email="srs@srijanshetty.in",
    license="MIT",
    url="https://github.com/srijanshetty/py-signalr-client",
    packages=find_packages(exclude=["tests*"]),
    install_requires=install_requires,
    description="Simple python SignalR client using asyncio.",
    download_url="https://github.com/srijanshetty/py-signalr-client.git",
    keywords=[
        "signalr",
        "sginalr-weboscket",
        "signalr-client",
        "signalr-asyncio",
        "signalr-aio",
    ],
)
