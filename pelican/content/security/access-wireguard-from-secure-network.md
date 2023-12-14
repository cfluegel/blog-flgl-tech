title: Wireguard aus einem sicheren Netzwerk nutzen
status: draft
lang: de
date: 2023-11-11 12:34:00

Ich hatte das erste mal Schwierigkeiten mich mit meinem Wireguard Netzwerk zu verbinden. Grundsätzlich bot das Internet hier 
einen freien Zugang aber Daten konnte ich über den Wireguard Tunnel nicht bekommen. An diesem Standort kommen WLAN Produkte von 
Aruba zum Einsatz. Vermutlich auch mit den entsprechenden Kontrollern, zumindest findet eine URL Filterung statt. 

Im Internet habe ich einen Hinweis zur Nutzung von dem NTP Port gefunden. Leider scheint Wireguard nicht auf mehr als einen Port lauschen 
zu können, weshalb ich einen anderen Weg finden musste. Also probiert ich es mit der folgenden IPTables Regel um den NTP auf den Wireguard 
Port umzuleiten: 
```bash
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 123 -j REDIRECT --to-port 51820
```

Und was soll ich sagen, damit hatte ich dann direkt auch schon wieder direkt Zugriff auf meinen Services 
