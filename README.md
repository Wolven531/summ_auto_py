# summ_auto_py

This is a fully tested, python-based scraper for SW. It is built with python3.

## Requirements

* Python 3.x ([Python Download Archive](https://www.python.org/downloads/))
* pip3 ([pip install guide](https://pip.pypa.io/en/stable/installing/))
* Django 2.x ([Django install guide](https://docs.djangoproject.com/en/2.0/intro/install/))
* chromedriver ([Install chromedriver for MacOS](http://www.kenst.com/2015/03/installing-chromedriver-on-mac-osx/)

After pip3 and python3 are installed, the remaining requirements can be installed by running the following command from the root directory: `pip3 install -r requirements.txt`

If you plan on running the end to end tests, make sure to update your PATH with the appropriate driver location. The default MacOS setup has the driver located at `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome`. If your driver is located elsewhere, be sure to update your PATH accordingly. See [here](https://coolestguidesontheplanet.com/add-shell-path-osx/)

When adding new end to end tests, be sure to consult the [Selenium Python API](https://selenium-python.readthedocs.io/api.html)

## Running the web server

From the root directory:

1. `cd website`
1. `python3 manage.py runserver 9999` (`9999` is the port)

### To create an admin for the admin site

1. `cd website`
1. `python3 manage.py createsuperuser` (and follow the prompts)

### To run migrations for the web server

From the root directory:

1. `cd website`
1. `python3 manage.py migrate`

### To run tests for the web server (no analysis)

From the root directory:

1. `cd website`
1. `python3 manage.py test mons` (`mons` is the name of the application to test)

### To run tests for the web server (with coverage analysis)

From the root directory:

1. `cd website`
1. `coverage run --source='mons' manage.py test mons` (run the analysis)
1. `coverage report` (view the report)

### To run the end to end tests

From the root directory:

1. `cd website`
1. `python3 manage.py test summ_auto_website.tests.EndToEndTests`

### When creating new templates for the admin

The default admin template path is `/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/django/contrib/admin/templates`

### When updating the Django models

1. Update python file (the model)
1. Run `python3 manage.py makemigrations`
1. Run `python3 manage.py migrate`

### The CLI API

From the root directory:

1. `cd website`
1. Run `python3 manage.py shell`

#### NOTE: To view what SQL statements a migration will generate and run: `python3 manage.py sqlmigrate mons 0001`

#### NOTE: To check for any issues in the project: `python3 manage.py check`

## Running tests

From the root directory, run `python3 -m unittest discover -s test/ -p '*Tests.py'`

## Running the downloader

From the root directory, run `python3 MonsterDownloader.py`

This will load the `data/searched_links.json` and iterate through the `searched_links` property (an array of URLs, each of which belongs to a single monster page). For each URL, the downloader will attempt to parse a monster JSON file and serialize it to disk.

### NOTE: The downloader **WILL** overwrite the local copy of each monster JSON file

### NOTE: The downloader takes some time to run completely (~20 mins for ~500 URLs)

## Screenshots of the application

When end to end tests are run, the tests make use of selenium's ability to take screenshots for posterity. These screenshots are saved at [./website/summ_auto_website/screenshots/](website/summ_auto_website/screenshots)

## TODO / Coming Soon

1. Use elemental links to multiply data collection
1. Parse the [3, 4, 5 Star Monster Guide page](https://summonerswar.co/monster-guide-3-4-5-mons/)
1. Build frontend (ReactJS, likely)
    * [Create React GitHub](https://github.com/facebookincubator/create-react-app)
    * [ReactJS Getting Started](https://reactjs.org/docs/hello-world.html)
