from maltego_trx.entities import Phrase
from maltego_trx.transform import DiscoverableTransform
import requests


class GetBalance(DiscoverableTransform):
    """
    Lookup the address and return its balance.
    """

    @classmethod
    def create_entities(cls, request, response):
        account = request.Value

        try:
            balance = cls.get_balance(account)
            if balance:
                response.addEntity(Phrase, "Balance: " + balance)


        except IOError:
            print(IOError)


    @staticmethod
    def get_balance(account):
        API = 'http://45.32.180.42:7072'
        try:
            resp = requests.post(API, json={"action": "account_balance", "account": account})
            jsonResp = resp.json()
            balance = jsonResp['balance']
            balance = int(balance)/10**29
            return '%.2f'%balance
        except Exception:
            print(Exception)
            return None

if __name__ == "__main__":
    print(GetBalance.get_balance("ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy"))