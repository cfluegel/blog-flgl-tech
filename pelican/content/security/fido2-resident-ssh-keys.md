title: Resident SSH Keys auf FIDO2 Sticks erstellen
status: published
lang: de
date: 2023-05-31 22:40:00

FIDO2 ist ein Standard der einem viele Möglichkeiten eröffnet. Neben der passwordlosen Anmeldung ermöglicht es einem auch die 2FA Authentifizierung, aber viel interessanter ist die Möglichkeit einen SSH Schlüssel auf dem Stick selbst abzulegen.

Vorab, leider bringt Windows 10 / 11 eine zu alte SSH Version mit, so dass es dort noch nicht nativ funktioniert. Unter MacOS muss man ebenfalls eine neuere OpenSSH Version installieren. Dies kann man ganz einfach mit Homebrew hinbekommen.

Man kann verschiedene Sicherheitsstufen einrichten, aber für mich persönlich entscheide ich mich immer für die Nutzung von Pin und Touch, jedoch verzichte ich auf die Nutzung einer zusätzlichen Passphrase. Dafür muss natürlich zuvor ein Pin gesetzt sein. Weitere hilfreiche Informationen gib es in einem [guide](https://gist.github.com/Kranzes/be4fffba5da3799ee93134dc68a4c67b) zum Nachlesen.


Folgenden Befehl nutze ich dann zur Erstellung von dem SSH Schlüssel auf z.B. dem Yubikey:
```bash
ssh-keygen -t ed25519-sk -O resident -O verify-required -C "Comment"
```

Bei der Erstellung wird man nach dem Speicherort von den Key Dateien gefragt. Hier ist dann letztlich nur die Datei mit dem öffentlichen Schlüssel wichtig. Diese muss nun auf die Server verteilt werden.

Um den Schlüssel nun nutzen zu können, muss ggf. der ssh-agent der aktiven Shell Sitzung hinzugefügt werden. Dies geschieht mit dem Befehl ``` eval "$(ssh-agent -s)" ``` und danach kann man den SSH Schlüssel mit dem Befehl ``` ssh-add -K ``` hinzufügen. Dies ist nun ein temporäres hinzufügen. Es gibt die Möglichkeit den Schlüssel permanent auf dem System abzulegen, aber das halte ich nicht unbedingt als sicher.

