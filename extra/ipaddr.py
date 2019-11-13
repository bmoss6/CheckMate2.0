#! /usr/bin/python

# hacky script that will give you the IP address of the PI once configured to a wifi access point
# You will need to set up a slack bot and give it the correct API key
# This link is probably how you set up a bot but I didn't test it
## https://slack.com/help/articles/115005265703-create-a-bot-for-your-workspace

from slackclient import SlackClient
import netifaces as ni
import os
import time

tries = 0
while True:
    if (tries > 60):
        exit()
    try:
        sc = SlackClient("Your API KEY") # Replace this with your api key from the bot you configured

        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        ip = ip.encode('ascii')

        message = "Rasberry Pi booted ipaddress "+ip

        print message

        sc.api_call(
                "chat.postMessage",
                channel="#random",
                text=message
                )
        break
    except Exception as e:
        tries = tries + 1
        time.sleep(1)
