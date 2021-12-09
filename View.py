
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

import sys
import timeit
import Controller
import numpy as np
from gurobipy import GRB
import pandas as pd
import Stock_Info as stocks
import matplotlib.pyplot as plt
from arch import arch_model



# ___________________________________________________
#  Variables and stock info retrieval
# ___________________________________________________

# -------> Stock Information

# ... Auxiliary variables to specify how the data should be loaded to the program. 
# see Controller.init() for more infomation.

calc_log_return = False
retrive_csv_info = False

# ... Automatic API
momentum_days=2*365
assets = []

# Optimizer parameters.

expected_return = None
min_bound = None
max_bound = None

# ___________________________________________________
#  Principal Menu and interaction with the user.
# ___________________________________________________

def GBM (miu,sigma,pesos): 

    num_dias=int(input("Cuantos años desea simular: "))*252
    lista=[]
    miu=miu+0.5*pow(sigma,2)
    simulacion=np.zeros((100,num_dias))
    asset=stocks.PreciosSpot(assets)
    for i in range(len(assets)):
        lista.append( asset.iat[0,i])
    s0=(np.dot(lista,pesos))
    dt=1/num_dias
    
    simulacion[:,0]=s0
    e=np.zeros((100,num_dias))
    for i in range(100):
        for j in range(num_dias):
            e[i][j]=np.random.standard_normal()
    for i in range(1,num_dias):
        simulacion[:,i]=simulacion[:,i-1] * (np.exp((miu-0.5*sigma**2)*dt+sigma*e[:,i-1]*np.sqrt(dt)))

    simulacion=pd.DataFrame(np.transpose(simulacion))
    plt.plot(simulacion)
    plt.xlabel('Steps')
    plt.ylabel('Stock Price')
    plt.title("Porfolio Price Simulation")
    plt.show()

def GARCH():
    retornos =stocks.stock_info(assets,momentum_days)
    for i in range(len(assets)):
        lista=[]
        lista.append( retornos.iloc[:,i])
        garch = arch_model(lista, vol='garch', p=1, o=0, q=1)
        garch_fitted = garch.fit()
        plt.plot(garch_fitted.conditional_volatility)
        plt.title("Volatilidad "+ str(assets[i]))
        plt.show()
        print(garch_fitted.summary())
    


def printMenu():

    print("\n*******************************************\n")
    print("Bienvenido:\n")

    print("1- Long Portfolio")
    print("2- Long Short Portfolio")
    print("0- Salir")
    print("\n*******************************************\n")

def optionOne():

    model, stock_return = Controller.longPortfolio(stock_info, expected_return, min_bound, max_bound)

    vars = Controller.calculatePortfolioVar(stock_info,momentum_days)
    printVar(vars)
    if model.status == GRB.OPTIMAL:

        variables = {v.varName : round(v.x, 4) for v in model.getVars()}
        wight_stocks = list(variables.values())

        print('\n-------------------------------\n')

        print("La volatilidad del portafolio optimo es:" + " " + str(round(np.sqrt(model.objVal)*100,3))+"%")
        print('El retorno anual del portafolio optimo es:' + ' ' + str(round(np.sum(wight_stocks*stock_return)*100,3)) + '%\n')
        print('Los pesos son: \n')
        for i, value in variables.items():
            print('\t', i, value)
        

        print('\n-------------------------------\n')
        
        x= int(input("Desea ver el GBM? Si: 1  No:0 "))
        if x==1:
            print(GBM(np.sum(wight_stocks*stock_return),np.sqrt(model.objVal),wight_stocks))
            print(GARCH())
    else:

        print('\n-------------------------------\n')
        print("No optimal solution with those constrains.")
        print('\n-------------------------------\n')


def optionTwo():

    model, stock_return = Controller.longShortPortfolio(stock_info, expected_return)

    vars = Controller.calculatePortfolioVar(stock_info,momentum_days)
    printVar(vars)

    if model.status == GRB.OPTIMAL:

        variables = {v.varName : round(v.x, 4) for v in model.getVars()}
        wight_stocks = list(variables.values())

        print('\n-------------------------------\n')

        print("La volatilidad del portafolio optimo es:" + " " + str(round(np.sqrt(model.objVal)*100,3))+"%")
        print('El retorno anual del portafolio optimo es:' + ' ' + str(round(np.sum(wight_stocks*stock_return)*100,3)) + '%\n')

        print('Los pesos son: \n')
        for i, value in variables.items():
            print('\t', i, value)

        print('\n-------------------------------\n')

        x= int(input("Desea ver el GBM? Si: 1  No:0 "))
        if x==1:
            print(GBM(np.sum(wight_stocks*stock_return),np.sqrt(model.objVal),wight_stocks))
            

    else:

        print('\n-------------------------------\n')
        print("No optimal solution with those constrains.")
        print('\n-------------------------------\n')

def printVar(vars):

    print("VaR:",vars)


# ___________________________________________________
#  Main ~ Run
# ___________________________________________________

while True:

    n= input("Desea cargar la informacion de Yahoo o del archivo generado 'Portafolio.csv'? 1: Yahoo, 0: Portafolio.csv. \n Si desea salir de la aplicacion escriba: EXIT\n>")

    if n =="EXIT":
        sys.exit(0)
    elif int(n)==1:
        generateCsv = True
        retrive_csv_info = False
        n=int(input("Ingrese el número de activos que conforman el portafolio"))
        for i in range(n):
            ticker=str(input("Ingrese el ticker del activo "))
            assets.append(ticker)
    else:
        retrive_csv_info = True
        generateCsv = False

    # ... Retrieve information of the assets from the specified source.

    momentum=input("Ingrese cuantos años de información desea descargar, o Enter si desea el default de 2 annos.")
    if momentum:
         momentum_days =int(momentum)*365

    stock_info = Controller.init(calc_log_return, retrive_csv_info, assets, momentum_days)
    #Carga la informacion en un .csv para no tener que estar descargando de Yahoo cada vez en las pruebas de funcionalidad.
    if generateCsv:
        stock_info.to_csv('Portafolio.csv', sep=';', index=False)

    printMenu() 
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        executiontime = timeit.timeit(optionOne, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    else:
        sys.exit(0)
        

