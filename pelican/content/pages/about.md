title: Über
lang: de
status: published
date: 2022-11-05 09:44

Dieses Blog dient mir als Notizblock in dem ich für mich relevante Informationen speichere. Alles rund um das Thema IT und Softwareentwicklung.

Ich benötige keine dynamische Webseite für die Darstellung von dem Inhalt weshalb ich mich für den Weg der statischen Webseitengenerierung entschieden habe. Es gibt inzwischen einige statische Webseitengeneratoren, aber die Wahl fiel auf Pelican. Ich hatte bereits in der Vergangenheit mit Pelican gearbeitet. Möglicherweise wechsel ich in der Zukunft noch einen der anderen Generatoren, aber das ist in der Zukunft.

Zum Versionstracking nutze ich ein eigenes Repository bei [Github](https://www.github.com/) und ist unter [Repository](https://github.com/cfluegel/blog-flgl-tech) öffentlich erreichbar. Ursprünglich hatte ich überlegt zwei separate Branches zu nutzen. Diese Idee habe ich inzwischen verworfen und arbeite direkt auf dem Main Branch.

Ich nutze Github Actions um automatisiert ein Docker Imager zu erzeugen und es im Anschluss auf Dockerhub zu veröffentlichen. In Verbindung mit einem automatisierten Deployment ermöglicht es mir ein relativ schnelles ausrollen einer neuen Version. Das ist für dieses Blog natürlich eher nicht notwendig, aber es erspart mir weitere Zeit zu investieren.
