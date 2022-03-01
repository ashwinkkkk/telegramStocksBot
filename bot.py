import os
import telebot
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from time import sleep
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
# import RPi.GPIO as GPIO


# GPIO.setmode(GPIO.BCM)  # choose BCM mode
# GPIO.setwarnings(False)
# GPIO.setup(18, GPIO.OUT)

url = 'https://finance.yahoo.com/screener/predefined/day_gainers'
alpha_vantage_api_key = '0KT2YEQW5Z673RFL'
API_KEY = '1660885509:AAGzq34hoBjyr_M_HWvcYq26dSwgw8dCQj8'
bot = telebot.TeleBot(API_KEY)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start', 'y'])
def send_welcome(message):
    global chatId
    global name
    print(message)
    name = message.chat.first_name
    response = """


▂▃▅▇█▓▒░۩۞۩ ۩۞۩░▒▓█▇▅▃▂

*Hi {name}, what would you like to do?*
    1. Find top stocks /1
    2. Set upper limit for a stock /2
    3. Set lower limit for a stock /3
    4. Favourite stocks /4
    5. View graph /5

""".format(name=name)
    try:
        with open(name + ".txt", "x") as x:
            print("User file created")
    except FileExistsError:
        print("File exists")
    chatId = message.chat.id
    msg = bot.send_message(message.chat.id, response, parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_start_user_selection)


def process_start_user_selection(message):
    print(f'user selection is {message.text}')
    user_selection = message.text
    if user_selection == "1" or user_selection == "/1":
        data = requests.get(url)
        stock_list = []
        print(f'Data status code is {data.status_code}')
        html_data = BeautifulSoup(data.content, 'html.parser')
        temp = list(html_data.children)[1]
        temp = list(temp.children)[1]
        temp = list(temp.children)[2]
        html = str(list(temp.children)[0])
        stock_list = html[html.find(
            '"pageCategory":"YFINANCE:') + 25:html.find('","fallbackCategory":')].split(',')
        print(stock_list)
        response = """
*Here are the top 5 stocks:*
 =====================
"""
        i = 1
        for stock in stock_list:
            if i < 6:
                response = response + "\t" + \
                    str(i) + ". " + str(stock_list[i - 1])
                i = i + 1
        response = response + "\n\n" + "{Press /y to go back to start.}"
        bot.send_message(message.chat.id, response, parse_mode='Markdown')
    elif user_selection == "2" or user_selection == "/2":
        msg = bot.send_message(
            message.chat.id, "Which stock do you want to set limit for?")
        bot.register_next_step_handler(msg, process_stock)
    elif user_selection == "3" or user_selection == "/3":
        msg = bot.send_message(
            message.chat.id, "Which stock do you want to set limit for?")
        bot.register_next_step_handler(msg, process_stock_lower)
    elif user_selection == "4" or user_selection == "/4":
        msg = bot.send_message(message.chat.id,
                               """Do you want to
    A: Edit your favorite stocks /A
    B: View information about your favorite stocks /B
        """)
        bot.register_next_step_handler(msg, process_favourite_option)
    elif user_selection == "5" or user_selection == "/5":
        msg = bot.send_message(message.chat.id,
                               """Which stock do you want to view graph for?
        """)
        if os.path.exists("stocks2.csv"):
            os.remove("stocks2.csv")
        else:
            print("The file stocks.txt does not exist")
        if os.path.exists("stockpic2.png"):
            os.remove("stockpic2.png")
        bot.register_next_step_handler(msg, process_time_for_graph)


def process_time_for_graph(message):
    print("Here in process time for stock")
    global stockToGraph
    stockToGraph = message.text
    msg = bot.send_message(message.chat.id,
                           """
    Choose start time of graph
    1.  2010  /2010
    2.  2011  /2011
    3.  2012  /2012
    4.  2013  /2013
    5.  2014  /2014
    6.  2015  /2015
    7.  2016  /2016
    8.  2017  /2017
    9.  2018  /2018
    10. 2019  /2019
    11. 2020  /2020
    12. 2021  /2021
    13. Yesterday /yesterday
    """)
    bot.register_next_step_handler(msg, process_stock_to_get_graph_for)


