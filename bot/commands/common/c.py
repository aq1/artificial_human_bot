import hmac
import hashlib
import time
import urllib.parse

import requests

import settings
from bot.commands import (
    AdminBaseCommand,
)


BTC_URL = 'https://api.blockcypher.com/v1/btc/main/addrs/{}/balance'
ETH_URL = ''
XMR_URL = ''


class CCommand(AdminBaseCommand):

    _COMMAND = 'cc'

    @staticmethod
    def get_currencies_rate():
        post_data = urllib.parse.urlencode({
            'command': 'returnAvailableAccountBalances',
            'nonce': int(time.time() * 1000)
        }).encode('utf-8')
        sign = hmac.new(settings.POLONIEX_SECRET.encode('utf8'), post_data, hashlib.sha512).hexdigest()
        response = requests.post(
            'https://poloniex.com/tradingApi',
            data=post_data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': settings.POLONIEX_KEY,
                'Sign': sign,
            }
        )

        rates = requests.get('https://poloniex.com/public?command=returnTicker').json()
        data = response.json()
        result = []
        for currency_name, currency_amount in data.get('exchange', {}).items():
            currency_amount = round(float(currency_amount), 8)
            try:
                rate = float(rates['USDT_{}'.format(currency_name)].get('highestBid'))
            except KeyError:
                rate = 0
            result.append({
                'name': currency_name,
                'amount': currency_amount,
                'rate': rate,
                'amount_usdt': currency_amount * rate,
            })

        btc_data = requests.get(BTC_URL.format(settings.B)).json()
        rate = float(rates['USDT_BTC']['highestBid'])
        amount = btc_data['final_balance'] / 100000000
        result.append({
            'name': 'BTC',
            'amount': amount,
            'rate': rate,
            'amount_usdt': amount * rate,
        })

        return sorted(result, key=lambda val: val['name'])

    @property
    def success_message(self):
        currencies = self.get_currencies_rate()
        text = (
            '*{name}*\n1 *{name}* = {rate:.2f} USDT\n'
            'You have {amount:.5f} {name} or *{amount_usdt:.2f} USDT*'
        )
        return '\n'.join([
            text.format(**currency)
            for currency in currencies
            if currency['amount_usdt'] > 0.5
        ])
