# PyTsunami
A simple python library for interacting with the Tsunami Exchange
## Available methods
- calcRemainMarginWithFundingPayment(positionSize, positionMargin, positionLstUpdCPF, unrealizedPnl) - Calculation of the remaining maring including funding payments
- getPositionNotionalAndUnrealizedPnl(address)- Calculation of the positions notional and unrealized Pnl
- getPosition(address) - Getting the position of a given address
- getPayout(address) - Getting the payout for a given address
- getTwapSpotPrice() - Getting the price of the pair on the Tsunami Exchange
- getOracleTwapPrice() - Getting the oracle price of the pair
- getFundingRate() - Calculating the current funding rate
- getTimeToNextFunding() - Calculating the time till next funding payments
- getNextFundingTimestamp() - Getting the timestamp of the next funding payments
- getDataFromContract(key) - Getting data entries from the contract (mainly used internally)
- getDataFromAddress(address, key) - Getting all datas from the contract (mostly used internally)
- liquidate(address) - Liquidate a given address
- long(investment, margin) - Going long on the defined trading pair with the presented amount (investment) and presented margin
- decreaseLong(investment, margin) - Decreasing a position by the given amount (investment) and presented margin
- short(investment, margin) - Going short on the defined trading pair with the presented amount (investment) and presented margin
- decreaseShort(investment, margin) - Increasing a position by the given amount (investment) and presented margin
- closePosition() - Closing the position of the current address
## Examples
Instantiation of the class for testnet:
```python
from tsunami import Tsunami
import pywaves as pw

# configure a testnet node
node = 'https://nodes-testnet.wavesnodes.com'
# asset id of USDN on testnet
usdnAssetId = 'HezsdQuRDtzksAYUy97gfhKy7Z1NW2uXYSHA3bgqenNZ'
# create an address, especially necessary if you want to go long or short
pw.setNode(node, 'T')
myAddress = pw.Address(seed='this is just a test seed')
# configure the address for the Tsunami market you want to interact with, e.g. the WAVES/USDN market
tsunamiContractAddress = '3N4mv2c2ehFvfSR5pXDCUqFZDaatagfBaMA'

tsunami = Tsunami(tsunamiContractAddress, myAddress = myAddress, node = node, usdnAssetId = usdnAssetId)
```
## Interacting with Tsunami markets
Once you have created an instance of the Tsunami class, you can use it to get information about the market by calling the corresponding methods.
```python
tsunami.getTwapSpotPrice()
```