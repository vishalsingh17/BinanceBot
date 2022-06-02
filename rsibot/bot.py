import websocket, json, pprint, talib, numpy
import config
from binance.client import Client
from binance.enums import *
import backtrader as bt

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
EMA_PERIOD20 = 20
EMA_PERIOD5 = 5
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.01

closes = []
in_position = False

client = Client(config.API_KEY_BINANCE, config.API_SECRET_BINANCE)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('Sending Order...')
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

def on_open(ws):
    print('Opened Connection')

def on_close(ws):
    print('Closed Connection')

def on_message(ws, message):
    global closes, in_position

    print('Received Message!!')
    json_message = json.load(message)
    pprint.pprint(json_message)

    candle = json.message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))