def process_stock_to_get_graph_for(message):

    print("Here in processing graph")
    userTimeSelection = message.text
    style.use('ggplot')
    print("stock to graph is ", stockToGraph)

    url = 'https://finance.yahoo.com/screener/predefined/day_gainers'
    if (userTimeSelection == "/2010"):
        start = dt.datetime(2010, 1, 1)
    elif (userTimeSelection == "/2011"):
        start = dt.datetime(2011, 1, 1)
    elif (userTimeSelection == "/2012"):
        start = dt.datetime(2012, 1, 1)
    elif (userTimeSelection == "/2013"):
        start = dt.datetime(2013, 1, 1)
    elif (userTimeSelection == "/2014"):
        start = dt.datetime(2014, 1, 1)
    elif (userTimeSelection == "/2015"):
        start = dt.datetime(2015, 1, 1)
    elif (userTimeSelection == "/2016"):
        start = dt.datetime(2016, 1, 1)
    elif (userTimeSelection == "/2017"):
        start = dt.datetime(2017, 1, 1)
    elif (userTimeSelection == "/2018"):
        start = dt.datetime(2018, 1, 1)
    elif (userTimeSelection == "/2019"):
        start = dt.datetime(2019, 1, 1)
    elif (userTimeSelection == "/2020"):
        start = dt.datetime(2020, 1, 1)
    elif (userTimeSelection == "/2021"):
        start = dt.datetime(2021, 1, 1)
    elif (userTimeSelection == "/yesterday"):
        start = dt.datetime(2021, 8, 18)
    end = dt.datetime(2021, 8, 19)

    df = web.DataReader(stockToGraph, 'yahoo', start, end)
    df.to_csv('stocks.csv')
    sleep(1)
    df = pd.read_csv('stocks.csv', parse_dates=True, index_col=0)
    df['Open'].plot()
    plt.savefig('stockpic.png')
    os.rename(r'./stocks.csv', r'./stocks2.csv')
    bot.send_photo(message.chat.id, photo=open(
        "./stockpic.png", "rb"), caption=f"Graph for {stockToGraph} \n /y")
    os.rename(r'./stockpic.png', r'./stockpic2.png')
    plt.clf()
    plt.cla()
    plt.close()


def process_stock(message):
    global stockToSetLimitFor
    print("Here in processing stock")
    stockToSetLimitFor = message.text
    msg = bot.send_message(message.chat.id, """
Set stock limit
""")
    bot.register_next_step_handler(msg, process_stock_limit)


def process_stock_limit(message):
    global stock_limit
    stock_limit = message.text
    print(stock_limit)
    msg = bot.send_message(message.chat.id, """
Do you want to enable buzzer? (yes or no)
""")
    bot.register_next_step_handler(msg, process_buzzer_and_start_analysing)


def process_buzzer_and_start_analysing(message):
    global buzzerEnabled
    buzzerEnabled = message.text
    print(buzzerEnabled)
    end = 0
    while(end == 0):
        ts = TimeSeries(key=alpha_vantage_api_key, output_format='pandas')
        data, meta_data = ts.get_intraday(
            symbol=stockToSetLimitFor, interval='1min', outputsize='full')
        print(data)

        close_data = data['4. close']
        print("close data is ", close_data)
        print("**************")
        last_close_data = close_data[0]
        print("Last close data is ", last_close_data)
        print("Limit is ", stock_limit)
        if(int(last_close_data) < int(stock_limit)):
            # if(buzzerEnabled == 'yes' or buzzerEnabled == 'Yes'):
            #     GPIO.output(18, 1)
            #     sleep(1)
            # GPIO.output(18, 0)
            print("gone below limit")
            response = f'*Hi {name} the last stock price for {stockToSetLimitFor} was {last_close_data} and it has gone below your limit of {stock_limit}*\n\n[press /y to go back to start]'
            msg = bot.send_message(
                message.chat.id, response, parse_mode='Markdown')
            end = 1
        sleep(60)


