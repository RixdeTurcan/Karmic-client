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

from appJar import gui
from configparser import ConfigParser

def setup():
	app = gui(showIcon=False)
	app.setTitle("Karmic Bot")

	return app


def showDisclaimer(dataManager):
	app = setup()
	app.addLabel("Title", "Karmic Bot")
	app.startLabelFrame("Conditions d'utilisation")

	disclaimer = "Karmic bot est un logiciel libre et open-source sous licence GPL 3.0, permettant de se connecter à des serveurs de données et de trading. " \
				 "De ce fait, ce logiciel appartient de droit à son utilisateur.\n\n"
	disclaimer += "L'utilisation de ces données est à la responsabilité entière de l'utilisateur et ne saurait engager la responsabilité de leurs émetteurs.\n\n"
	disclaimer += "Ce logiciel n'est en aucun cas destiné à conseiller l'utilisateur ou à l'aider à la prise de décision concernant des produits financiers. " \
				  "Ses auteurs ne seraient donc être tenus responsables des conséquences de l'utilisation de celui-ci."

	app.addMessage("disclaimer", disclaimer)

	app.stopLabelFrame()

	completed = [False]
	def acceptDisclaimer(name):
		if name == "Accepter":
			dataManager.setStatus("setup")
			completed[0] = True
		app.stop()

	app.addButtons(["Refuser", "Accepter"], acceptDisclaimer)

	isStop = [False]
	def stop():
		isStop[0] = not completed[0]
		return True
	app.setStopFunction(stop)

	app.go()
	return isStop[0]

