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

from configparser import ConfigParser
import sqlite3
import math
import time
from datetime import datetime

class TradingManager:
	def __init__(self, binanceWrapper):
		self.dbPair = sqlite3.connect('data/trading.db', timeout=30.)
		self.query = self.dbPair.cursor()

		self.binanceWrapper = binanceWrapper

		self.fund = 0

		self.limitQty = {}

		self.initLogs = []

	def init(self):
		self.query.execute("CREATE TABLE IF NOT EXISTS trades("
						   "id INTEGER PRIMARY KEY,"
						   "idKarmic INTEGER,"
						   "idBuyBinance INTEGER,"
						   "idTpBinance INTEGER,"
						   "pair TEXT,"
						   "timestampBuy INTEGER,"
						   "timestampTp INTEGER,"
						   "qty REAL,"
						   "priceBuy REAL,"
						   "priceTp REAL)")

		self.query.execute("CREATE TABLE IF NOT EXISTS logs("
						   "id INTEGER PRIMARY KEY,"
						   "val TEXT)")
		self.dbPair.commit()

		config = ConfigParser()
		config.read("data/config.cfg")
		self.fund = config.getint("binance", "fund", fallback=0)
		if self.fund<=0:
			raise Exception("No sufficient fund")

		info = self.binanceWrapper.getExchangeInfo()
		for symbol in info["symbols"]:
			minQty, stepQty, minNotional = self.binanceWrapper.getLimitsQty(symbol["symbol"], info)
			self.limitQty[symbol["symbol"]] = {
					"minQty": minQty,
					"stepQty": stepQty,
					"minNotional": minNotional
			}

	def checkOpenTrades(self, openTrades):
		self.query.execute("SELECT pair, idKarmic FROM trades WHERE timestampTP IS NULL")
		fetch = self.query.fetchall()
		for f in fetch:
			pair = f[0]
			idKarmic = f[1]

			found = False
			for trade in openTrades:
				if trade["pair"] == pair and int(trade["id"]) == idKarmic:
					found = True
					break

			if not found:
				self.tp(pair, idKarmic, True, None)

	def getLogs(self):
		logs = []

		self.query.execute("SELECT val FROM logs ORDER BY id")
		fetch = self.query.fetchall()
		for f in fetch:
			logs.append(f[0])

		return logs

	def getQty(self, pair, price, bag):
		minQty = max(self.limitQty[pair]["minQty"], self.limitQty[pair]["minNotional"]/price*1.1)
		minQty = math.ceil(minQty/self.limitQty[pair]["stepQty"])
		minQty *= self.limitQty[pair]["stepQty"]

		qty = max(self.fund*bag/price, minQty)
		qty = math.floor(qty/self.limitQty[pair]["stepQty"])
		qty *= self.limitQty[pair]["stepQty"]

		return qty

	def updateTrades(self):
		logs = []

		self.query.execute("SELECT id, pair, idBuyBinance, timestampBuy, qty FROM trades WHERE priceBUY IS NULL")
		fetch = self.query.fetchall()
		for f in fetch:
			idTrade = f[0]
			pair = f[1]
			idBinance = f[2]
			timestampBuy = f[3]
			qty = f[4]

			info = self.binanceWrapper.checkOrder(pair, idBinance)
			if info["status"] == "FILLED":
				price = float(info["cummulativeQuoteQty"])
				self.query.execute("UPDATE trades SET priceBuy="+str(price)+" WHERE id="+str(idTrade))
				self.dbPair.commit()

				logs.append(self.logBuy(pair, timestampBuy, qty, price))

		self.query.execute("SELECT id, pair, idTpBinance, timestampTp, qty, priceBuy FROM trades WHERE priceTp IS NULL AND timestampTp IS NOT NULL")
		fetch = self.query.fetchall()
		for f in fetch:
			idTrade = f[0]
			pair = f[1]
			idBinance = f[2]
			timestampTp = f[3]
			qty = f[4]
			priceBuy = f[5]

			info = self.binanceWrapper.checkOrder(pair, idBinance)
			if info["status"] == "FILLED":
				price = float(info["cummulativeQuoteQty"])
				self.query.execute("UPDATE trades SET priceTp="+str(price)+" WHERE id="+str(idTrade))
				self.dbPair.commit()

				logs.append(self.logTp(pair, timestampTp, qty, price, priceBuy))

		return logs

	def checkBuy(self, pair, idKarmic):
		self.query.execute("SELECT id FROM trades WHERE pair=\"" + pair + "\" AND idKarmic=" + str(idKarmic))
		fetch = self.query.fetchone()

		return fetch is None

	def buy(self, pair, idKarmic, qty, withBinanceTrading, price):
		logs = []
		done = False

		self.query.execute("SELECT id FROM trades WHERE pair=\"" + pair + "\" AND idKarmic=" + str(idKarmic))
		fetch = self.query.fetchone()

		if fetch is None:
			idBinance = 0
			if withBinanceTrading:
				idBinance = self.binanceWrapper.buy(pair, qty)

			timestamp = round(time.time())

			if withBinanceTrading:
				self.query.execute("INSERT INTO trades(idKarmic, idBuyBinance, pair, qty, timestampBuy) VALUES("
								   " "+str(idKarmic)+","
								   " "+str(idBinance)+","
								   " \""+pair+"\","
								   " "+str(qty)+","
								   " "+str(timestamp)+")")
			else:
				self.query.execute("INSERT INTO trades(idKarmic, idBuyBinance, pair, qty, timestampBuy, priceBuy) VALUES("
								   " "+str(idKarmic)+","
								   " "+str(idBinance)+","
								   " \""+pair+"\","
								   " "+str(qty)+","
								   " "+str(timestamp)+","
								   " "+str(price)+")")

				logs.append(self.logBuy(pair, timestamp, qty, price))

			self.dbPair.commit()

			done = True

		return logs, done

	def checkTp(self, pair, idKarmic):
		self.query.execute("SELECT qty FROM trades WHERE timestampTp IS NULL AND pair=\""+pair+"\" AND idKarmic="+str(idKarmic))
		fetch = self.query.fetchone()
		if fetch is not None:
			return fetch[0], True
		return 0., False




	def tp(self, pair, idKarmic, withBinanceTrading, price):
		logs = []
		qty = 0.
		self.query.execute("SELECT id, qty, idBuyBinance, priceBuy FROM trades WHERE timestampTp IS NULL AND pair=\""+pair+"\" AND idKarmic="+str(idKarmic))
		fetch = self.query.fetchone()
		if fetch is not None:
			idTrade = fetch[0]
			qty = fetch[1]
			idBuyBinance = fetch[2]
			priceBuy = fetch[3]

			idBinance = 0
			if idBuyBinance != 0 and withBinanceTrading:
				idBinance = self.binanceWrapper.sell(pair, qty)

			timestamp = round(time.time())

			if idBinance == 0:
				self.query.execute("UPDATE trades SET timestampTp=" + str(timestamp) + ", idTpBinance=" + str(idBinance) + ", priceTp="+str(price)+" WHERE id=" + str(idTrade))

				logs.append(self.logTp(pair, timestamp, qty, price, priceBuy))
			else:
				self.query.execute("UPDATE trades SET timestampTp="+str(timestamp)+", idTpBinance="+str(idBinance)+" WHERE id="+str(idTrade))
			self.dbPair.commit()

		return logs, qty

	def logBuy(self, pair, timestamp, qty, price):
		posQuote = pair.find("USDT")
		date = str(datetime.fromtimestamp(timestamp).strftime('%d/%m - %Hh %Mm %Ss'))

		log = date+" : BUY "+str(qty)+" "+pair[:posQuote]+" à "+str(price)+"$"
		self.query.execute("INSERT INTO logs(val) VALUES(\""+log+"\")")
		self.dbPair.commit()

		return log

	def logTp(self, pair, timestamp, qty, price, priceBuy):
		posQuote = pair.find("USDT")
		date = str(datetime.fromtimestamp(timestamp).strftime('%d/%m - %Hh %Mm %Ss'))
		profit = round(100 * (price / priceBuy - 1.), 1)

		log = date + " : TP " + str(qty) + " " + pair[:posQuote] + " à " + str(price) + "$ -> profit : " + str(profit) + "%"
		self.query.execute("INSERT INTO logs(val) VALUES(\""+log+"\")")
		self.dbPair.commit()

		return log
