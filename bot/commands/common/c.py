import hmac
import hashlib
import time
import urllib.parse

import requests

import settings
from bot.commands import (
    AdminBaseCommand,
)


C_URL = 'https://api.blockcypher.com/v1/{}/main/addrs/{}/balance?limit=0'


class CCommand(AdminBaseCommand):

    _COMMAND = 'cc'

    @staticmethod
    def get_currencies_rate():
        rates = requests.get('https://poloniex.com/public?command=returnTicker').json()
        result = []

        parameters = (
            ('btc', 'eth'),
            (settings.B, settings.E),
            (100000000, 1e+18)
        )

        for token, addresses, coefficient in zip(*parameters):
            amount = 0
            rate = 0
            for address in addresses:
                data = requests.get(C_URL.format(token, address)).json()
                rate = float(rates[f'USDT_{token.upper()}']['low24hr'])
                amount += data['final_balance'] / coefficient
            result.append({
                'name': token.upper(),
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
