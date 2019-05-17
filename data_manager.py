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

import sqlite3
from configparser import ConfigParser

class DataManager:
	def __init__(self):
		self.dbPair = sqlite3.connect('data/data.db', timeout=30.)
		self.query = self.dbPair.cursor()

		self.status = "disclaimer"
		self.withBinanceTrading = None
		self.withPopup = None
		self.withManualConfirm = None

	def init(self):
		config = ConfigParser()
		config.read("data/pref.cfg")

		self.withBinanceTrading = config.getboolean("gui", "withBinanceTrading", fallback=True)
		self.withPopup = config.getboolean("gui", "withPopup", fallback=False)
		self.withManualConfirm = config.getboolean("gui", "withManualConfirm", fallback=False)

		self.savePreferences()

		self.query.execute("CREATE TABLE IF NOT EXISTS status("
						   "id INTEGER PRIMARY KEY,"
						   "val TEXT)")
		self.dbPair.commit()

		self.query.execute("SELECT val FROM status")
		fetch = self.query.fetchone()
		if fetch is None:
			self.query.execute("INSERT INTO status(val) VALUES(\""+self.status+"\")")
			self.dbPair.commit()
		else:
			self.status = fetch[0]

	def savePreferences(self):
		config = ConfigParser()
		config["gui"] = {
				"withBinanceTrading": self.withBinanceTrading,
				"withPopup": self.withPopup,
				"withManualConfirm": self.withManualConfirm
		}
		with open('data/pref.cfg', 'w') as configfile:
			config.write(configfile)


	def setStatus(self, status):
		self.status = status
		self.query.execute("UPDATE status SET val=\""+self.status+"\"")
		self.dbPair.commit()
