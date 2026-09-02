# Etemptation Lunch Ticket

This script aims to ask for lunch ticket into Etemptation interface.

It is made with [Selenium](https://www.selenium.dev/selenium/docs/api/py/index.html#)
and [Python](https://www.python.org)

## Prerequisites

You have to install docker locally to run the image.


## Usage

### Build the image 
```bash
# Clone the repository
git clone 
cd etemptation_lunch_ticket

docker build -t harbor.ville-noumea.nc/infra/etemptation_lunch_ticket .
```

### Push the image on harbor
```bash
docker login -u USER harbor.ville-noumea.nc
docker push harbor.ville-noumea.nc/infra/etemptation_lunch_ticket
```

### Execute on production 
```bash
# launch the script
docker run --rm -e USERNAME="USER" -e PASSWORD="PASS" harbor.ville-noumea.nc/infra/etemptation_lunch_ticket
```

### Execute on qualif
```bash
# launch the script
docker run --rm -e USERNAME="USER" -e PASSWORD="PASS" -e WEBSITE_URL="https://etemptation-qual.ville-noumea.nc" harbor.ville-noumea.nc/infra/etemptation_lunch_ticket
```
