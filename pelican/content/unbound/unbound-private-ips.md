title: Unbound und DNS Rebind Schutz
status: published
lang: de
date: 2025-01-09 11:22:33

Um sich vor [DNS Rebind](https://unit42.paloaltonetworks.com/dns-rebinding/) Attaken zu schützen bietet Unbound die Möglichkeit Private IP Adressen in den DNS Antworten zu filtern. Hierdurch werden Anfragen auf DNS Namen, welche IP Adressen aus den benannten Bereichen enthält, mit einer leeren Antwort beantwortet. Falls man jedoch aufgrund fehlender Infrastruktur für sich selbst private Adressen in einer öffentlichen DNS Zone eingetragen hat, dann möchte man vielleicht sicherstellen das dieser Parameter für den eigenen privaten Adressraum nicht gesetzt ist. Aus Sicherheitsgründen wird bzw. wurde überlegt diesen als Standard mit aufzunehmen.

Der notwendige Parameter für die Konfiguration ```unbound.conf``` lautet ```private-address: <RFC1913-Adresse>/<bits>```. Er kann mehrfach in der Konfiguration erscheinen, falls alle privaten Adressräume angegeben sind.

In meinen Fall musste ich einen Teilbereich entfernen da ich für mein Heimnetz nicht auf einen lokalen DNS Server zurückgreifen wollte, und stattdessen private Adressen gewollt in einer öffentlichen Zone eingetragen habe. Noch nicht die endgültige Lösung, natürlich, aber ein Workaround der mir hilft um die nächsten Aufgaben zu erledigen.
