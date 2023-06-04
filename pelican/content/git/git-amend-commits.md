title: Git commits nachträglich bearbeiten
status: published
lang: de
date: 2023-06-04 12:23:05

Manchesmal kann es notwendig sein den letzten Commit zu modifizieren bevor man diesen an z.B. Github schickt. Vielleicht weil man vergessen hat den Commit zu signieren, oder noch Änderungen vergessen hat. Für mich habe ich zwei Fälle in denen ich von dieser Möglichkeit gebrauch mache; GPG Signature vergessen und Fehler in der Commit Nachricht. Alles weitere würde ein Rebase der Commit Historie erfordern und dies kann bei geteilten Repositories zu schweren Merge Konflikten sorgen. Es gibt Situationen bei denen dies sicherlich von Vorteil sein kann, aber ich selbst besitze in diesem Bereich zu wenig Wissen als das ich da eine sinnvolle Quelle für wäre.

## Beispiel 1: Signature vergessen
```bash
git commit -m "added new content "

# vergessen ein -S mit an dem commit Befehl zu übergeben. Den letzten Commit kann man dann mit dem Befehl anpassen:

git commit --amend --no-edit -S
```

## Beispiel 2: Fehlerhafte Commmit Message
```bash
git commit -m "best commit ever"

# Es ist doch nicht der beste Commit... also ändern wir das eben

git commit --amend -m "well, this was not the best commit"

```
