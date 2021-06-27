from TWSE_brokerage_crawler import TWSE_Brokerage_crawler
from TWSE_brokerage_csv_parser import TWSE_brokerage_csv_parser
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date

from base_loger import log
from settings import DB_INTERFACE, DB_USER_NAME, DB_PASSWORD, DB_ADDRESS, DB_NAME, CSV_FOLDER
from DB_structure import TradeDetail

import asyncio
import os

target_list = ['3231', '6142']
twse_crawler = TWSE_Brokerage_crawler("https://bsr.twse.com.tw/bshtm/")
twse_parser = TWSE_brokerage_csv_parser()
tasks = []
db_engine = create_engine(
    f'{DB_INTERFACE}://{DB_USER_NAME}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'
)
date = date.today()

#crawling data from TWSE
for stock_num in target_list:
    log.info(f'Crawing stock num: {stock_num} ...')
    tasks.append(twse_crawler.crawl_data(stock_num))
asyncio.run(asyncio.wait(tasks))

#parse TWSE's csv file then insert to database
for stock_number in target_list:
    log.info(f'Parse stock num csv file: {stock_number} ...')
    brok_data =  twse_parser.parse_data(stock_number)
    summorize_data = twse_parser.brok_summorize(brok_data)
    insert_list = []
    for brok_name, detail in summorize_data.items():
        data = TradeDetail(
            stock_num = stock_number,
            brokerage_name = brok_name,
            date = str(date),
            total = detail['total'],
            buy_avg = detail['buy_avg'],
            buy_quantity = detail['buy_quantity'],
            sell_avg = detail['sell_avg'],
            sell_quantity = detail['sell_quantity']
        )
        insert_list.append(data)
    try:
        log.info(f'Insert {stock_number} data ...')
        with Session(db_engine) as session:
            session.add_all(insert_list)
            session.commit()
        os.remove(
            os.path.join(CSV_FOLDER, f'{stock_number}.csv')
        )
        log.info(f'Done')

    except:
        log.error(f'Insert {stock_number} data fail')
        raise 

