
"""
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribution:
 *      
 *      Santiago Bobadilla (s.bobadilla@uniandes.edu.co)
 *      Daniel Zea (d.zea@uniandes.edu.co)
 *      Juan A. Jaramillo (ja.jaramillop@uniandes.edu.co)
 *      Andrés F. Vergara (af.vergarar@uniandes.edu.co)
 *
 """

import os
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from pandas_datareader import data


# ___________________________________________________
#  Load table with CSV information
#  - Pre define path = Same folder
#  - Charge stock Adj Close Price
#  - Charge stock Adj Close Log Returns
# ___________________________________________________


def define_path_mps(file):
    '''
    Length(Stock_info.py) = 13. The function gets the absolute path to this file and then modifies it
    to access 'Portafolio.csv' which is saved in the same directory as the current file.
    Modifying this file's name, i.e. 'Stock_info.py', will require you to change [:-13]
    for the new file's name lenght.
    '''

    absolute_path = os.path.abspath(__file__)[:-13]
    separador = absolute_path[-1]

    return(absolute_path.replace(separador, '/') + file + ".csv")

def get_info(csv_separator):
    '''
    Reads assets info from a csv file named Portafolio into a pandas dataframe object.
    It assumes the information being read contains the logarithmic returns of the desired assets.
    '''
    path = define_path_mps('Portafolio')
    return pd.read_csv(path, sep = csv_separator,index_col = 0)

def get_log_info(csv_separator):
    '''
    Reads assets info form a csv file named Portafolio into a pandas dataframe object.
    It assumes the information being read contains the prices of the desired assets.
    '''

    path = define_path_mps('Portafolio')
    df =  pd.read_csv(path, sep = csv_separator,index_col = 0)

    df = np.log(df).diff()
    df = df.dropna()

    return df

# ___________________________________________________
#  Automatic API, and additional information
# ___________________________________________________

# ... Additional Information: https://nicobesser.medium.com/stocks-data-from-investing-in-python-ce2c7c1135d7

def YahooData(dataframe,assets_list,start_date,end_date):
    for i in assets_list:
        dataframe[i] = data.DataReader(i,data_source='yahoo',start=start_date , end=end_date)["Adj Close"]
    return dataframe

# If boolean retrive_csv_info is false
def stock_info (assets, momentum):
    '''
    Imports the information on the assets prices for the last 'momentum' days from Yahoo into a pandas dataframe and immediately
    Calculates logarithmic returns. All NA values are dropped.
    '''

    start = (datetime.today() - timedelta(days = momentum)).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')
    df_prices = pd.DataFrame()
    print("FROM:",start)
    print("TO:",today)

    df = YahooData(df_prices,assets,start,today)

    print("IMPORTED PRICES:\n----------------------------------------------\n")
    print(df.head(5),"\n...", df.tail(5))
    print("\n----------------------------------------------\n")

    df = np.log(df).diff() #diff() y dropna() porque no son intepretados por intellisense???

    df = df.dropna()

    print("CALCULATED LOGARITHMIC RETURNS:\n----------------------------------------------\n")
    print(df.head(5),"\n...", df.tail(5))
    print("\n----------------------------------------------\n")

    return df

def PreciosSpot(assets, momentum):
    
    today = datetime.today().strftime('%Y-%m-%d')
    df_prices = pd.DataFrame()
    df = YahooData(df_prices,assets,today,today)

    return df
