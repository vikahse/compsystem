## Реализация небольшой сети офиса

## Описание хода работы 

1. Строим топологию, как указано в задании: в качестве клиентов сети выбираем Virtual PC (VPCS), в качестве коммутаторов доступа и ядра сети выбираем Cisco vIOS Switch, в качестве маршрутизатора выбираем Cisco vIOS Router.
2. Соединяем их между собой как на картинке в задании и настраиваем каждую ноду по-своему
   
![Моя топология сети офиса](https://github.com/vikahse/compsystem/blob/main/Lab1/images/topology.jpeg)

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
5. Проверка:

---

VPC1:

```
show ip
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc1_ip.jpeg)

VPC2:

```
show ip
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc2_ip.jpeg)

---

SW1:

```
do show vlan
do show vlan 10
do show vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw1_vlan.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw1_vlan_10.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw1_vlan_20.jpeg)

Видно, что интерфейс gi0/1 только на vlan 10

SW2:

```
do show vlan
do show vlan 10
do show vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw2_vlan.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw2_vlan_10.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw2_vlan_20.jpeg)

Видно, что интерфейс gi0/2 только на vlan 20

SW0:

```
do show vlan
do show vlan 10
do show vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw0_vlan.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw0_vlan_10.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw0_vlan_20.jpeg)

---

Теперь проверим, что SW0 является корнем STP дерева для VLAN 10, 20 и, что линк между коммутаторами уровня доступа стал заблокированным

SW0:

```
do show spanning-tree vlan 10
do show spanning-tree vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw0_stp_10.jpeg)
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw0_stp_20.jpeg)

SW1:

```
do show spanning-tree vlan 10
do show spanning-tree vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw1_stp_10.jpeg)
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw1_stp_20.jpeg)

SW2:

```
do show spanning-tree vlan 10
do show spanning-tree vlan 20
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw2_stp_10.jpeg)
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/sw2_stp_20.jpeg)

Мы видим, что Root Id Address у всех коммутаторов равен 5000.0005.0000, а это и есть Address у SW0, так же у SW0 написано - This bridge is the root. Так же видно, что gi0/0 BLK, то есть линк между коммутаторами SW1 и SW2 заблокирован. Еще я читала статью, что для блокировки линка между коммутаторами можно ставить большую стоимость прохода. (https://notes.networklessons.com/stp-determining-blocked-port-using-cost)

Дополнительно:

SW1:
```
interface gi0/0
spanning-tree cost 200 - (https://notes.networklessons.com/stp-determining-blocked-port-using-cost)
exit

interface gi0/1
spanning-tree portfast edge -  функция, которая позволяет порту пропустить состояния listening и learning и сразу же перейти в состояние forwarding. Настраивается на портах уровня доступа, к которым подключены пользователи или сервера (http://xgu.ru/wiki/STP_в_Cisco)
exit
```

SW2:
```
interface gi0/0
spanning-tree vlan cost 200 - (https://notes.networklessons.com/stp-determining-blocked-port-using-cost)
exit

interface gi0/2
spanning-tree portfast edge - функция, которая позволяет порту пропустить состояния listening и learning и сразу же перейти в состояние forwarding. Настраивается на портах уровня доступа, к которым подключены пользователи или сервера (http://xgu.ru/wiki/STP_в_Cisco)
exit
```

---
Проверка на ping:

R1:

```
ip routing
do show ip route
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/r1_route.jpeg)

VPC1:
```
ping 10.0.10.1 -c 3
ping 10.0.20.1 -c 3
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc1_ping.jpeg)

VPC2:
```
ping 10.0.20.1 -c 3
ping 10.0.10.1 -c 3
```
![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc2_ping.jpeg)

---
Проверка на отказоустойчивость:
1) Уберем линк между SW1 и SW2, то есть интерфейс gi0/0:
   
Связь сохранилась

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc1_link_0_0.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc2_link_0_0.jpeg)

2) Уберем линк между SW1 и SW0:
   
Связь сохранилась

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc1_link_1_0.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc2_link_1_0.jpeg)

3) Уберем линк между SW2 и SW0:
   
Связь сохранилась

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc1_link_1_0_2.jpeg)

![](https://github.com/vikahse/compsystem/blob/main/Lab1/images/vpc2_link_1_0_2.jpeg)

Дополнительные команды:

```
show run - показывает как настроены интерфейсы (do show run, если находимся в conf t)
show vlan
show vlan id <vlan-id>
show spanning-tree vlan <vlan-id>
show ip route
show arp
```
Литература:
* http://xgu.ru/wiki/STP_в_Cisco
* https://notes.networklessons.com/stp-determining-blocked-port-using-cost
* https://habr.com/ru/companies/otus/articles/749644/
* https://habr.com/ru/articles/143768/
* https://www.justogroup.ru/dokumentacija/cisco/kommutiruemye_seti/nastroyka_stp.pdf
* https://habr.com/ru/articles/321132/
* https://linkas.ru/articles/vlan-v-cisco/?ysclid=lxdsyrun6m868682459
* https://www.geeksforgeeks.org/portfast-configured-on-a-cisco-switch-port/
* https://ipcisco.com/lesson/stp-configuration-on-cisco-packet-tracer/
* https://asp24.ru/novichkam/vlan-dlya-chaynikov/
* http://www.netza.ru/2013/01/vlan.html?ysclid=lxdr2nrdfk522463858
