
'''
Pasos para la implementacion del Value at Risk del portafolio de activos:

1. Definir la matriz var-covar de los activos.
2. Calcular el VaR de cada activo independiente.
    2.1. Calcular la volatilidad del portafolio de mercado.
    2.2. Calcular la covarianza entre el activo y el mercado.
    2.3. Calcular el beta del activo = Cov(Activo,Mercado)/VarMercado.
    2.4. multiplicar: (cuantilNormal(1-alpha) * BetaActivo * sigmaMercado) % (queda en porcentaje)
3. Calcular la matriz de correlaciones a partir de la matriz de varianzas y covarianzas.
    3.1. Calcular la matriz diagonal de var-covar y realizar la siguiente operacion: sigmas = inverse(sqrt(Diag(var-covar)))
    3.2. Realizar la siguiente operacion matricial: corr_matrix = sigmas * var-covar * sigmas
4. Calcular el DVAR^2 con la siguiente operacion equivalente en Excel: MMULT(transponer(vectorVaRs);MMULT(corr_matrix;vectorVaRs))
5. calcular sqrt(DVAR^2) y este ya es el resultado buscado para el Daily Value at Risk del portafolio.
NOTA: La respuesta queda expresada en porcentaje.

'''

import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
import Stock_Info
from scipy.stats import norm


def portfolioVaR(df_daily: DataFrame, momentum: int):
    
    #importa los datos del portafolio de mercado:
    # 2.1
    assets = ["^GSPC"]
    df_Mkt_rets = Stock_Info.stock_info(assets,momentum)
    sigmaMkt = np.sqrt(df_Mkt_rets.var())[0]
    
    # 2.2 calcula la covarianza entre el activo y el mercado
    
    covariances = []
    pairs = pd.DataFrame()
    for column in df_daily:
        pairs= pd.concat([df_Mkt_rets,df_daily[column]],axis =1)
        covariances.append(pairs.cov().at["^GSPC",column])

    # 2.3 Calcula los betas de cada activo:

    betas = []
    for i in range(len(covariances)):
        betas.append(covariances[i]/(sigmaMkt**2))

    # 2.4 Queda expresado en porcentaje...

    VaRs = []
    for i in range(len(covariances)):
        VaRs.append(norm.ppf(0.95)*betas[i]*sigmaMkt)
    
    VaRs = pd.DataFrame(VaRs, index=df_daily.columns)

    # 1.0 definir la matriz var-covar de los activos

    varCovar = pd.DataFrame()
    varCovar = df_daily.cov()

    # 3.0 Calcular la matriz de correlaciones a partir de la matriz de varianzas y covarianzas.

    # 3.1. Calcular la matriz diagonal de var-covar y realizar la siguiente operacion: sigmas = inverse(sqrt(Diag(var-covar)))

    diag = np.diag(np.diag(varCovar)) # matriz diagonal con las varianzas de los activos del portafolio.
    diag = np.sqrt(diag) # matriz diagonal con las volatilidades de los activos del portafolio.
    diag = pd.DataFrame(diag)

    invSigmas = pd.DataFrame(np.linalg.pinv(diag.values), columns= varCovar.columns, index = varCovar.index)

    # 3.2. Realizar la siguiente operacion matricial: corr_matrix = sigmas * var-covar * sigmas

    invSigmasA, varCovarA = invSigmas.align(varCovar) # para evitar future warnings.
    corr_matrix = pd.DataFrame(np.matmul(np.matmul(invSigmasA,varCovarA),invSigmasA))

    # 4. Calcular el DVAR^2 con la siguiente operacion equivalente en Excel: MMULT(transponer(vectorVaRs);MMULT(corr_matrix;vectorVaRs))

    dvar2 = np.matmul(VaRs.transpose(), np.matmul(corr_matrix, VaRs))

    # 5. Calcular sqrt(DVAR^2) y este ya es el resultado buscado para el Daily Value at Risk del portafolio.

    dvar = np.sqrt(dvar2.at[0,0])*100 #expresado en procentaje.

    return dvar


