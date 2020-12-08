# SSX999 Project
#
# Augustin BRISSART
# Github: @augustin999
 

import time as tm
import numpy as np
import pandas as pd

from trader import config, dataManager, utils


class Currency(object):

    def __init__(self, name, nEur, nBase):
        """
        This object represents a currency contained in a wallet.
        It can be owned or not, and has a corresponding price.
        """
        self.name = name.upper()
        self.nEur = nEur
        self.nBase = nBase
        self.price = dataManager.get_price(self.name)
        return

    def buyable(self):
        """
        Return True if money is available to buy the currency.
        Return False if currency is already owned.
        """
        return (self.nEur != 0 and self.nBase == 0)
    
    def sellable(self):
        """
        Return True if currency is already owned.
        Return False if money is available to buy the currency.
        """
        return (self.nEur == 0 and self.nBase != 0)

    def buy(self):
        """
        Create a buy order.
        Maker fees are targeted.
        """
        if self.buyable():
            self.price = dataManager.buy(self.name, self.nEur)
            self.nBase = self.nEur / self.price
            self.nEur = 0 
        return

    def sell(self):
        """
        Create a sell order.
        Maker fees are targeted
        """
        if self.sellable():
            self.price = dataManager.sell(self.name, self.nBase)
            self.nEur = self.nBase * self.price
            self.nBase = 0
        return

    def update_price(self):
        self.price = dataManager.get_price(self.name)
        return



class Wallet(object):

    def __init__(self, structure):
        """
        This object represents a wallet.
        A wallet contains multiple Currency instances.

        structure : dictionary
            'capital': float
            'universe': [currency_name_1, currency_name_2, ...]
        """
        self.capital = float(structure['capital'])
        self.universe = structure['universe']
        self.currencies = dict()
        nb_currencies = len(structure['universe'])
        initial_amount_per_currency = self.capital / nb_currencies
        for currency_name in self.universe:
            self.currencies[currency_name] = Currency(
                currency_name,
                initial_amount_per_currency,
                0
            )
        return

    def create_performances(self):
        """
        Create the file which will store the algorithm's performances
        """
        #  prepare fresh performances
        perf_data = dict()
        date = np.trunc(tm.time())
        date = utils.toTs(date)
        perf_data['time'] = str(date)

        total = 0

        for base in self.universe:
            nEurLabel = base + '_nEur'
            nBaseLabel = base + '_nBase'
            priceLabel = base + '_price'
            totalLabel = base + '_total'

            perf_data[nEurLabel] = self.currencies[base].nEur
            perf_data[nBaseLabel] = self.currencies[base].nBase
            perf_data[priceLabel] = self.currencies[base].price
            perf_data[totalLabel] = self.currencies[base].nEur + self.currencies[base].nBase * self.currencies[base].price

            total += perf_data[totalLabel]

        perf_data['total'] = total

        #  persist performances
        performances = pd.DataFrame(perf_data, index=[0])
        utils.dump_as_csv(content=performances, path=config.performances_path)

    def update_performances(self):
        """
        Update the file which stores the algorithm's trading performances
        """
        #  prepare fresh performances
        perf_data = dict()
        date = np.trunc(tm.time())
        date = utils.toTs(date)
        perf_data['time'] = str(date)

        total = 0

        for base in self.universe:
            nEurLabel = base + '_nEur'
            nBaseLabel = base + '_nBase'
            priceLabel = base + '_price'
            totalLabel = base + '_total'

            perf_data[nEurLabel] = self.currencies[base].nEur
            perf_data[nBaseLabel] = self.currencies[base].nBase
            perf_data[priceLabel] = self.currencies[base].price
            perf_data[totalLabel] = self.currencies[base].nEur + self.currencies[base].nBase * self.currencies[base].price

            total += perf_data[totalLabel]
        
        perf_data['total'] = total

        performances = pd.DataFrame(perf_data, index=[0])

        #  Load previous performances
        previous_performances = pd.read_csv(config.performances_path, sep=config.CSV_SEP)
        
        #  Merge previous and fresh performances, and then persist them
        performances = previous_performances.append(performances, ignore_index=True)
        cols = list(performances.columns)
        col1 = cols[0]
        cols.remove(col1)
        performances = performances[cols]
        utils.dump_as_csv(content=performances, path=config.performances_path)
