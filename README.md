# SSX999_Project

I'm building a cryptocurrency trading algorithm. I will use the GCP Cloud Scheduler to garantee the success of every decision and execution of orders. 

Kraken is the only compatible exchange for this first project. 

## Local install

First install TA-lib
``` sh
brew install ta-lib
```

Then install all dependencies
``` sh
poetry install
```

## Usage

To launch the algorithm, run
``` sh
poetry run python main.py
```

## Deploy

First, add your GCP project ID and service account in Makefile
``` Makefile
GCP_PROJECT_ID="<YOUR_PROJECT_ID>"
GCP_SERVICE_ACCOUNT="<YOUR_SERVICE_ACCOUNT>"
```

Then run
``` sh
make deploy
```
