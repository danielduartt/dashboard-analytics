# Total móvel dentro de 30 dias 

```
total movel 30 dias = 
DataAtual = MAX(Tb_Calendario[Date])
RETURN 
    CALCULATE( [Total Vendas], DATESBETWEEN(Tb_Calendario[Date], DataAtual - 30, DataAtual))
```