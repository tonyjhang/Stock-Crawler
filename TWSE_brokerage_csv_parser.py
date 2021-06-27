from Parser import Parser

from settings import CSV_FOLDER
from base_loger import log

import csv
import os
import codecs

class TWSE_brokerage_csv_parser(Parser):    
    def parse_data(self, stock_num:str) -> iter:
        csv_path = os.path.join(CSV_FOLDER, f'{stock_num}.csv')
        if os.path.exists(csv_path) is not True:
            log.error(f'{csv_path} is not exist')
            raise FileNotFoundError

        with codecs.open(csv_path, 'r', encoding='big5', errors='ignore') as fdata:
            rows = csv.reader(fdata, delimiter=',')
            for row in rows:
                yield row

    def brok_summorize(self, brok_data:iter) -> dict:
        result = {}
        counter = 0
        for data in brok_data:
            counter += 1
            #prevent return title
            if counter < 4:
                continue

            #there's two data in one row
            for i in range(1, 2):
                dist = 0
                if i == 2:
                    dist = 6
                if data[1+dist] == '':
                    continue
                name = data[1+dist][4:].strip()
                if name not in result:
                    result[name] = {}
                    result[name]['buy_avg'] = 0.0
                    result[name]['sell_avg'] = 0.0
                    result[name]['buy_quantity'] = 0
                    result[name]['sell_quantity'] = 0
                    result[name]['total'] = 0
                price = float(data[2+dist])
                buy = int(data[3+dist])
                sell = int(data[4+dist])
                if buy != 0:
                    total = price * buy
                    result[name]['total'] += total
                    if result[name]['buy_quantity'] == 0:
                        result[name]['buy_quantity'] += buy
                        result[name]['buy_avg'] = price
                        continue

                    piror_total = (result[name]['buy_avg'] * result[name]['buy_quantity'])
                    result[name]['buy_avg'] = (piror_total + total) / \
                        (result[name]['buy_quantity'] + buy)
                    result[name]['buy_quantity'] += buy
                else:
                    total = price * sell
                    result[name]['total'] -= total
                    if result[name]['sell_quantity'] == 0:
                        result[name]['sell_quantity'] += buy
                        result[name]['sell_avg'] = price
                        continue

                    piror_total = (result[name]['sell_avg'] * result[name]['sell_quantity'])
                    result[name]['sell_avg'] = (piror_total + total) / \
                        (result[name]['sell_quantity'] + sell)
                    result[name]['sell_quantity'] += sell
        return result



