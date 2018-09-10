#import modules
import pandas as pd
import os
import time
from datetime import datetime
from time import mktime

import matplotlib
import matplotlib.pyplot as plt

from matplotlib import style
style.use("dark_background")

import re

#path for data files
path = "C:/Users/Bruno/Desktop/Robot/intraQuarter"

#stat you are trying to gather in the database
#KeyStats is the name of a folder and 
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    #Prepare information on Pandas, creating columns
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 'Status'])

    ticker_list = []

    #Include S&P 500 data downloaded to data frame
    sp500_df = pd.DataFrame.from_csv("SP500.csv")



    #get the file names
    #set the number of stocks 1:x
    for each_dir in stock_list[1:]:
       #Finding the ticker
        ticker = each_dir.split("\\")[1]
        each_file = os.listdir(each_dir)
        ticker_list.append(ticker)

        #Set starting points, so that % change doens't begin with n/a
        starting_stock_value = False
        starting_sp500_value = False


        
        if len(each_file) > 0:
            for file in each_file:

                #Date syntax of the HTML file from Yahoo! Finance. This sets up the info type we want
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                full_file_path = each_dir+'/'+file

                #The source can be a HTML website
                source = open(full_file_path,'r').read()
                try:
                    #Excluding a HTML code that came before the data in the website
                    #The [1] means that we get everything to the right of the code
                    #The [0] stops gathering info after it
                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    except:
                        value = float(source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0])

                    #Exclude weekends from S&P 500 data
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                   #259200 are seconds for t-3 to jump weekends and holidays
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                    #Get stock price from Y! Finance website
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except:
                        
                        #Search for "d" digits, with (1 and 8) in length
                        #   <span id="yfs_110_afl">43.27</span>
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            #print(stock_price)

                        except:

                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                #print(stock_price)

                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                
                                stock_price = float(stock_price.group(1))
                                #print(stock_price)

                            except:

                                print('wtf stock price lol',ticker,file, value)
                                time.sleep(5)


                    #Set starting points (again), so that % change doens't begin with n/a
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                        
                    if not starting_sp500_value:
                       starting_sp500_value = sp500_value 

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    location = len(df['Date'])

                    difference = stock_p_change-sp500_p_change
                    
                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    
                    #Connecting pandas to the information stamps
                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':difference,
                                    'Status':status},
                                   ignore_index = True)

                    #Pass, that is, ignore info that is not available
                except Exception as e:
                    pass
                    
                    
    #Plot each stock on the graph, with a beta indicator
    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])


            if plot_df['Status'][-1] == 'underperform':
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label=each_ticker, color=color)

            plt.legend()

        except Exception as e:
            print(str(e))

   plt.show()
          
    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)


Key_Stats()
