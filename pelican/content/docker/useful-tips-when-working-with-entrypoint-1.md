title: Hilfreiche Tipps für die eigene entrypoint.sh (1 von X)
status: published
lang: de
date: 2023-05-09 18:00:00

Es gibt zwei Befehle - CMD und ENTRYPOINT - die man in einem Dockerfile für den Start der Anwendung nutzen kann. Das Verhalten ist ähnlich aber unterscheidet sich leicht. In diesem Artikel(serie) möchte ich nicht auf die Unterschiede eingehen, sondern nur meine eigenen Erfahrungen und (Tipps) niederschreiben.

# Konfigurationsdatei beim Start eines Docker Containers bearbeiten
Für den kürzlich geschriebenen Artikel über [Multi Stage Dockerbuilds]({filename}multi-stage-build.md) brauchte ich eine Möglichkeit Inhalt in der Konfigurationsdatei anzupassen. Der Inhalt soll durch die Übergabe von Environment Variable bei dem Aufruf von ```docker run -e ``` verändert werden. Sollte kein Parameter übergeben sein, soll der Container natürlich weiterhin funktionien.

## Wenn kein Wert übergeben wurde einen Standardwert nutzen
Da ich mich für ein *simples* Bash Skript entschieden hatte, war die Lösung recht simple:
```bash
PORT=${LISTENPORT:-8888}
```
Falls die Variable ```$LISTENPORT``` nicht gesetzt sein, so wird automatisch der String "8888" in die Variable ```$PORT``` geschrieben.


## zusätzliche Zeilen an einer bestimmten Stelle einfügen
Für die Freischaltung von weiteren IP Bereichen wollte ich an einer bestimmten Stelle in der Konfiguration weitere Zeilen unbestimmter Anzahl einfügen.

***Vorab***: *Ich bin noch nicht 100% von dieser Lösung überzeugt, aber etwas besseres war mir bis jetzt nicht eingefallen. Sollte mir etwas besseres einfallen dann trage ich diese hier nach*

### Umsetzung

Meine Idee war das ich die Konfigurationsdatei mit einem Marker zu versehen und die zusätzlichen Zeilen hinter den Marker ```# dynamicRanges``` einzufügen. Hierdurch muss die Konfigurationsdatei angepasst werden, aber letztlich handelt es sich ja hier um mein Docker Image. Die folgende Befehlszeile ist in der ```entrypoint.sh``` enthalten und fügt die Daten aus der temporären Datei hinter der gesuchten Zeile.

```bash
sed -i "/# dynamicRanges/r ${TEMPFILE}" ${CONFIGFILE}
```

In diesem Fall hätte ich die zusätzlichen Zeilen vermutlich auch ans Ende der Konfigurationsdatei anfügen können, aber nicht jeder Konfiguraton
