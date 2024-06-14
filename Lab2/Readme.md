## Реализация скрипта для определения MTU 

---
Чтобы запустить контейнер необходимы следующие две команды:

```
docker build -t scriptimage .
docker run scriptimage
```

Если небходимо указать дополнительные параметры, то команда будет выглядеть так:

```
docker run -e MaxBlockSize=1500 -e MinBlockSize=0 -e Address=www.aaa.ru scriptimage
```

* MaxBlockSize - верхняя граница поиска

* MinBlockSize - нижняя граница поиска

* Address - адрес назначения
---
Так же скрип реализован на языке PowerShell, для его запуска необходимо запустить и открыть Windows PowerShell, и в командой строке написать следующие строки для запуска:

```
Set-Executionpolicy RemoteSigned -Scope Process

powershell -executionpolicy RemoteSigned -file lab2.ps1
```
Чтобы указать параметры:

```
powershell -executionpolicy RemoteSigned -file lab2.ps1 -Address '8.8.8.8' -MaxBlockSize 2000
```
---
