import requests
import os
from sys import platform
from time import sleep
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY")
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

print(API_KEY)
bitcoinPrice = ''
operatingSys = platform
biggerThanNotif = False

# Parameters for the request
# Parameters can be found here:
# https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyMap
parameters = {
    'id': '1'  # ID 1 is for bitcoin
}

# Headers for the request (including API key)
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}
def Fetch_Bitcoin_Price():
    try:
        # Makes the request to coinmarketcap.com's API
        response = requests.get(URL, headers=headers, params=parameters)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Extract Bitcoin price in USD
        # Supported languages can be found here:
        # https://coinmarketcap.com/api/documentation/v1/#section/Standards-and-Conventions
        bitcoinPrice = data['data']['1']['quote']['USD']['price']
        return bitcoinPrice

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def Make_Notafication(price):
    title = "Bitcoin Notifier"
    notaficationCmd = ""
    if (platform == "darwin"):
        notaficationCmd = f'''
        osascript -e 'display notification "bitcoin is now at {price:.2f}"'
        '''
    elif (platform == "linux"):
        notaficationCmd = f'''
        notify-send "{title}" "bitcoin is now at {price:.2f}"
        '''
    elif (platform == "win32"):
        # if you want a notafications for windows then you can use win10toast
        # and uncomment this:
        """
        toast.show_toast(
        "Notification",
        "Notification body",
        duration = 20,
        icon_path = "icon.ico",
        threaded = True,
        )
        """
        return
    os.system(notaficationCmd)

if __name__ == "__main__":
    print("python notifier")

    bitcoinPrice = Fetch_Bitcoin_Price()
    Make_Notafication(bitcoinPrice)

    while True:
        if(bitcoinPrice != None):
            break
        else:
            print("Failed to fetch bitcoin price")
            sleep(10)
            pass
    
    print(f"Current price of bitcoin: ${bitcoinPrice:.2f}")
    notifyWhen = float(input("at what ammount would you like to get notified when BTC reaches? "))

    if (bitcoinPrice > notifyWhen):
        biggerThanNotif = True
        print("the program will now notify you when it reaches that number")
    elif (bitcoinPrice < notifyWhen):
        biggerThanNotif = False
        print("the program will now notify you when it reaches that number")
    else:
        print("You can not enter a number that is equal to bitcoin price")
    
    print(f"the program will refresh the price every hour")
    while True:
        sleep(3600)
        bitcoinPrice = Fetch_Bitcoin_Price()

        if bitcoinPrice != None:
            if biggerThanNotif == True and bitcoinPrice <= notifyWhen:
                Make_Notafication(bitcoinPrice)
            elif biggerThanNotif == False and bitcoinPrice >= notifyWhen:
                Make_Notafication(bitcoinPrice)
        else:
            print("Failed to fetch bitcoin Price")

