# summ_auto_py

This is a fully tested, python-based scraper for SW. It is built with python3.

## Running tests

From the root directory, run `python3 -m unittest discover -s test/ -p '*Tests.py'`

## Running the downloader

From the root directory, run `python3 src/MonsterDownloader.py`

This will load the `data/searched_links.json` and iterate through the `searched_links` property (an array of URLs, each of which belongs to a single monster page). For each URL, the downloader will attempt to parse a monster JSON file and serialize it to disk.

### NOTE: The downloader **WILL** overwrite the local copy of each monster JSON file

### NOTE: The downloader takes some time to run completely (~20 mins for ~500 URLs)

## TODO / Coming Soon

1. Use elemental links to multiply data collection
1. Parse the [3, 4, 5 Star Monster Guide page](https://summonerswar.co/monster-guide-3-4-5-mons/)
1. Spin up Django server to provide data
    * [Django Project](https://www.djangoproject.com)
    * [Mozilla on Django](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
1. Build frontend (ReactJS, likely)
    * [Create React GitHub](https://github.com/facebookincubator/create-react-app)
    * [ReactJS Getting Started](https://reactjs.org/docs/hello-world.html)
