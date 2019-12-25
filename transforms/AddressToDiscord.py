from maltego_trx.entities import Alias
from maltego_trx.transform import DiscoverableTransform
import requests

class AddressToDiscord(DiscoverableTransform):
    """
    Lookup the address and return a tipbot account.
    """

    @classmethod
    def create_entities(cls, request, response):
        account = request.Value

        try:
            name = cls.get_discord(account)
            if name:
                response.addEntity(Alias, name)
                response.addUIMessage("BEEPBOOP")

        except IOError:
            print(IOError)


    @staticmethod
    def get_discord(account):
        UFW_API = 'https://bananobotapi.banano.cc/ufw/'
        try:
            resp = requests.get(UFW_API + account)
            jsonResp = resp.json()
            for i in jsonResp:
                name = i['user_last_known_name']
            return name
        except BaseException:
            return None

if __name__ == "__main__":
    print(AddressToDiscord.get_discord("ban_3i63uiiq46p1yzcm6yg81khts4xmdz9nyzw7mdhggxdtq8mif8scg1q71gfy"))