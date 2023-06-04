title: Meine .gitconfig Datei für signierte Commits
status: published
lang: de
date: 2023-06-01 10:18:00

Meine Git Konfiguration ist nicht sonderlich spannend und ich habe ein privates Git Repo mit allen meiner dot files je nach Plattform, d.h. MacOS, Linux und Windows, aber durch die Nutzung von GPG sind Zeilen hinzugekommen

Die Konfigurationsoptionen sind hinzugekommen und müssen an die persönlichen Einstellungen angepasst werden:

* **user.signingkey:**   der GPG Fingerprint
* **commit.gpgsign:** sollen alle Commits signiert werden?
* **alias.logs:** zeigt die GPG Signaturen
* **alias.resign:** einen alten Commit nachträglich signieren (mit Vorsicht nutzen)

Man kann sicher vieles mehr machen und vielleicht wird es noch mehr werden, aber derzeit ist das völlig ausreichend für mich.

```
[user]
  name = Christoph Flügel

  # E-Mail Adresse anpassen
  # muss ebenfalls bei Github hinterlegt werden
  email = E-Mail.Adresse@Domain.Tld

  # Signing Key der bei Github eingetragen ist
  signingkey = F6B65...B2F4D

# Alle Commits signieren
[commit]
  gpgsign = true

[pull]
  rebase = false

[color]
  ui = true

[merge]
  ff = false

[init]
  defaultBranch = main

[alias]
  logs = log --show-signature
  resign = "!re() { git rebase --exec 'git commit --amend --no-edit -n -S' -i $1; }; re"
```
