# -*- coding: utf-8 -*-

# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#       - Бумаги с нулевой волатильностью вывести отдельно.

import os
from itertools import islice
from operator import itemgetter
from threading import Thread


class MaxMinVolatility(Thread):

    volatility_list = []
    zero_volatility = []

    def __init__(self, file_name, dir_name):
        super().__init__()
        self.dir_name = dir_name
        self.file_name = file_name

    def run(self):
        pathfile = os.path.abspath(os.path.join(self.dir_name, self.file_name))
        with open(pathfile, 'r', encoding='utf8') as file:
            prices = [line.split(',', maxsplit=3)[2] for line in islice(file, 1, None)]
            max_price = float(max(prices))
            min_price = float(min(prices))
            half_sum = (max_price + min_price) / 2
            volatility = ((max_price - min_price) / half_sum) * 100
            if volatility > 0:
                MaxMinVolatility.volatility_list.append((self.file_name[:-4], round(volatility, 2)))
            else:
                MaxMinVolatility.zero_volatility.append(self.file_name[:-4])
        MaxMinVolatility.volatility_list.sort(key=itemgetter(1), reverse=True)


def main():

    tickers = [MaxMinVolatility(file_name=file, dir_name='trades') for file in os.listdir('trades')]

    for ticker in tickers:
        ticker.start()

    for ticker in tickers:
        ticker.join()

    print('Максимальная волатильность:')
    for n in range(3):
        print('\t', MaxMinVolatility.volatility_list[n])
    print('Минимальная волатильность:')
    for n in range(3):
        print('\t', MaxMinVolatility.volatility_list[::-1][n])
    print(f'Нулевая волатильность: {MaxMinVolatility.zero_volatility}')


if __name__ == '__main__':
    main()
