# Proyecto final para el curso de Ingenieria Financiera.
# septimo semestre de Ingenieria Industrial.

# Sobre este proyecto:

El proyecto consta de un optimizador de portafolios basado en la teoria de seleccion de portafolios de Markowitz con algunas modificaciones, provee una estimacion de la volatilidad y los retornos esperados para el portafolio ensamblado, como tambien el calculo de su valor en riesgo (VaR). El programa tambien ofrece visualizar una simulaicion de Monte Carlo con movimiento browniano geometrico para el precio del portafolio durante los años que se piensa tener. Finalmente, la herramienta tambien calcula la estimacion de la volatilidad con garch(1,1) para cada uno de los activos que conforman el portafolio.

El archivo requirements.txt contiene uan lista de todas las dependencias del programa y su respectiva version. La mayoria de los paquetes requeridos son free open-source. Sin embargo, el paquete de optimizacion de gurobi requiere de una licencia academica para operar gratis, esta se puede conseguir facilmente en la pagina de ellos: https://www.gurobi.com/downloads/gurobi-optimizer-eula/ siguiendo los pasos indicados en la instalacion.
