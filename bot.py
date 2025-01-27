from _secret import TOKEN, CHANNEL_ID_MAIN, CHANNEL_ID_TEST
import telebot
import json
import time
import subprocess
from datetime import datetime

bot = telebot.TeleBot(TOKEN)

# configure shell commands
vnstat_script = 'vnstat -i eth0 --json > vnstat.txt'
speed_test_cli_script = 'speedtest-cli --secure --json > speed_test_cli.txt'

while True:
    # run commands
    subprocess.run(vnstat_script, shell=True, check=False, text=True, capture_output=True)
    subprocess.run(speed_test_cli_script, shell=True, check=False, text=True, capture_output=True)

    # load vnstat results
    vnstat_file = open('vnstat.txt')
    vnstat_json = json.load(vnstat_file)
    vnstat_file.close()

    # load speed test results
    speed_test_cli_file = open('speed_test_cli.txt')
    speed_test_cli_json = json.load(speed_test_cli_file)
    speed_test_cli_file.close()

    # get connection speed
    server_name = f"{speed_test_cli_json['server']['name']}"
    server_country = f"{speed_test_cli_json['server']['country']}"
    server_sponsor = f"{speed_test_cli_json['server']['sponsor']}"
    upload_speed = f"{speed_test_cli_json['upload'] / 2 ** 20:.2f}"
    download_speed = f"{speed_test_cli_json['download'] / 2 ** 20:.2f}"

    # get date of traffic stats
    unix_time = int(vnstat_json['interfaces'][0]['updated']['timestamp'] + 7200 + 3600)  # why???? fix it later...
    updated_time = datetime.fromtimestamp(unix_time).strftime('%H:%M %d-%m-%Y')

    # get traffic stats
    received_traff_total = f"{int(vnstat_json['interfaces'][0]['traffic']['total']['rx']) / 2 ** 30:.1f}"
    sent_traff_total = f"{int(vnstat_json['interfaces'][0]['traffic']['total']['tx']) / 2 ** 30:.1f}"
    received_traff_month = f"{int(vnstat_json['interfaces'][0]['traffic']['month'][-1]['rx']) / 2 ** 30:.1f}"
    sent_traff_month = f"{int(vnstat_json['interfaces'][0]['traffic']['month'][-1]['tx']) / 2 ** 30:.1f}"
    received_traff_day = f"{int(vnstat_json['interfaces'][0]['traffic']['day'][-1]['rx']) / 2 ** 30:.1f}"
    sent_traff_day = f"{int(vnstat_json['interfaces'][0]['traffic']['day'][-1]['tx']) / 2 ** 30:.1f}"
    received_traff_hour = f"{int(vnstat_json['interfaces'][0]['traffic']['hour'][-1]['rx']) / 2 ** 20:.1f}"
    sent_traff_hour = f"{int(vnstat_json['interfaces'][0]['traffic']['hour'][-1]['tx']) / 2 ** 20:.1f}"
    received_traff_fiveminute = f"{int(vnstat_json['interfaces'][0]['traffic']['fiveminute'][-1]['rx']) / 2 ** 20:.1f}"
    sent_traff_fiveminute = f"{int(vnstat_json['interfaces'][0]['traffic']['fiveminute'][-1]['tx']) / 2 ** 20:.1f}"

    # create message
    message = (f"🗓️ {updated_time}\n"
               f"     ⏳ Connection speed ({server_name}/{server_sponsor}):\n"
               f"          ⬆️ Upload - {upload_speed} MB/s\n"
               f"          ⬇️ Download - {download_speed} MB/s\n"
               f"     🚦 Traffic:\n"
               f"          📊 Last five minutes:\n"
               f"               ⬆️ Sent - {received_traff_fiveminute} MB\n"
               f"               ⬇️ Received - {received_traff_fiveminute} MB\n"
               f"          📊 Last hour:\n"
               f"               ⬆️ Sent - {sent_traff_hour} MB\n"
               f"               ⬇️ Received - {received_traff_hour} MB\n"
               f"          📊 Last day:\n"
               f"               ⬆️ Sent - {sent_traff_day} GB\n"
               f"               ⬇️ Received - {received_traff_day} GB\n"
               f"          📊 Last month:\n"
               f"               ⬆️ Sent - {sent_traff_month} GB\n"
               f"               ⬇️ Received - {received_traff_month} GB\n"
               f"          📊 All time:\n"
               f"               ⬆️ Sent - {sent_traff_total} GB\n"
               f"               ⬇️ Received - {received_traff_total} GB")

    # send message
    bot.send_message(CHANNEL_ID_MAIN, message)

    # sleep after message
    time.sleep(30 * 60)
