#Copyright 2019 Jory Lafaye - GPL-3.0-or-later
#
#This file is part of Karmic-client.
#
#    Karmic-client is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Karmic-client is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Karmic-client.  If not, see <https://www.gnu.org/licenses/>.

import printlog
from data_manager import DataManager
from socket_manager import SocketManager
from binance_wrapper import BinanceWrapper
from trading_manager import TradingManager

import time

def main():
	dataManager = DataManager()
	socketManager = SocketManager()
	binanceWrapper = BinanceWrapper()
	tradingManager = TradingManager(binanceWrapper)

	dataManager.init()
	socketManager.init()
	binanceWrapper.init()
	tradingManager.init()

	printLog("Start runtime")

	serverIsOnline = False
	while True:
		try:
			if not socketManager.isServerOnline() and serverIsOnline:
				serverIsOnline = False
				printLog("Server offline")
			if socketManager.isServerOnline() and not serverIsOnline:
				serverIsOnline = True
				printLog("Server online")

			logs = []

			openTrades = socketManager.getOpenTrades()
			if openTrades is not None:
				tradingManager.checkOpenTrades(openTrades)

			trade = socketManager.getNextTrade()
			if trade is not None:
				if trade["side"] == "buy":
					qty = tradingManager.getQty(trade["pair"], trade["price"], trade["bag"])
					log, done = tradingManager.buy(trade["pair"], trade["id"], qty, dataManager.withBinanceTrading, trade["price"])
					logs += log
				elif trade["side"] == "tp":
					log, qty = tradingManager.tp(trade["pair"], trade["id"], dataManager.withBinanceTrading, trade["price"])
					logs += log

			logs += tradingManager.updateTrades()
			for log in logs:
				printLog(log)

		except Exception as e:
			printLog(e)

		time.sleep(0.05)

if __name__ == '__main__':
	main()
