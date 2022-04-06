# python-signalr-client
**Python** signalR client using asyncio.
It's mainly based on [TargetProcess signalR client](https://github.com/TargetProcess/signalr-client-py) which uses gevent.

# Performance and supplemental libraries
* For better performance users can install `uvloop` and `ujson` which are automatically detected.
* Users can pass a custom session to the client, i.e a [`cfscrape`](https://github.com/Anorov/cloudflare-scrape) session in order to bypass Cloudflare.

# Compatibility
Asyncio requires Python 3.10+.

# Installation
#### Pypi (most stable)
```python
pip install signalr-client-aio
```
#### Github (master)
```python
pip install git+https://github.com/srijanshetty/py-signalr-client.git
```
