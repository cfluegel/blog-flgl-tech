title: Abstände zwischen den Icons im Dock hinzufügen
status: published
lang: de
date: 2023-05-09 13:23:55

Im Dock sammeln sich über die Zeit so einige Icons. Um hier nicht den Überblick zu verlieren kann es helfen logische Gruppen zu bilden.

MacOS bietet (aktuell) dafür noch keine eigene Möglichkeit, weshalb man auf einen Workaround zurückgreifen muss. Es gibt zwei Größen die man einfügen kann. Ich hatte noch keinen Einsatzzweck für die großen Trenner, weshalb ich bisher nur die kleinen Trenner bei meinen Geräten genutzt habe.

### Kleine Trenner
```bash
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="small-spacer-tile";}'; killall Dock
```

### Große Trenner
```bash
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="spacer-tile";}'; killall Dock
```

[Quelle](https://chrispennington.blog/blog/add-spacer-in-macos-dock/)