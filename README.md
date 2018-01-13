# summ_auto_py

This is a fully tested, python-based scraper for SW. It is built with python3.

## Requirements

* Python 3.x ([Python Download Archive](https://www.python.org/downloads/))
* pip3 ([pip install guide](https://pip.pypa.io/en/stable/installing/))
* Django 2.x ([Django install guide](https://docs.djangoproject.com/en/2.0/intro/install/))
* chromedriver ([Install chromedriver for MacOS](http://www.kenst.com/2015/03/installing-chromedriver-on-mac-osx/))

After pip3 and python3 are installed, the remaining requirements can be installed by executing the following command from the root directory: `pip install -r requirements.txt`

If you plan on executing the end to end tests:

* Download chromedriver for your platform [here](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* I place the default windows driver at `C:\Program Files\chromedriver`
* The default MacOS setup has the driver located at `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome`
* If your driver is located elsewhere, be sure to update your PATH accordingly
* [MacOS PATH Update instructions](https://coolestguidesontheplanet.com/add-shell-path-osx/)

When adding new end to end tests, be sure to consult the [Selenium Python API](https://selenium-python.readthedocs.io/api.html)

## Running the web server (from `website`)

1. `python manage.py runserver 9999` (`9999` is the port)

### To create an admin for the admin site (from `website`)

1. `python manage.py createsuperuser` (and follow the prompts)

### Migrations for the web server (from `website`)

1. `python manage.py migrate`

### Tests for the web server (no analysis, from `website`)

1. `python manage.py test` (`mons` can be appended, name of application to test)

### Tests for the web server (with coverage analysis, from `website`)

1. Execute analysis, choose **one**:
    * `coverage run manage.py test`
    * `coverage run --source='mons' manage.py test`
1. View Repoty:
    * `coverage report`

### End to end tests (from `website`)

1. `python manage.py test summ_auto_website.tests.EndToEndTests`

### When creating new templates for the admin

The default admin template path is `/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/django/contrib/admin/templates`

### When updating the Django models

1. Update python file (the model)
1. `python manage.py makemigrations`
1. `python manage.py migrate`

### The CLI API (from `website`)

1. `python manage.py shell`

#### NOTE: To view what SQL statements a migration will generate: `python manage.py sqlmigrate mons 0001`

#### NOTE: To check for any issues in the project: `python manage.py check`

## Tests (from root)

`python -m unittest discover -s test/ -p '*Tests.py'`

## Running the downloader (from root)

`python MonsterDownloader.py`

On Windows, this can be parallelized with the batch script executed from the root directory: `.\UpdateAllMons.bat`

This will load the `data/searched_links.json` and iterate through the `searched_links` property (an array of URLs, each of which belongs to a single monster page). For each URL, the downloader will attempt to parse a monster JSON file and serialize it to disk.

Optionally, you can filter through which searched links you wish to download. Simply pass any number of terms as additional args to the python script.

### Examples

* Download URLs that contain `fire` **OR** `water`: `python MonsterDownloader.py fire water`
* Download URLs that contain `amazon` **OR** `bear`: `python MonsterDownloader.py amazon bear`

### NOTE: This is a union operation, not an intersection. In other words, **ANY** term appearing in the URL will cause that URL to be attempted

### NOTE: The downloader **WILL** overwrite the local copy of each monster JSON file

### NOTE: The downloader takes a while to complete (~20 mins for ~500 URLs)

## Screenshots of the application

When end to end tests are executed, the tests make use of selenium's ability to take screenshots for posterity. These screenshots are saved at [./website/summ_auto_website/screenshots/](website/summ_auto_website/screenshots)

## TODO / Coming Soon

1. Use elemental links to multiply data collection
1. Parse the [3, 4, 5 Star Monster Guide page](https://summonerswar.co/monster-guide-3-4-5-mons/)
1. Build frontend (ReactJS, likely)
    * [Create React GitHub](https://github.com/facebookincubator/create-react-app)
    * [ReactJS Getting Started](https://reactjs.org/docs/hello-world.html)
