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

import zmq
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from configparser import ConfigParser

class SocketManager:
	def __init__(self):
		self.karmicIp = None
		self.karmicTradePort = None
		self.karmicInfoPort = None
		self.karmicToken = None
		self.karmicSecret = None

		self.crypt = None

		self.infoSocket = None
		self.tradeSocket = None

	def init(self):
		config = ConfigParser()
		config.read("data/config.cfg")

		self.karmicIp = config.get("karmic", "ip")
		self.karmicTradePort = config.get("karmic", "tradePort")
		self.karmicInfoPort = config.get("karmic", "infoPort")
		self.karmicToken = config.get("karmic", "token")
		self.karmicSecret = config.get("karmic", "secret")

		self.crypt = Fernet(b64decode(self.karmicSecret))

		context = zmq.Context()
		self.infoSocket = context.socket(zmq.SUB)
		self.infoSocket.connect(str("tcp://"+self.karmicIp+":"+self.karmicInfoPort).encode('utf-8'))
		self.infoSocket.setsockopt(zmq.SUBSCRIBE, self.karmicToken.encode("utf-8"))

		self.tradeSocket = context.socket(zmq.SUB)
		self.tradeSocket.connect(str("tcp://"+self.karmicIp+":"+self.karmicTradePort).encode('utf-8'))
		self.tradeSocket.setsockopt(zmq.SUBSCRIBE, self.karmicToken.encode("utf-8"))

	def receiveOpenTrade(self):
		try:
			return self.infoSocket.recv(flags=zmq.NOBLOCK).decode("utf-8").split(" ", 1)
		except 	zmq.Again:
			return [None, None]


	def getOpenTrades(self):
		topic, cryptedMess = self.receiveOpenTrade()

		if cryptedMess is not None:
			mess = self.crypt.decrypt(b64decode(cryptedMess)).decode("utf-8")

			info = mess.split(":")
			infoOpenTrades = info[0].split("_")

			openTrades = []
			for trade in infoOpenTrades:
				t = trade.split('.')
				if len(t) == 2:
					openTrades.append({
							"pair": t[0],
							"id": t[1]
					})

			return openTrades
		return None

	def receiveTrade(self):
		try:
			return self.tradeSocket.recv(flags=zmq.NOBLOCK).decode("utf-8").split(" ", 1)
		except 	zmq.Again:
			return [None, None]

	def getNextTrade(self):

		topic, cryptedMess = self.receiveTrade()
		if cryptedMess is not None:
			trade = self.crypt.decrypt(b64decode(cryptedMess)).decode("utf-8").split("_")

			return {
					"side": trade[0],
					"pair": trade[1],
					"id": int(trade[2]),
					"bag": float(trade[3]),
					"price": float(trade[4])
			}
		return None
