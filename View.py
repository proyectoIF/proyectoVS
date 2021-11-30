
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

# ___________________________________________________
#  Variables and stock info retrieval
# ___________________________________________________

# -------> Stock Information

# ... Auxiliary variables to specify how the data should be loaded to the program. 
# see Controller.init() for more infomation.

calc_log_return = False
retrive_csv_info = False

# ... Automatic API

assets = ["AAPL", "AMZN", "CHPT"]
momentum_days = 365*2

# ... Retrieve information of the assets from the specified source.

stock_info = Controller.init(calc_log_return, retrive_csv_info, assets, momentum_days)
stock_info.to_csv('Portafolio.csv', sep=';', index=False)

# Optimizer parameters.

expected_return = None
min_bound = None
max_bound = None

# ___________________________________________________
#  Principal Menu and interaction with the user.
# ___________________________________________________


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
        
