import logging
import bitso
import os


# Global variables
API_KEY_BITSO = os.environ.get('API_KEY_BITSO')
API_SECRET_BITSO = os.environ.get('API_SECRET_BITSO')
USDC_CONTACT_ID = os.environ.get('USDC_CONTACT_ID')
MIN_USDC_AMOUNT = 10


# Initial config
bitsoApi = bitso.Api(timeout=None, key=API_KEY_BITSO, secret=API_SECRET_BITSO)
logging.basicConfig(level=logging.INFO, format="%(asctime)s;%(name)s;%(levelname)s;%(message)s")


def getUsdBalanceBitso():
  return float(bitsoApi.balances().usd.available)


def withdrawUSDCToBinance():
  usdBalance = int(getUsdBalanceBitso())
  logging.info("Bitso balance: {:.4f} USDC".format(usdBalance))
  
  if usdBalance > MIN_USDC_AMOUNT:
    result = bitsoApi.crypto_withdrawals(usdBalance, USDC_CONTACT_ID)
    logging.debug("Withdraw result:{}".format(result))
    if result is not None and result.amount is not None:
      logging.info("Withdrawn: {:.4f} USDC".format(result.amount))
    else:
      logging.info("Withdrawal failed")


if __name__ == '__main__':
  withdrawUSDCToBinance()
