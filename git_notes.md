# Git-Notizen für den allgemeinen Umgang

***

Weil ich ein Noob und eine Person bin, die sich gerne Notizen macht, ein weiteres file für Notizen bei dem allgemeinen Umgang mit git und die Funktionsweisen.

***

## Keywords mit ihren Bedeutungen:

- `push` = Lädt Änderungen/ commits zu einem entfernten Server hoch

- `pull` = gleicht das lokale repository mit dem entfernten Repository ab

- `log` = log-Daten anschauen (ausführlich)

- `show` = Änderungen verfolgen
 
- `gitk` = Dateiversionen verfolgen

- `ammend` = nachträgliche Änderungen an Konflikten und commits machen und diese dann direkt pushen

- `branch` = stellt den lokalen Arbeitsbereich dar, welcher eine Abzweigung von dem master ist

- `conflict` = entsteht, wenn zwei Personen Änderungen in dem gleichen Bereich einer Datei machen und diese dann zusammenführen wollen, es gibt verschiedene Möglichkeiten, diesen Konflik zu lösen

***

## Befehle:

- `git remote show origin` = liest das Quell-Repository aus und zeigt Informationen von diesem Repository an

- `git status` = gibt einem den akutellen Stand von Dateien im Vergleich zu dem remote Repository an

- `git log --stat -abbrev-commit` = `stat` gibt an, wie viele Dateien pro commit verändert wurden, also wie viele Additionen und Subtraktionen es bei einer Datei gab; mit `abbrev-commit` werden die Hashes von den Commits abgekürzt, sodass nur noch 10 stellen übrig bleiben

- `git show --pretty=oneline Hash-Wert` = gibt die commits mit dem entsprechenden Hash-Wert als Einzeiler aus

- `git commit --amend -m "Nachricht"` = auf diese Weise kann man einen letzten commit (logischerweise nur, wenn noch nicht gepusht wurde) noch einmal korrigieren
***

## Management von Dateien und Struktur:

- `git init --bare` = erstellt ein Repo, welches nur zum Teilen mit anderen Personen gedacht ist und ohne die eigentlichen Arbeitsdateien auskommt

- `git clone xxx` = klont ein entferntes Repository, kann man aus github mit dem https link von dem repository machen oder mit per ssh, Link kommt dann an die Stelle von XXX

## Szenarien mit Lösungen:

- Problem: Man hat zwei Dateien verändert, aber nur eine geadded. Man pusht dann und schreibt in die vommit message, was man an beiden Dateien verändert hat obwohl nur die eine vorerst gepusht wird.
Man kann den commit für die zweite Datei dann nachholen.

1. `Git add Datei2`

2. `git commit --amend --no-edit`

Auf diese Weise wird der vorherige commit komplett durch den neuen commit ersetzt, aber beide Dateien bleiben erhalten. Wegen `no-edit` bleibt auch die alte Datei erhalten.

