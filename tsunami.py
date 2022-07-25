import requests
from datetime import datetime

class Tsunami:

    def __init__(self, contractAddress, myAddress = None, node = 'https://nodes.wavesexplorer.com', usdnAssetId = 'DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p'):
        self.contractAddress = contractAddress
        self.usdnAssetId = usdnAssetId
        self.myAddress = myAddress
        self.node = node
        self.LONG = 1
        self.SHORT = 2

    def calcRemainMarginWithFundingPayment(self, positionSize, positionMargin, positionLstUpdCPF, unrealizedPnl):
        position = requests.post(self.node + '/utils/script/evaluate/' + self.contractAddress, json = { "expr": "calcRemainMarginWithFundingPayment(" + str(positionSize) + ", "  + str(positionMargin) + ", " + str(positionLstUpdCPF) + ", " + str(unrealizedPnl) + ")" }).json()
        positionValues = position['result']['value']

        return { 'remainMargin': positionValues['_1']['value'], 'badDebt': positionValues['_2']['value'] }

    def getPositionNotionalAndUnrealizedPnl(self, address, option = 1):
        position = requests.post(self.node + '/utils/script/evaluate/' + self.contractAddress, json = { "expr": "getPositionNotionalAndUnrealizedPnl(\"" + address + "\", " + str(option) + ")" }).json()
        positionValues = position['result']['value']

        return { 'positionNotional': positionValues['_1']['value'], 'unrealizedPnl': positionValues['_2']['value'] }

    def getPosition(self, address):
        position = requests.post(self.node + '/utils/script/evaluate/' + self.contractAddress, json = { "expr": "getPosition(\"" + address + "\")" }).json()
        positionValues = position['result']['value']

        return { 'positionSize': positionValues['_1']['value'], 'margin': positionValues['_2']['value'], 'pon': positionValues['_3']['value'], 'positionLstUpdCPF': positionValues['_4']['value'] }

    def getPayout(self, address):
        position = self.getPosition(address)
        notionalAndUnrealizedPnl = self.getPositionNotionalAndUnrealizedPnl(address)
        remainMarginWithFundingPayment = self.calcRemainMarginWithFundingPayment(position['positionSize'], position['margin'], position['positionLstUpdCPF'], notionalAndUnrealizedPnl['unrealizedPnl'])

        return remainMarginWithFundingPayment['remainMargin'] / 1000000

    def getTwapSpotPrice(self):
        qtAstR = self.getDataFromContract('k_qtAstR')
        bsAstR = self.getDataFromContract('k_bsAstR')

        return qtAstR / bsAstR

    def getOracleTwapPrice(self):
        oracle = self.getDataFromContract('k_ora')
        priceKey = self.getDataFromContract('k_ora_key')

        return self.getDataFromAddress(oracle, priceKey) / 1000000

    def getShortFundingRate(self):
        marketPrice = self.getTwapSpotPrice()
        indexPrice = self.getOracleTwapPrice()
        if marketPrice > indexPrice:
            direction = 1
        else:
            direction = -1

        return direction * self.getDataFromContract('k_shortFundingRate') / 10000

    def getLongFundingRate(self):
        marketPrice = self.getTwapSpotPrice()
        indexPrice = self.getOracleTwapPrice()
        if marketPrice > indexPrice:
            direction = -1
        else:
            direction = 1

        return direction * self.getDataFromContract('k_longFundingRate') / 10000

    def getTimeToNextFunding(self):
        nextFundingRound = self.getNextFundingTimestamp()
        now = datetime.now()

        return nextFundingRound - now

    def getNextFundingTimestamp(self):
        return self.getDataFromContract('k_nextFundingBlockMinTimestamp')

    def getDataFromContract(self, key):
        return self.getDataFromAddress(self.contractAddress, key)

    def getDataFromAddress(self, address, key):
        return requests.get(self.node + '/addresses/data/' + address + '/' + key).json()['value']

    def liquidate(self, address):
        return self.myAddress.invokeScript(self.contractAddress, 'liquidate', [{'type': 'string', 'value': address}], [])

    def long(self, investment, margin):
        return self.myAddress.invokeScript(self.contractAddress, 'increasePosition', [{'type': 'integer', 'value': self.LONG}, {'type': 'integer', 'value': margin * 1000000}, {'type': 'integer', 'value': int(investment / 4 * 1000)}], [ { "amount": investment * 1000000, "assetId": self.usdnAssetId }])

    def decreaseLong(self, investment, margin):
        return self.myAddress.invokeScript(self.contractAddress, 'decreasePosition', [{'type': 'integer', 'value': self.LONG}, {'type': 'integer', 'value': investment * 1000000 }, {'type': 'integer', 'value': margin * 1000000}, {'type': 'integer', 'value': int(investment / 2 * 1000)}], [ ])

    def short(self, investment, margin):
        return self.myAddress.invokeScript(self.contractAddress, 'increasePosition', [{'type': 'integer', 'value': self.SHORT}, {'type': 'integer', 'value': margin * 1000000}, {'type': 'integer', 'value': int(investment / 4 * 1000)}], [ { "amount": investment * 1000000, "assetId": self.usdnAssetId }])

    def decreaseShort(self, investment, margin):
        return self.myAddress.invokeScript(self.contractAddress, 'decreasePosition', [{'type': 'integer', 'value': self.SHORT}, {'type': 'integer', 'value': investment * 1000000}, {'type': 'integer', 'value': margin * 1000000}, {'type': 'integer', 'value': int(investment / 2 * 1000)}], [ ])

    def closePosition(self):
        return self.myAddress.invokeScript(self.contractAddress, 'closePosition', [], [])
