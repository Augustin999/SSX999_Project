# SSX999_Project

I'm building a cryptocurrency trading algorithm. I will use the GCP Cloud Scheduler to garantee the success of every decision and execution of orders. 

Kraken is the only compatible exchange for this first project. 

OHLC data are pulled from the Kraken REST API. 
Technical indicators are computed on it. 
A strategy evaluate the position to hold for the next time period. 
If the position has changed, create an order.
The algorithm is set to only post orders which match the lowest fee rate (called _maker fees_) from the Kraken exchange. 

## Settings

In the config.py file, one can change the default general trading parameters like the reference fiat, the time period to trade, the initial capital to start with (here in euros), and the list of assets to trade. 
``` sh
QUOTE = 'EUR'
PERIOD = '4h'
CAPITAL = 100
UNIVERSE = ['ADA', 'ETH', 'XBT', 'XTZ', 'WAVES', 'EOS']
```

## Local install

Install all dependencies
``` sh
poetry install
```

## Usage

To run the algorithm on your computer, put your Kraken _API_Private_Key_ and _API_Public_key_ files in the directory of the project, and run :
``` sh
make run-local
```

To run it and write the files in a bucket, run :
``` sh
make run-bucket
```

## Deploy

First, add your GCP project ID, service account and bucket and check the other personal settings in Makefile :
``` Makefile
# ----- personal settings -----
GCP_PROJECT_ID="<PROJECT-ID>"
GCP_SERVICE_ACCOUNT="<SERVICE-ACCOUNT-NAME"
GCP_BUCKET="<BUCKET-NAME>"
GCP_REGION="europe-west6"
SCHEDULE="1 */4 * * *"
# ----- ----------------- -----
```

Then create a GCP bucket named as given in the settings, and put your Kraken _API_Private_Key_ and _API_Public_key_ files in a directory called _keys_.

Then run
``` sh
make deploy
```

## Objectives of this project

This is probably one of the simplest cryptocurrency trading algorithms that one can find on the Internet. However, my purposes were to learn more about trading, programming in Python and using tools like GCP or APIs providing data. This project met these goals. I learned a lot on each of these aspects. The strategy implemented in this repository has given good results on previous historical data but was not confronted to money management measurements. 

Use it at your own risks. I do not claim to have found the Grail at all. I am not responsible for any loss that one can suffer through this algorithm.
