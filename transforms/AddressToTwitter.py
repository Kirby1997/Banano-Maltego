from maltego_trx.entities import TwitterList
from maltego_trx.transform import DiscoverableTransform
import requests
import os
import time

class AddressToTwitter(DiscoverableTransform):
    """
    Lookup the address and return a tipbot account.
    """

    @classmethod
    def create_entities(cls, request, response):
        account = request.Value

        try:
            name = cls.get_twitter(account)
            if name:
                response.addEntity(TwitterList, name)
                response.addUIMessage("BEEPBOOP")

        except IOError:
            print(IOError)


    @staticmethod
    def get_twitter(address):

        try:
            modi = os.path.getmtime("twitter.txt")
            curr = time.time()
            if curr - modi > 10 * 24 * 60 * 60:  # If file hasn't been updated in 10 days
                API = "https://ba.nanotipbot.com/users/twitter"
                resp = requests.get(API)
                with open("twitter.txt", "w", encoding="utf-8") as file:
                    file.write(resp.text)

        except Exception:
            API = "https://ba.nanotipbot.com/users/twitter"
            resp = requests.get(API)
            with open("twitter.txt", "w", encoding="utf-8") as file:
                file.write(resp.text)

        with open("twitter.txt", "r", encoding="utf-8") as f:
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
    print(AddressToTwitter.get_twitter("ban_3xfwyej3i6ahjpmbozdmz78xjmxouomukyfcne834wgjpxwkpsc4amd17u87"))