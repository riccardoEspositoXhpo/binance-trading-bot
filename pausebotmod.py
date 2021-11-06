from tradingview_ta import TA_Handler, Interval, Exchange
import os
import time
import threading

INTERVAL = Interval.INTERVAL_1_MINUTE #Timeframe for analysis

EXCHANGE = 'BINANCE'
SCREENER = 'CRYPTO'
SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
THRESHOLD = 13 # 7 of 15 MA's indicating sell
TIME_TO_WAIT = 2 # Minutes to wait between analysis
FULL_LOG = False # List analysis result to console

def analyze():

    paused = True

    for symbol in SYMBOLS:  
        analysis = {}
        handler = {}
        
        handler = TA_Handler(
                symbol=symbol,
                exchange=EXCHANGE,
                screener=SCREENER,
                interval=INTERVAL,
                timeout= 10)
    
        try:
            analysis = handler.get_analysis()
        except Exception as e:
            print("pausebotmod:")
            print("Exception:")
            print(e)
        
        ma_sell = analysis.moving_averages['SELL']
        if ma_sell >= THRESHOLD:
            paused = paused and True
            print(f'pausebotmod: {symbol} Market not looking too good, bot paused from buying {ma_sell}/{THRESHOLD}.')
        else:
            print(f'pausebotmod: {symbol} Market looks ok, bot is running {ma_sell}/{THRESHOLD} Waiting {TIME_TO_WAIT} minutes for next market checkup ')
            paused = False

    return paused
    
#if __name__ == '__main__':
def do_work():
      
    while True:
        if not threading.main_thread().is_alive(): exit()
        # print(f'pausebotmod: Fetching market state')
        paused = analyze()
        if paused:
            with open('signals/paused.exc','a+') as f:
                f.write('yes')
        else:
            if os.path.isfile("signals/paused.exc"):
                os.remove('signals/paused.exc')
                        
        # print(f'pausebotmod: Waiting {TIME_TO_WAIT} minutes for next market checkup')    
        time.sleep((TIME_TO_WAIT*60))
