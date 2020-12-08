# SSX999_Project

I'm building a cryptocurrency trading algorithm. I will use the GCP Cloud Scheduler to garantee the success of every decision and execution of orders. 

Kraken is the only compatible exchange for this first project. 

## Local install

Install all dependencies
``` sh
poetry install
```

## Usage

To run the algorithm on your computer, run
``` sh
make run-local
```

To run it and write the files in a bucket, run
``` sh
make run-bucket
```

## Deploy

First, add your GCP project ID, service account and bucket in Makefile
``` Makefile
GCP_PROJECT_ID="<YOUR_PROJECT_ID>"
GCP_SERVICE_ACCOUNT="<YOUR_SERVICE_ACCOUNT>"
GCP_BUCKET="<YOUR_BUCKET>"
```

Then run
``` sh
make deploy
```