def showSetup(dataManager):
	config = ConfigParser()
	config.read("data/config.cfg")

	ip = config.get("karmic", "ip", fallback="127.0.0.1")
	tradePort = config.get("karmic", "tradePort", fallback="33909")
	infoPort = config.get("karmic", "infoPort", fallback="33910")
	token = config.get("karmic", "token", fallback="")
	secret = config.get("karmic", "secret", fallback="")
	binanceKey = config.get("binance", "key", fallback="")
	binanceSecret = config.get("binance", "secret", fallback="")
	binancefund = config.get("binance", "fund", fallback="100")

	app = setup()
	app.addLabel("Title", "Karmic Bot")
	app.startLabelFrame("Configuration de l'application")

	entryIp = "Karmic IP : "
	app.addLabel(entryIp, entryIp, 0, 0)
	app.addValidationEntry(entryIp, 0, 1)
	app.setEntry(entryIp, ip)
	app.setEntryWidth(entryIp, 16)

	entryTradePort = "Karmic Trade Port : "
	app.addLabel(entryTradePort, entryTradePort, 1, 0)
	app.addValidationEntry(entryTradePort, 1, 1)
	app.setEntry(entryTradePort, tradePort)
	app.setEntryWidth(entryTradePort, 6)

	entryInfoPort = "Karmic Info Port : "
	app.addLabel(entryInfoPort, entryInfoPort, 2, 0)
	app.addValidationEntry(entryInfoPort, 2, 1)
	app.setEntry(entryInfoPort, infoPort)
	app.setEntryWidth(entryInfoPort, 6)

	app.addLabel("sep1", " ", 3, 0)

	entryToken = "Karmic Token : "
	app.addLabel(entryToken, entryToken, 4, 0)
	app.addValidationEntry(entryToken, 4, 1)
	app.setEntry(entryToken, token)
	app.setEntryWidth(entryToken, 25)

	entrySecret = "Karmic Secret : "
	app.addLabel(entrySecret, entrySecret, 5, 0)
	app.addValidationEntry(entrySecret, 5, 1)
	app.setEntry(entrySecret, secret)
	app.setEntryWidth(entrySecret, 70)

	app.addLabel("sep2", " ", 6, 0)
	entryBinanceKey = "Binance Key : "
	app.addLabel(entryBinanceKey, entryBinanceKey, 7, 0)
	app.addValidationEntry(entryBinanceKey, 7, 1)
	app.setEntry(entryBinanceKey, binanceKey)
	app.setEntryWidth(entryBinanceKey, 80)

	entryBinanceSecret = "Binance Secret : "
	app.addLabel(entryBinanceSecret, entryBinanceSecret, 8, 0)
	app.addValidationEntry(entryBinanceSecret, 8, 1)
	app.setEntry(entryBinanceSecret, binanceSecret)
	app.setEntryWidth(entryBinanceSecret, 80)

	app.addLabel("sep3", " ", 9, 0)
	entryBinanceFund = "Fonds alloués sur Binance (USDT) : "
	app.addLabel(entryBinanceFund, entryBinanceFund, 10, 0)
	app.addValidationEntry(entryBinanceFund, 10, 1)
	app.setEntry(entryBinanceFund, binancefund)
	app.setEntryWidth(entryBinanceFund, 7)

	completed = [False]
	def validSetup():
		valid = True

		ip = app.getEntry(entryIp)
		ipComp = ip.split(".")
		app.setEntryValid(entryIp)
		if len(ipComp) != 4:
			valid = False
			app.setEntryInvalid(entryIp)
		else:
			for comp in ipComp:
				if not comp.isdigit() or int(comp) < 0 or int(comp) > 255:
					valid = False
					app.setEntryInvalid(entryIp)
					break

		tradePort = app.getEntry(entryTradePort)
		app.setEntryValid(entryTradePort)
		if not tradePort.isdigit() or int(tradePort) < 0 or int(tradePort) > 65535:
			valid = False
			app.setEntryInvalid(entryTradePort)

		infoPort = app.getEntry(entryInfoPort)
		app.setEntryValid(entryInfoPort)
		if not infoPort.isdigit() or int(infoPort) < 0 or int(infoPort) > 65535:
			valid = False
			app.setEntryInvalid(entryInfoPort)

		token = app.getEntry(entryToken)
		app.setEntryValid(entryToken)
		if len(token) != 20 or not token.isalnum():
			valid = False
			app.setEntryInvalid(entryToken)

		secret = app.getEntry(entrySecret)
		app.setEntryValid(entrySecret)
		if len(secret) != 60 or not secret[:-1].isalnum() or secret[-1] != "=":
			valid = False
			app.setEntryInvalid(entrySecret)

		binanceKey = app.getEntry(entryBinanceKey)
		app.setEntryValid(entryBinanceKey)
		if not binanceKey.isalnum():
			valid = False
			app.setEntryInvalid(entryBinanceKey)

		binanceSecret = app.getEntry(entryBinanceSecret)
		app.setEntryValid(entryBinanceSecret)
		if not binanceSecret.isalnum():
			valid = False
			app.setEntryInvalid(entryBinanceSecret)

		binanceFund = app.getEntry(entryBinanceFund)
		app.setEntryValid(entryBinanceFund)
		if not binanceFund.isdigit() or int(binanceFund)<=0:
			valid = False
			app.setEntryInvalid(entryBinanceFund)

		if valid:
			print(ip)
			config = ConfigParser()
			config["karmic"] = {
					"ip": ip,
					"tradePort": tradePort,
					"infoPort": infoPort,
					"token": token,
					"secret": secret
			}
			config["binance"] = {
					"key": binanceKey,
					"secret": binanceSecret,
					"fund": binanceFund
			}
			with open('data/config.cfg', 'w') as configfile:
				config.write(configfile)
			dataManager.setStatus("run")
			completed[0] = True
			app.stop()

	app.stopLabelFrame()

	app.addButton("Valider", validSetup)

	isStop = [False]
	def stop():
		isStop[0] = not completed[0]
		return True
	app.setStopFunction(stop)

	app.go()
	return isStop[0]


