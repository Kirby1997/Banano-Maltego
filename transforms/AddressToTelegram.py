from maltego_trx.entities import Alias
from maltego_trx.transform import DiscoverableTransform
import requests
import os
import time

class AddressToTelegram(DiscoverableTransform):
    """
    Lookup the address and return a tipbot account.
    """

    @classmethod
    def create_entities(cls, request, response):
        account = request.Value

        try:
            name = cls.get_telegram(account)
            if name:
                response.addEntity(Alias, name)

        except IOError:
            print(IOError)


    @staticmethod
    def get_telegram(address):

        try:
            modi = os.path.getmtime("telegram.txt")
            curr = time.time()
            if curr - modi > 10 * 24 * 60 * 60:  # If file hasn't been updated in 10 days
                API = "https://ba.nanotipbot.com/users/telegram"
                resp = requests.get(API)
                with open("telegram.txt", "w", encoding="utf-8") as file:
                    file.write(resp.text)

        except Exception:
            API = "https://ba.nanotipbot.com/users/telegram"
            resp = requests.get(API)
            with open("telegram.txt", "w", encoding="utf-8") as file:
                file.write(resp.text)

        with open("telegram.txt", "r", encoding="utf-8") as f:
            telegram = f.read()
        telegram = telegram.strip("((")
        telegram = telegram.strip("))")
        pairs = {}
        for account in telegram.split("), ("):
            account = account.split(", ")
            account[1] = account[1].strip("\'")
            account[2] = account[2].strip("\'")
            pairs[account[2]] = account[1]  # + " - " + account[0]

        for entry in pairs:
            if entry == address:
                name = pairs[entry]
                return name
        return None



if __name__ == "__main__":
    print(AddressToTelegram.get_telegram("ban_33nhg1yrzfpw7rgz6iemhn4em3qnbxj11j7s75co7oimsx7ewszwqofo5ng5"))