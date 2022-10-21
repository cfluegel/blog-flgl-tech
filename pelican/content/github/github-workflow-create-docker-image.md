title: Github Workflow zum Erstellen von Docker Images nutzen
status: published
lang: de

Ich bin wahrlich nicht die erste Person die sich mit dem Thema beschäftigt und höchstwahrscheinlich gibt es auch effizientere Lösungen, aber ich bin am sprichwörtlichen Rom angekommen.

## Was ist Github Workflow
Github Workflow bietet die Möglichkeit automatisiert Aufgaben durchführen zu lassen. Die Aufgaben können sowohl automatisch durch ein Event ausgelöst werden, als auch manuell gestartet werden. Das ganze ist im Rahmen eines Continuous Integration / Continuous Delivery Prozess zu verstehen und bietet die hierfür notwendigen Tools

Ein Workflow kann einen oder mehrere Jobs besitzen, welche sich zum Beispiel um die Prüfung von Quelltext, dem Bauen von Artifacten und dem anschließenden Deployment kümmern, aber man besitzt beim Erstellen viele Freiheiten

Github bietet unterschiedliche Betriebssystem-Runner für die Ausführung der Jobs an.

Jede größere Plattform besitzt inzwischen ähnliche Tools für die CI/CD Integration.

## Weshalb Github Workflow für mich
Das hat im Grunde zwei Gründe.
Zum einen begann ich Github intensiver zu nutzen als ich 2021 anfing meine Infrastruktur mit Ansible Playbooks aufzubauen, aber der andere Grund ist die derzeitige Wahl meines Arbeitsmittels.

Als Apple die eigene Arm Architektur mit ihren M1 präsentierte hat mich das enorme Stromsparpotenzial begeistert. Seitdem bin ich mehr oder minder am Testen wie gut die Apple M1 (und nachfolgende) Architektur nutzbar ist.

Die Architektur war in diesem Fall der Grund für den Weg zu Github Workflow, da jedes Docker Image eben nicht in der sonst so üblichen x86_64 Architektur erstellt wird. Ich hätte keine Probleme mit der manuellen Erstellung gehabt, solange ich dafür nicht extra andere Computer starten müsste.

Und somit begann ich mich mit den Möglichkeiten von Github Workflow w zu beschäftigen.

## Wie nutze ich Github Workflow
Aktuell nutze ich Github Workflow nur zur Erstellung von Webserver Container Images mit dem [Pelican](https://getpelican.com/) Output von diesem Blog. Die Workflows und der Content ist unter diesem [Github Repo](https://github.com/cfluegel/blog-flgl-tech) zu finden.

Der [Workflow](https://github.com/cfluegel/blog-flgl-tech/blob/main/.github/workflows/create-docker-image.yml) wird aktuell bei jedem Push ausgeführt. Das beinhaltet auch das Bestätigen eines PR über die Github Webseite. Hier bietet Github Workflow die Möglichkeit Schritte eines Jobs mit if-Bedingungen zu versehen. Ich möchte aktuell nicht das direkt ein neues Image erstellt wird. Deshalb sind die entsprechenden Schritte mit einer solchen if-Bedingung versehen.

Ansonsten ist der Workflow recht einfach gehalten. Hier die groben Schritte:

1. Code auschecken
2. Python Umgebung vorbereiten + Pelican Abhängigkeiten mit pip installieren
3. ```make clean``` im Pelican Ordner ausführen (eigentlich nicht notwendig)
4. ```make publish``` im Pelican Ordner ausführen um den statischen Content des Blogs zu generieren
5. Docker anmelden, Metadaten sammeln und das Image erstellen. Danach wird es direkt unter meinem Dockerhub Benutzer hochgeladen

Der Dockerhub Benutzername und *Personal Access Token* liegen in den Github Repository Secrets bereit. Der Weg wurde so in den [Github Workflow Dokumentation](https://docs.github.com/en/actions/using-workflows) beschrieben.

Die von mir gefundenen Bespiele nutzten Ubuntu als Basis für das Runner Betriebssystem und das erschien mir dann das einfachste hier ebenfalls auf Ubuntu zu setzen.

## Ausblick
Durch meine intensivere Nutzung von Docker werde ich wohl zukünftig weiter auf Github Workflows setzen. Die Limits für freie Benutzeraccounts sind aktuell noch recht großzügig, so dass ich wohl nicht so schnell an die Limits ankomme. Zumindest bei der Nutzung von Standard Runnern und Abläufen.