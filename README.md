# quiosque-dl
Um pequeno script em Python para baixar arquivos do quiosque da UFRRJ em massa.


## Configuração
O script tenta abrir seu arquivo de configuração na seguinte ordem:

 * $XDG_CONFIG_HOME/quiosque-dl.conf
 * ~/quiosque-dl.conf

Exemplo de configuração:
```INI
[User]
Name=<matrícula>
Password=<senha>
```
