from arch import arch_model

model = arch_model(train, mean='Zero', vol='GARCH', p=15, q=15)
