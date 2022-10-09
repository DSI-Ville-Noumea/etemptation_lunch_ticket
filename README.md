# Etemptation Lunch Ticket

This script aims to ask for lunch ticket into Etemptation interface.

It is made with [Selenium](https://www.selenium.dev/selenium/docs/api/py/index.html#)
and [Python](https://www.python.org)

## Prerequisites

You have to install the driver of the browser. 


### Manualy

#### Firefox 

```bash
wget -O /tmp/geckodriver-v0.31.0-linux64.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar -C /usr/local/bin/ -xvf /tmp/geckodriver-v0.31.0-linux64.tar.gz
```

#### Chromium

```bash
sudo apt-get install chromium-chromedriver
```

#### Add the path to the config file

```json
{
    "driver_path": "/usr/local/bin/geckodriver"
}
```

### Default

The driver may be installed in the local environment (.venv). This is done by the script. 
You just have to define the browser in the configuration file `settings.json`: 

```json
{
    "browser": "firefox"
}
```

## Usage

```bash
# Clone the repository
git clone 
cd etemptation

# install needed libraries
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

# configure the script with your own information
mv settings.json{.example,}
vim settings.json

# launch the script
python ./etemptation_lunch_ticket.py
```