def showApplication(dataManager, socketManager, tradingManager):
	app = setup()

	app.addLabel("Title", "Karmic Bot")
	app.startLabelFrame("Historique des trades")
	app.startScrollPane("historyContainer2")
	app.setScrollPaneWidth("historyContainer2", 700)
	initLog = ""
	initLogs = tradingManager.getLogs()
	for log in initLogs:
		initLog = log+"\n"+initLog
	app.addLabel("history", initLog)
	app.stopScrollPane()
	app.stopLabelFrame()

	app.addLabel("server", "Status du serveur Karmic : Offline")

	binanceTradingCheckBox = "Activer le trading Binance "
	popupNewTradeCheckBox = "Activer un Popup à chaque trade"
	manualConfirmationCheckBox = "Demander une confirmation manuelle à chaque trade"
	app.addCheckBox(binanceTradingCheckBox)
	if dataManager.withBinanceTrading:
		app.setCheckBox(binanceTradingCheckBox)

	app.addCheckBox(popupNewTradeCheckBox)
	if dataManager.withPopup:
		app.setCheckBox(popupNewTradeCheckBox)

	app.addCheckBox(manualConfirmationCheckBox)
	if dataManager.withManualConfirm:
		app.setCheckBox(manualConfirmationCheckBox)

	stop = [True]
	def gotoConfig(name):
		stop[0] = False
		if name == "Conditions d'utilisation":
			dataManager.setStatus("disclaimer")
		else:
			dataManager.setStatus("setup")
		app.stop()
	app.addButtons(["Conditions d'utilisation", "Paramètres"], gotoConfig)

	app.startSubWindow("Trade info")
	app.addImage("warning", "data/spaceship.png")
	tradeInfoLabel = "Trade information"
	app.addLabel(tradeInfoLabel, "")

	def closePopup():
		app.hideSubWindow("Trade info")
	app.addButton("ok", closePopup)

	app.stopSubWindow()

	countServer = [100]
	serverIsOnline = [False]
	def updateTrade():
		try:
			countServer[0] += 1
			if countServer[0] > 100 and serverIsOnline[0]:
				app.setLabel("server", "Status du serveur Karmic : Offline")
				serverIsOnline[0] = False
			if countServer[0] <= 100 and not serverIsOnline[0]:
				app.setLabel("server", "Status du serveur Karmic : Online")
				serverIsOnline[0] = True

			openTrades = socketManager.getOpenTrades()
			if openTrades is not None:
				tradingManager.checkOpenTrades(openTrades)
				countServer[0] = 0

			updatePref = False

			withBinanceTrading = app.getCheckBox(binanceTradingCheckBox)
			if withBinanceTrading != dataManager.withBinanceTrading:
				updatePref = True
				dataManager.withBinanceTrading = withBinanceTrading

			withPopup = app.getCheckBox(popupNewTradeCheckBox)
			if withPopup != dataManager.withPopup:
				updatePref = True
				dataManager.withPopup = withPopup
				if not withPopup:
					app.setCheckBox(manualConfirmationCheckBox, False)
					dataManager.withManualConfirm = False

			withManualConfirm = app.getCheckBox(manualConfirmationCheckBox)
			if withManualConfirm != dataManager.withManualConfirm:
				updatePref = True
				dataManager.withManualConfirm = withManualConfirm
				if withManualConfirm:
					app.setCheckBox(popupNewTradeCheckBox)
					dataManager.withPopup = True

			if updatePref:
				dataManager.savePreferences()

			history = app.getLabel("history")
			logs = []

			trade = socketManager.getNextTrade()
			if trade is not None:
				countServer[0] = 0
				if trade["side"] == "buy":
					qty = tradingManager.getQty(trade["pair"], trade["price"], trade["bag"])

					confirm = True
					if withManualConfirm and tradingManager.checkBuy(trade["pair"], trade["id"]):
						posQuote = trade["pair"].find("USDT")
						note = "Buy "+str(qty)+" "+trade["pair"][:posQuote]+" at approx "+str(trade["price"])+"$"
						confirm = app.okBox("Trade confirmation", note)

					if confirm:
						log, done = tradingManager.buy(trade["pair"], trade["id"], qty, withBinanceTrading, trade["price"])
						logs += log

						if done and withPopup and not withManualConfirm:
							posQuote = trade["pair"].find("USDT")
							note = "Buy "+str(qty)+" "+trade["pair"][:posQuote]+" at approx "+str(trade["price"])+"$"
							app.setLabel(tradeInfoLabel, note)
							app.showSubWindow("Trade info")




				elif trade["side"] == "tp":

					confirm = True
					qty, checkTp = tradingManager.checkTp(trade["pair"], trade["id"])
					if withManualConfirm and checkTp:
						posQuote = trade["pair"].find("USDT")
						note = "TP "+str(qty)+" "+trade["pair"][:posQuote]+" at approx "+str(trade["price"])+"$"
						confirm = app.okBox("Trade confirmation", note)

					if confirm:
						log, qty = tradingManager.tp(trade["pair"], trade["id"], withBinanceTrading, trade["price"])
						logs += log

						if withPopup and qty > 0. and not withManualConfirm:
							posQuote = trade["pair"].find("USDT")
							note = "TP "+str(qty)+" "+trade["pair"][:posQuote]+" at approx "+str(trade["price"])+"$"
							app.setLabel(tradeInfoLabel, note)
							app.showSubWindow("Trade info")


			logs += tradingManager.updateTrades()
			for log in logs:
				printLog(log)
				history = log + "\n" + history

			app.setLabel("history", history)
		except Exception as e:
			printLog(e)

	app.setPollTime(50)
	app.registerEvent(updateTrade)

	app.go()
	return stop[0]
