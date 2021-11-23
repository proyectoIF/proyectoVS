
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

import pandas as pd
import numpy as np

# ___________________________________________________
#  Paper Implementation
# ___________________________________________________


def Menton_Robert_Porfolio (df, excepted_return):

    returns = df.mean()*252
    df_cov = df.cov()*252
    df_cov_inv = pd.DataFrame(np.linalg.pinv(df_cov.values), df_cov.columns, df_cov.index)

    vector_ones = np.ones(len(df.columns))

    # @ is for matrix multiplication.
    a = vector_ones@df_cov_inv@returns
    b = returns.T@df_cov_inv@returns
    c = vector_ones.T@df_cov_inv@vector_ones
    d = b*c - a**2

    g = 1/d*(b*df_cov_inv@vector_ones - a*df_cov_inv@returns)
    h = 1/d*(c*df_cov_inv@returns - a*df_cov_inv@vector_ones)

    weights = g + h*excepted_return
    risk = np.sqrt(1/d * ( (c * (excepted_return**2)) - (2 * a * excepted_return) + b ))
    
    return weights, risk

