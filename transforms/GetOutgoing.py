from maltego_trx.entities import Person
from maltego_trx import *
from maltego_trx.maltego import MaltegoEntity
from maltego_trx.transform import DiscoverableTransform
import requests


class GetOutgoing(DiscoverableTransform):
    """
    Lookup the address and return its balance.
    """

    @classmethod
    def create_entities(cls, request, response):
        account = request.Value

        try:
            totals = cls.get_outgoing(account)
            if totals:
                for address in totals:

                    entity = response.addEntity(Person, address)

                    entity.setLinkLabel(totals[address])
                    entity.setLinkColor("3")
                    entity.setType("Banano Address")
                    entity.addProperty(fieldName="Cryptocurrency Address", displayName="Cryptocurrency Address", value=address)

        except IOError:
            print(IOError)


    @staticmethod
    def get_outgoing(account):
        API = 'http://45.32.180.42:7072'
        totals = {}
        try:
            resp = requests.post(API, json={"action": "account_history", "account": account, "count": "100000"})
            jsonResp = resp.json()
            history = jsonResp['history']

            for transaction in history:
                amount = int(transaction['amount']) / 10 ** 29
                destination = transaction['account']
                if destination not in totals:
                    # List is received, sent, Discord name, Twitter name, Telegram name, Exchange
                    totals[destination] = [0]

                if transaction['type'] == "send":
                    totals[destination][0] = totals[destination][0] + int(amount)

            return totals
        except Exception:
            print(Exception)
            return None

if __name__ == "__main__":
    print(GetOutgoing.get_outgoing("ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy"))