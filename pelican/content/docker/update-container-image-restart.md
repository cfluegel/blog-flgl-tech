title: Update running Docker container to latest image
status: published
lang: de

Seit kurzem nutze ich für einige Dienste intensiv die Möglichkeiten von Docker (Podman wäre hier als direkte Alternative zu benennen) und bin soweit auch zufrieden. Dazu wird es nun weitere Artikel geben.

Nun ist es, wie bei jeder anderen Software, notwendig die Software aktual zu halten. Es gibt einen automatischen Weg, aber aktuell lasse ich mich nur über neue Container Images informieren und entscheide dann wenn ich das Update durchführe.

Ich nutze ```docker-compose.yml``` Dateien und nutze die folgenden Befehle zum Updaten und neustarten.
```
# Update der Images
docker compose pull

# Docker Container neu erstellen, ggf. neubauen und dann im Hintergrund starten
docker compose up --force-recreate --build -d
```

Da sich hierdurch die Anzahl an Layer und alten Images erhöhen kann ist es ratsam in regelmäßigen Abständen auch den folgenden Befehl auszuführen. Um unnötige Downloads zu vermeiden sollte dies erst nach Test der neuen Version geschehen.
```
docker image prune -f
```

Quelle: [Stackoverflow](https://stackoverflow.com/a/49316987)