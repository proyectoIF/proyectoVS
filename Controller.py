
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

import Stock_Info as info
import Min_Risk_Long_Portfolio as min_risk
import Merton_Robert_Portfolio as merton_robert


# ___________________________________________________
#  Loads assets info.
# ___________________________________________________

def init(log, csv, assets, momentum):
    """
    loads the stock information based on the needs.
    """
    # If retrive_csv_info is set to false (in View) then stock information will be imported from Yahoo.
    if not csv:
        return info.stock_info(assets, momentum)

    # If calc_log_return is set to false (in View) but retrive_csv_info is set to true then the assets
    # information is loaded from the file 'Portafolio.csv'. In this case the file 'Portafolio.csv' must
    # contain the logarithmic returns of the assets. 
    if not log:
        return info.get_info(';')
    else:
        return info.get_log_info(';')


# ___________________________________________________
#  Portfolio functions 
# ___________________________________________________


def longPortfolio(stock_info, expected_return, min_bound, max_bound):
    """
    Optimizer that returns the optimal portfolio with only long positions.
    """
    model, stock_return = min_risk.optimal_long_portfolio(stock_info, expected_return, min_bound, max_bound)
    model.optimize()

    return model, stock_return


def longShortPortfolio(stock_info, expected_return):
    """
    Optimizer that returns the optimal porfalofio with short and long positions.
    """
    model, stock_return = min_risk.optimal_long_short_portfolio(stock_info, expected_return)
    model.optimize()

    return model, stock_return


def mertonRobertPorfolio(stock_info, expected_return):
    """
    https://www.jstor.org/stable/2329621?origin=JSTOR-pdf
    """
    return merton_robert.Menton_Robert_Porfolio(stock_info, expected_return)