def process_favourite_option(message):
    optionAtFavStocks = message.text
    if(optionAtFavStocks == "a" or optionAtFavStocks == "A" or optionAtFavStocks == "/A"):
        print("Here in optionAtFavStocks a")
        resp = """
Hello {name} what do you want to
    A: Add new stock /A
    B: Delete my list of favorite stocks /B
    C: Add new list of stocks /C
""".format(name=name)

        msg = bot.send_message(message.chat.id, resp)
        bot.register_next_step_handler(msg, process_edit_stock_option)

    elif(optionAtFavStocks == "b" or optionAtFavStocks == "B" or optionAtFavStocks == "/B"):
        with open(name + '.txt') as r:
            listOfStocks = list(r)
        if listOfStocks != []:
            loading = """
            Loading…█▒▒▒▒▒▒▒▒▒
            """
            msg = bot.send_message(message.chat.id, loading,
                                   parse_mode='Markdown')
            print("Here in optionAtFavStocks b")
            with open(name + '.txt') as r:
                listOfStocks = list(r)
            print(listOfStocks)
            symbolList = []
            for i in listOfStocks:
                symbolList.append(i.replace("\n", ""))
            print(symbolList)
            response = "*Stock*     *Last close*"
            for stock in symbolList:
                ts = TimeSeries(key=alpha_vantage_api_key,
                                output_format='pandas')
                data, meta_data = ts.get_intraday(
                    symbol=stock, interval='1min', outputsize='full')
                print(data)

                close_data = data['4. close']
                print("close data is ", close_data)
                print("**************")
                last_close_data = close_data[0]
                print("close data", close_data)
                print("Last close data is ", last_close_data)
                response = response + f"\n" + \
                    str(stock) + "      " + str(last_close_data)

            msg = bot.send_message(message.chat.id, response,
                                   parse_mode='Markdown')
        else:
            msg = bot.send_message(
                message.chat.id, "You have no favorite stocks")


def process_edit_stock_option(message):
    whichEdit = message.text
    if(whichEdit == "b" or whichEdit == "B" or whichEdit == "/B"):
        file = open(name + ".txt", "w")
        file.close()
        response = f"*ALL FAVORITE STOCKS OF {name} DELETED*"
        msg = bot.send_message(message.chat.id, response,
                               parse_mode='Markdown')
    elif(whichEdit == "a" or whichEdit == "A" or whichEdit == "/A"):
        response = "*What stock do you want to add to your favorites?*"
        msg = bot.send_message(message.chat.id, response,
                               parse_mode='Markdown')
        bot.register_next_step_handler(msg, process_add_stock_to_database)
    elif(whichEdit == "c" or whichEdit == "C" or whichEdit == "/C"):
        response = "Type your list of stocks seperated by a comma"
        msg = bot.send_message(message.chat.id, response)
        bot.register_next_step_handler(
            msg, process_add_list_of_stock_to_database)


def process_add_stock_to_database(message):
    stock = message.text
    with open(name + ".txt", "a+") as f:
        f.write(stock)
        f.write("\n")
    reply = f"{stock} was added to your list of favorite stocks!"
    msg = bot.send_message(message.chat.id, reply)


def process_add_list_of_stock_to_database(message):
    stockList = message.text.split(",")
    print(stockList)
    with open(name + ".txt", "w") as f:
        for stock in stockList:
            f.write(stock)
            f.write("\n")


def process_stock_lower(message):
    global stockToSetLimitFor
    print("Here in processing stock")
    stockToSetLimitFor = message.text
    msg = bot.send_message(message.chat.id, """
Set stock limit
""")
    bot.register_next_step_handler(msg, process_stock_limit_lower)


def process_stock_limit_lower(message):
    global stock_limit
    stock_limit = message.text
    print(stock_limit)
    msg = bot.send_message(message.chat.id, """
Do you want to enable buzzer? (yes or no)
""")
    bot.register_next_step_handler(
        msg, process_buzzer_and_start_analysing_lower)


def process_buzzer_and_start_analysing_lower(message):
    global buzzerEnabled
    buzzerEnabled = message.text
    print(buzzerEnabled)
    end = 0
    while(end == 0):
        ts = TimeSeries(key=alpha_vantage_api_key, output_format='pandas')
        data, meta_data = ts.get_intraday(
            symbol=stockToSetLimitFor, interval='1min', outputsize='full')
        print(data)

        close_data = data['4. close']
        print("close data is ", close_data)
        print("**************")
        last_close_data = close_data[0]
        print("Last close data is ", last_close_data)
        print("Limit is ", stock_limit)
        if(int(last_close_data) > int(stock_limit)):
            # if(buzzerEnabled == 'yes' or buzzerEnabled == 'Yes'):
            #     GPIO.output(18, 1)
            #     sleep(1)
            # GPIO.output(18, 0)
            print("gone above limit")
            response = f'*Hi {name} the last stock price for {stockToSetLimitFor} was {last_close_data} and it has gone above your limit of {stock_limit}*\n\n[press /y to go back to start]'
            msg = bot.send_message(
                message.chat.id, response, parse_mode='Markdown')
            end = 1
        sleep(60)


bot.polling()
