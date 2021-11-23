
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

import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np


# ___________________________________________________
#  Long Portfolio with special constrains
#  - Expected Return
#  - Minimum Weight
#  - Maximum Weight
# ___________________________________________________

def optimal_long_portfolio(df, expected_return, min_bound, max_bound):

    stock_return = df.mean()*252
    df_cov = df.cov()*252

    model = gp.Model('Best Portfolio')
    model.setParam(GRB.Param.OutputFlag, 0)

    wight_stocks = {i : model.addVar(vtype = GRB.CONTINUOUS, name = i, lb = 0, ub = 1) for i in df.columns}
    weights = np.array(list(wight_stocks.values()))
    model.addConstr(quicksum(wight_stocks[i] for i in wight_stocks) == 1, name='Budget')

    if expected_return != None:
        model.addConstr(quicksum(wight_stocks[i]*stock_return[i] for i in wight_stocks) >= expected_return, name='Return')

    if min_bound != None:
        for i, value in wight_stocks.items():
            model.addConstr(value >= min_bound, name = 'LBound' + i)

    if max_bound != None:
        for i, value in wight_stocks.items():
            model.addConstr(value <= max_bound, name = 'UBound' + i)

    model.setObjective(df_cov.dot(weights).dot(weights), GRB.MINIMIZE)
    model.update()

    return model, stock_return


# ___________________________________________________
#  Long Short Portfolio with special constrains
#  - Expected Return
# ___________________________________________________

def optimal_long_short_portfolio(df, expected_return):

    stock_return = df.mean()*252
    df_cov = df.cov()*252

    model = gp.Model('Best Portfolio')
    model.setParam(GRB.Param.OutputFlag, 0)

    wight_stocks = {i : model.addVar(vtype = GRB.CONTINUOUS, name = i, lb = -1, ub = 1) for i in df.columns}
    weights = np.array(list(wight_stocks.values()))
    model.addConstr(quicksum(wight_stocks[i] for i in wight_stocks) == 1, name='Budget')

    if expected_return != None:
        model.addConstr(quicksum(wight_stocks[i]*stock_return[i] for i in wight_stocks) >= expected_return, name='Return')

    model.setObjective(df_cov.dot(weights).dot(weights), GRB.MINIMIZE)
    model.update()

    return model, stock_return