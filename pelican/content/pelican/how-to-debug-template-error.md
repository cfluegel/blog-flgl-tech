title: Fehler in Pelican Templates debuggen
status: published
lang: de
date: 2022-10-24 07:52:00 

Ich habe mir das Theme, welches ich für diese Webseite nutze, bezüglich eingebundenen Fonts angeschaut. Hintergrund ist derzeit laufende DSGVO Abmahnwelle aufgrund eingebundener Fonts zu fremden Servern. [Heise berichtet](https://www.heise.de/news/DSGVO-Abmahnwelle-wegen-Google-Fonts-7206364.html). Google wird im Artikel genutzt, aber sicher zählt dies auch für andere Server von Fremdpersonen & -Firmen.

Leider nutzt das Theme auch Google Fonts, weshalb ich das Blog so noch nicht online stellen kann. Die letzten Änderungen im [Git Repo](https://github.com/fle/pelican-simplegrey) beziehen sich leider nicht auf die aktuelle Verfahrens-welle bezüglich den Fonts, weshalb ich selbst die Anpassungen vornehmen musste.

Der Download der Fonts und das anschließende Einbinden war nicht sonderlich kompliziert, aber ich nutzt die Gelegenheit um weitere kleine Anpassungen an den Template Dateien vorzunehmen.

Beim Bearbeiten baute ich leider Fehler in einer der Templatedateien ein. Diese führten zu einer eher wenig sagenden Exceptions sobald ich das Blog neu generieren wollte. Erst mit diesem Befehl (gekürzt) habe ich dann mehr Informationen über die Quelle für den Fehler in Erfahrung bringen können. Die nachfolgende Befehlszeile habe ich mir aus dem Makefile extrahiert:

```bash
# zusätzliche Parameter:
# -v   verbose
# -D   debug
pelican -r content/ -o output/ -s pelicanconf.py -v -D
```

Ich will nicht ausschließen das es nicht auch einen Weg mithilfe von make gegeben hätte, aber dieser Weg hatte für mich funktioniert.

Es half das ich bereits Python Erfahrung besitze, aber die Meldung enthielt den Namen des Templates und eine ungefähre Stelle an der ich suchen musste.

Natürlich hätte ich auch einen Diff erstellen oder die vorherige Version des Templates wieder herstellen können, aber ich will neue Wege kennenlernen. Und einfach alle Änderungen wegwerfen erschien mir nicht als Produktiv. Nun bin ich um einen weiteren Weg reicher und kann das Wissen so vielleicht zukünftig bei anderen Probleme mit Pelican etwas damit anfangen.
