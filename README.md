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
