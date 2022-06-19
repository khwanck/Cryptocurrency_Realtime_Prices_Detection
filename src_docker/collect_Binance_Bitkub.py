import websocket
import datetime
import requests
from pprint import pprint
import time
import json, requests, time, asyncio
import numpy as np
import datetime as dt

from kafkaHelper import initProducer, produceRecord
from config import config, params

crypto_name=params['currency_1']
bk_name='THB_'+crypto_name.upper()
bn_name=crypto_name.lower()+'usdt'

API_HOST = 'https://api.bitkub.com'
mycoin = ['THB_BTC','THB_USDT']
bitkub_colunm=['last','lowestAsk','highestBid','percentChange','baseVolume','quoteVolume','high24hr','low24hr','change']
binance_colunm=['c','a','b','P','v','q','h','l','p']
binance_data=[]
bitkub_data=[]
bitkub_usdt=[]

def on_message(ws, message):
    global binance_data
    msg = json.loads(message)
    for ls in binance_colunm:
        binance_data.append(float(msg[ls]))
    ws.close()

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print("### closed ###" + close_msg)

def streamKline(currency):
    websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{currency}@ticker'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
    ws.close()

def bitkub_message():
    global bitkub_data
    global bitkub_usdt
    response = requests.get(API_HOST + '/api/market/ticker')
    result = response.json()
    data = result[bk_name]
    for ls in bitkub_colunm:        
        bitkub_data.append(float(data[ls]))
    
    data = result['THB_USDT']
    bitkub_usdt.append(float(data['last']))

# real time data collector
async def async_getCryptoRealTimeData(producer, topic, crypto, time_inverval):
    global binance_data
    global bitkub_data
    global bitkub_usdt
    while True:
        t_0 = time.time()

        bitkub_message()
        #print('bitkub:',bitkub_data)
        #print('usdt:',bitkub_usdt)
        streamKline(bn_name)
        #print('binance:',binance_data)

        if len(bitkub_data)==len(binance_data) and bitkub_data!=[] and binance_data!=[]:
            new_data = {
              "schema": {
                "type": "struct",
                "fields": [
                  {
                    "type": "string",
                    "optional": False,
                    "field": "currency"
                  },                  
                  {
                    "type": "string",
                    "optional": False,
                    "field": "timestamp"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_last"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_lowAsk"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_highBid"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_percentChange"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_baseVolume"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_quoteVolume"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_high24hr"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_low24hr"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bn_change"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "thb_usdt"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_last"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_lowAsk"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_highBid"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_percentChange"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_baseVolume"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_quoteVolume"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_high24hr"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_low24hr"
                  },
                  {
                    "type": "float",
                    "optional": False,
                    "field": "bk_change"
                  }
                ],
                "optional": False,
                "name": "binance_bitkub"
              },
              "payload": {
                "timestamp": dt.datetime.utcnow(),
                "currency": crypto.upper(),
                "bn_last": binance_data[0],
                "bn_lowAsk": binance_data[1],
                "bn_highBid": binance_data[2],
                "bn_percentChange": binance_data[3],
                "bn_baseVolume": binance_data[4],
                "bn_quoteVolume": binance_data[5],
                "bn_high24hr": binance_data[6],
                "bn_low24hr": binance_data[7],
                "bn_change": binance_data[8],
                "thb_usdt": bitkub_usdt[0],
                "bk_last": bitkub_data[0],
                "bk_lowAsk": bitkub_data[1],
                "bk_highBid": bitkub_data[2],
                "bk_percentChange": bitkub_data[3],
                "bk_baseVolume": bitkub_data[4],
                "bk_quoteVolume": bitkub_data[5],
                "bk_high24hr": bitkub_data[6],
                "bk_low24hr": bitkub_data[7],
                "bk_change": bitkub_data[8],
              }
            } 
        
        # debug / print message
        print('API request at time {0}'.format(dt.datetime.utcnow()))
        # produce record to kafka
        produceRecord(new_data, producer, topic)
        # debug \ message in prompt
        print('Record: {}'.format(new_data))

        # clear data
        binance_data=[]
        bitkub_data=[]
        bitkub_usdt=[]

        # wait
        await asyncio.sleep(time_inverval - (time.time() - t_0))


# initialize kafka producer
producer = initProducer()

# define async routine
async def main():
    await asyncio.gather(async_getCryptoRealTimeData(producer, 'topic_Binance_Bitkub', params['currency_1'], params['api_call_period']))

# run async routine
asyncio.run(main())
