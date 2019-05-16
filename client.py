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
from gui import showDisclaimer, showSetup, showApplication


def main():
	dataManager = DataManager()
	dataManager.init()

	if dataManager.status == "disclaimer":
		close = showDisclaimer(dataManager)
		if close:
			return

	if dataManager.status == "setup":
		close = showSetup(dataManager)
		if close:
			return

	socketManager = SocketManager()
	binanceWrapper = BinanceWrapper()
	tradingManager = TradingManager(binanceWrapper)

	while True:
		try:
			socketManager.init()
			binanceWrapper.init()
			tradingManager.init()
			break
		except Exception as e:
			print(e)
			dataManager.setStatus("setup")
			close = showSetup(dataManager)
			if close:
				return

	printLog("Start runtime")
	stop = showApplication(dataManager, socketManager, tradingManager)
	if not stop:
		main()

if __name__ == '__main__':
	main()
