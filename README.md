# blog-flgl-tech

Dieses Repository dient als Grundlage für mein persönliches ["Blog"](https://blog.flgl.tech). Wobei Blog
nicht ganz passend ist. Es handelt sich eher um eine Art Notizbuch um meine Erfahrungen, Wissen und Fehler
aus der Welt der Technologie zu dokumentieren. Hauptsächlich für mich, aber falls andere die Notizen ebenfalls hilfreich finden ist das natürlich noch viel besser.

Für den Inhalt ist definitiv keine dynamische Webseite (z.B. mit PHP) notwendig. Außerdem sorgen dynamische Webseiten gleich für mehr Komplexität und mögliche Sicherheitsprobleme. Deshalb hab ich mich für die Nutzung eines Static Site Generators entschieden. Ein kleiner Nebeneffekt ist das ich mich hierdurch gleich mit Github Actions beschäftigen konnte und hierdurch Erfahrung bei der automatischen Genenerierung von Docker Images machen konnte.


# Todo für Github Actions
* ~~Regelmäßig testweise den Content neugenerieren~~: bei mehr Contributoren wäre es sicher nützlich, so eher nicht
* ~~Bei Push auf den **Main** Branch einen automatischen Upload auf den Server durchführen~~
  Watchtower aktualisiert regelmäßig (alle 6 Stunden) falls eine neue Version existiert
