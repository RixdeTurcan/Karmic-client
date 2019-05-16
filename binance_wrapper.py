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

from binance.client import Client
from configparser import ConfigParser
import time
import sys

class BinanceWrapper:

	def __init__(self):
		self.api_key = None
		self.api_secret = None

		self.client = None

		self.lastTime = time.time()
		self.count = 0
		self.limitPerSec = sys.float_info.max

	def init(self):
		config = ConfigParser()
		config.read("data/config.cfg")

		self.api_key = config.get("binance", "key")
		self.api_secret = config.get("binance", "secret")

		self.client = Client(self.api_key, self.api_secret)

		info = self.getExchangeInfo()
		for limits in info["rateLimits"]:
			if limits["rateLimitType"] == "REQUEST_WEIGHT":
				if limits["interval"] == "SECOND":
					self.limitPerSec = min(self.limitPerSec, float(limits["limit"])/float(limits["intervalNum"]))
				elif limits["interval"] == "MINUTE":
					self.limitPerSec = min(self.limitPerSec, float(limits["limit"])/(60.*float(limits["intervalNum"])))
				elif limits["interval"] == "DAY":
					self.limitPerSec = min(self.limitPerSec, float(limits["limit"])/(60.*60.*24.*float(limits["intervalNum"])))
		self.limitPerSec *= 0.9

	def getExchangeInfo(self):
		self.checkWaiting(1)
		return self.client.get_exchange_info()

	def getLimitsQty(self, symbol, info=None):
		minQty = 0.
		stepQty = 0.
		minNotionnal = 0.
		if info is None:
			info = self.getExchangeInfo()
		for s in info["symbols"]:
			if s["symbol"] == symbol:
				for f in s["filters"]:
					if f["filterType"]=="LOT_SIZE":
						minQty = float(f["minQty"])
						stepQty = float(f["stepSize"])
					if f["filterType"]=="MIN_NOTIONAL":
						if f["applyToMarket"]:
							minNotionnal = float(f["minNotional"])
				break
		return minQty, stepQty, minNotionnal


	def buy(self, symbol, qty):
		self.checkWaiting(1)
		info = self.client.order_market_buy(symbol=symbol, quantity=qty)
		return info["orderId"]

	def sell(self, symbol, qty):
		self.checkWaiting(1)
		info = self.client.order_market_sell(symbol=symbol, quantity=qty)
		return info["orderId"]

	def checkOrder(self, symbol, orderId):
		self.checkWaiting(1)
		info = self.client.get_order(symbol=symbol, orderId=orderId)
		return info

	def checkWaiting(self, weight):
		currTime = time.time()

		self.count = max(0, self.count - (currTime - self.lastTime)*self.limitPerSec)
		self.count += weight

		self.lastTime = currTime

		if self.count > self.limitPerSec:
			time.sleep((self.count-self.limitPerSec)/self.limitPerSec)
			print("waiting "+str((self.count-self.limitPerSec)/self.limitPerSec)+"s")
