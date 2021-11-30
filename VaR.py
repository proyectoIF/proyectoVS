
'''
Pasos para la implementacion del Value at Risk del portafolio de activos:

1. Definir la matriz var-covar de los activos.
2. Calcular el VaR de cada activo independiente.
    2.1. Calcular la volatilidad del portafolio de mercado.
    2.2. Calcular la covarianza entre el activo y el mercado.
    2.3. Calcular el beta del activo = Cov(Activo,Mercado)/VarMercado.
    2.4. multiplicar: (cuantilNormal(1-alpha) * BetaActivo * sigmaMercado) % (queda en porcentaje)
3. Calcular la matriz de correlaciones a partir de la matriz de varianzas y covarianzas.
    3.1. calcular la matriz diagonal de var-covar y realizar la siguiente operacion: sigmas = inverse(sqrt(Diag(var-covar)))
    3.2. Realizar la siguiente operacion matricial: corr_matrix = sigmas * var-covar * sigmas
4. Calcular el DVAR^2 con la siguiente operacion equivalente en Excel: MMULT(transponer(vectorVaRs);MMULT(corr_matrix;vectorVaRs)))
5. calcular sqrt(DVAR^2) y este ya es el resultado buscado para el Daily Value at Risk del portafolio.

'''

import pandas as pd
import numpy as np
import Stock_Info



def portfolioVaR(df_daily_covar):
    
    #importa los datos del portafolio de mercado:
    assets = ["^GSPC"]
    momentum = len(df_daily_covar.index)
    df_Mkt_rets = Stock_Info.stock_info(assets,momentum)

