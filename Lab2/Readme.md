## Реализация скрипта для определения MTU 

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
