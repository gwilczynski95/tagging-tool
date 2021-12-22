# Tagging tool
Fast tagging tool written in Flask.

Right now the only feature is cutting images to square based on 
selected interest point.

Project based on example from [flask repo.](https://github.com/pallets/flask)


### Installation

**Be sure to use the same version of the code as the version of the docs
you're reading.** You probably want the latest tagged version, but the
default Git version is the main branch.
```bash
git clone https://github.com/gwilczynski95/tagging-tool
cd tagging-tool
```


Create a virtualenv and activate it:
```bash
python3.8 -m venv venv
. venv/bin/activate
```


Or on Windows cmd:
```bash
py -3 -m venv venv
venv\Scripts\activate.bat
```


Install Tagging Tool:

`pip install -e .`

### Making it runnable from PyCharm

1. Create new configuration.
2. In script path enter absolute path to `/venv/bin/flask`
3. Add environmental variable `FLASK_APP=<path to __init__.py in tagging_tool>`
4. You're ready to go!

### Run
```bash
export FLASK_APP=<path to __init__.py in tagging_tool>
export FLASK_ENV=development
flask run
```


Or on Windows cmd::

```bash
set FLASK_APP=<path to __init__.py in tagging_tool>
set FLASK_ENV=development
flask run
```


Open http://localhost:5000 in a browser.