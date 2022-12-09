title: Experimente mit MacVLAN Netzwerk
status: published
lang: de

Docker richtet standardmäßig das Bridge Interface ```docker0``` ein. Mit diesem Interface kommunizieren die Docker Container mit der Außenwelt. Intern erhalten die Docker Container dann eine interne nicht geroutete IP aus der Bereich 172.17.0.0/16 und durch Freigabe von Ports erhält man dann Zugriff auf die jeweiligen Container.

Zu 99% funktioniert das Standard Docker Netzwerk, also wieso möchte man ein anderes Netzwerk nutzen?

Folgende Gründe haben sich für mich herauskristalisiert:

* falls mehr als ein Container einen bestimmten Port nutzen müssen
* der Container auf L2 erreichbar sein muss


# Einrichtung eines MacVLAN Docker Netzwerk
Zunächst muss man den Netzwerkschnittstellennamen des kabelgebundenen Netzwerkschnittstelle herausfinden und für später notieren. In dem nachfolgenden Beispiel heißt die Schnittstelle **eno1**.
```bash
# ip l
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 98:90:96:c2:b7:78 brd ff:ff:ff:ff:ff:ff
    altname enp0s25
3: wlp2s0: <BROADCAST,MULTICAST> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default qlen 1000
    link/ether cc:3d:82:4c:3e:52 brd ff:ff:ff:ff:ff:ff
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:f0:6b:22:d0 brd ff:ff:ff:ff:ff:ff
```

Zusätzlich benötigt man die Netzmaske der Schnittstelle. Der einfachheit konzentriere ich mich hier auf die IPv4 Variante, da dies in vielen Fälle (leider) noch das meist genutzte sein wird.

In meinem Setup hat die Schnittstelle die IP Adresse 192.168.178.65 mit der Netzmask /24 und das Default Gateway ist 192.168.178.1.
```bash
# ip address list eno1
2: eno1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 98:90:96:c2:b7:78 brd ff:ff:ff:ff:ff:ff
    altname enp0s25
    inet 192.168.178.65/24 metric 100 brd 192.168.178.255 scope global dynamic eno1
       valid_lft 616403sec preferred_lft 616403sec
```

Mit den jetzt bekannten Daten kann das Docker Netzwerk eingerichtet werden. Hierzu gibt man den folgenden Befehl als Benutzer root ein:
```bash
# docker network create -d macvlan --subnet=192.168.178.65/24 --gateway=192.168.178.1  -o parent=eno1 macvlan0
```

Ob die Einrichtung erfolgreich war kann mit dem Befehl überprüft werden.
```bash
# docker network ls
```
Es werden hier nun alle bekannten Netzwerke dargestellt und dort sollte nun das Netzwerk mit dem Namen macvlan0 auftauchen.

**Wichtig!** Es wird hier der gesamte IP Netzwerkraum von dem angegebenen Netzwerk genutzt, wenn ein Container ohne explizite Angabe einer IP Adresse gestartet wird. Hierdurch kann es zu Doppelbelegungen der IP Adresse kommen. Um dies zu verhindern, bietet der Befehl "```docker network create```" noch die Option "```--ip-range```" mit derer einen Bereich aus dem Netzwerk für die Zuweisung definiert werden kann. Dieser Bereich kann dann von der DHCP Zuweisung ausgeklammert werden. Die Eingabe muss in der From *xxx.xxx.xxx.xxx/nn* geschehen. Bezogen auf das hier genutzte Netz wäre die Eingabe also:
"```--ip-range 192.168.178.248/29```" um die automatische Zuweisung auf den IP Bereich *192.168.178.249 bis 192.168.178.254* zu begrenzen.

Alternative dazu erstellt man die Docker Container mit der Angabe einer IP Adresse:
```bash
# docker  run --net=macvlan0 --ip=192.168.178.222 -itd alpine:latest /bin/sh
```

# Fallstrick 1: Kommunikation zwischen Docker Host und MacVLAN Container funktioniert nicht
Falls der Container mit dem Docker Host kommunizieren muss, z.B. weil
* man einen PiHole auf dem selben Host laufen hat
* oder lokale auf den Dienst des Containers zugreifen möchte
so wird zusätzlich eine freie IP Adresse aus dem IP Bereich benötigt. Diese IP Adresse fungiert als Router in der Routing Tabelle des Host Computer.

```bash
# ip link add mac0 link eno1 type macvlan mode bridge
# ip addr add 192.168.178.200/24 dev mac0
# ifconfig mac0 up
```

Danach kann der Docker Host den zuvor erstellen Container mit der IP 192.168.178.22 zugreifen.


Quellen:

* [https://collabnix.com/2-minutes-to-docker-macvlan-networking-a-beginners-guide/](https://collabnix.com/2-minutes-to-docker-macvlan-networking-a-beginners-guide/)
* [https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/](https://blog.oddbit.com/post/2018-03-12-using-docker-macvlan-networks/)
* [https://www.linuxtechi.com/create-use-macvlan-network-in-docker/](https://www.linuxtechi.com/create-use-macvlan-network-in-docker/)
