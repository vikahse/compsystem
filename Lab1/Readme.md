## Реализация небольшой сети офиса

## Описание хода работы 

1. Строим топологию, как указано в задании: в качестве клиентов сети выбираем Virtual PC (VPCS), в качестве коммутаторов доступа и ядра сети выбираем Cisco vIOS Switch, в качестве маршрутизатора выбираем Cisco vIOS Router.
2. Соединяем их между собой как на картинке в задании и настраиваем каждую ноду по-своему
   
   (снимок экрана моей топологии)

3. Настройка клиентов сети:
```
ip 10.0.10.1/24 10.0.10.254 - VPC1
ip 10.0.20.1/24 10.0.20.254 - VPC2
```

Команда для просмотра ip:
```
show ip
```
4. Настройка коммутаторов доступа:
   
SW1:

```
en

conf t

hostname SW1 - устанавливаем название

vlan 10, 20 - указываем vlan
exit

interface gi0/1
switchport mode access
switchport access vlan 10
exit

interface gi0/0
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

interface gi1/0
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

spanning-tree mode rapid-pvst
spanning-tree vlan 10 priority 28672

do wr

```
  
SW2:

```
en

conf t

hostname SW2 - устанавливаем название

vlan 10, 20 - указываем vlan
exit

interface gi0/2
switchport mode access
switchport access vlan 20
exit

interface gi0/0
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

interface gi1/0
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

spanning-tree mode rapid-pvst
spanning-tree vlan 20 priority 28672

do wr

```

SW0:

```
en

conf t

hostname SW0 - устанавливаем название

vlan 10, 20 - указываем vlan
exit

interface gi0/1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

interface gi0/2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 1,10,20 
exit

spanning-tree mode rapid-pvst - rapid-pvst позволяет коммутаторам быстро обнаруживать изменения в сети и сходимость сети в случае сбоев, что повышает производительность и надежность сети
spanning-tree vlan 10, 20 priority 24567 - устанавливаем SW0 корнем дерева для vlan 10,20 c помощью priority, чем меньше priority, тем важнее узел в дереве

do wr

```
R1

```
en

conf t

hostname R1 - устанавливаем название

interface gi0/3
ip address 10.0.1.254 255.255.255.0
no shutdown
exit

interface gi0/3.10
encapsulation dot1q 10
ip address 10.0.10.254 255.255.255.0
exit

interface gi0/3.20
encapsulation dot1q 20
ip address 10.0.20.254 255.255.255.0
exit

do wr

ip routing - включение маршрутизации
```

Дополнительные команды:

```
show run - показывает как настроены интерфейсы (do show run, если находимся в conf t)
show vlan
show spanning-tree vlan <vlan-id>
show ip route
