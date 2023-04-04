title: Docker Multi-Stage Builds
status: published
lang: de
date: 2023-04-04 21:28:00
modified: 2023-04-04 22:38:00

Das wichtigste an Docker Images ist es die Image Größe so klein wie möglich zu halten. Leider ist es nicht immer möglich auf bereits komplierte Software zurückgreifen zu können. Für solche Fälle muss man dann die Software irgendwie eingehändig übersetzen. Dies würde jedoch für viele unnötige Softwarekomponenten in dem Docker Image sorgen.

Die Lösung für dieses Problem heißt Docker Multi Stage Builds. Das Kompilieren und das Bauen des finalen Image werden bei dieser Variante auf verschiedene Ebenen ausgeglidert.

Das *Dockerfile* enthält in diesem Fall mehr als einen Beschreibungsblock. Üblicherweise sieht man einen Two-Stage Build bestehend aus dem Kompilieren und dem Zusammenbauen des finalen Image geschieht dann über zwei Stages.

Jede Ebene beginnt mit einem "FROM ..." Befehl und kann mit "AS uniqname" abgeschlossen werden. Erst dies ermöglichst den Zugriff auf Dateien einer anderen Stage.

# Beispiel Aufbau eins Two Stage Builds
```docker
### FIRST STAGE (Builder)
FROM debian:latest AS builder
RUN apt update && apt install build-essentials
#
# ... weitere Schritte ...
#
RUN make && make install

### FINAL STAGE (Image creation)
FROM debian:latest
COPY --from=builder /usr/local/bin/self_compiled_binary /usr/local/bin

EXPOSE 1234
ENTRYPOINT ["/usr/local/bin/self_compiled_binary"]
```

# Praxisbeispiel
Ich habe das Konzept testweise beim Erstellen von diesem Github Repository umgesetzt: [Docker Tinyproxy](https://github.com/cfluegel/docker-tinyproxy) Es ist fernab von einer wirklich eleganten Lösung, aber ich wollte mich zunächst nur mit dem Konzept vertraut machen. Experte kann man später werden

Wieso Tinyproxy? Weil Tinyproxy am Ende nur wenige Dateien auf dem Dateisystem ablegt. Hierdurch hält sich der Umfang der Zeilen in dem Dockerfile in Grenzen.

In der ersten Stage werden alle für das Kompilieren notwendige Softwarepakete installiert. Die Software wird dann als letztes in das finale Image kopiertn, nachdem zuvor der C Programmcode übersetzt wurde.

## Nun einige Zahlen

| Image | Größe |
|-------|-------|
| Debian | 124 MB |
| Builder Stage | 505 MB | 
| Finales Image | 125 MB |


Man erkennt, ohne Multi Stage Build wäre das Image mit 505 viel zu groß. So ist es nur minimal größer als das Debian Image. Und auch das lässt sich noch optimieren, wenn man möchte.
