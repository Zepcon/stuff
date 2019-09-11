# Vim_notes

Einfach ein paar Notizen für den Aufbau und den Umgang mit Vim

***

Vim Notizen:

- Escape Key auf capslock packen, weil man damit schneller zwischen den modes wechseln kann

3 verschiedene Modes: Normal, Insert, Visual

- ~/.vimrc kann die vim Konfigurationen verändern, am besten in git behalten, damit man die Veränderungen beobachten kann
	-> gihub.com/thoughtbot/dotfiles kann man die

- vimtutor oder vimadventures kann am Anfang helfen, die ersten Dinge zu lernen
	-> vimcasts.org

- Ctrl+P kann filenames auch mit Teilen suchen
- NerdTree kann filename Verläufe anzeigen

***
## Allgemeine Befehle:

- `:w` = speichern

- `:q` = verlassen

- `:q!` = verlassen ohne zu speichern

- `u` = undo

- `Strg + R` = redo

***

## Command Mode:

1. mit den `h`, `l`, `j`, `k` Tasten kann man den Cursor bewegen:

- `h` = links
- `l` = rechts
- `j` = runter
- `k` = hoch

2. mit `w`, `e`, `b` kann man zwischen den Wörtern und an die Positionen von Wörtern springen:

- `w` = Anfang vom nächsten Wort
- `e` = Ende des Wortes
- `b` = Anfang des Wortes

- Mit der Kombination aus Zahlen und diesen Buchstaben, führt man den Befehl so oft aus. Beispielsweise 3w springt 3 Wörter weiter zum Anfang.

- Man kann so auch mehrere Zeichen oder Buchstaben hintereinander schreiben, mit (glaube ich) 3ihello hat man hellohellohello

3. Mit dem Buchstaben `f` kann man im command modus ein Buchstaben oder ein Wort finden. Wenn man also `flol` eingibt, erhält man das nächste lol und mit 3fer das dritt-nächste er

3. Mit `%`, also der zweier-Tastenkombination kann man zu der nächsten Klammer ( { [ springen.

4. Für den Anfang einer Line `0` drücken und für as Ende `$`

5. Mit `*` kann man das nächste gleiche Wort finden, welches sich momentan unter dem Cursor befindet und mit `#` findet man das vorherige Wort, ebenfalls unter dem Cursor.

6. Mit `gg` kann man an den Anfang von dem kompletten file springen, mit `G` zu dem Ende. Wenn man zu einer bestimmten line-nummer springen will, einfach die Nummer for G packen, also 4G für die vierte Line.

7. Mit `/` kann man eine Suche nach einem Text starten, welcher dahinter eingegeben wird. Mit `n` und `N` kann man dann weiter durch die occurences gehen.

8. Mit `o` für unter der momentanen oder `O` für ober der momentanen Line kann man text in eine neue Line schreiben, wenn die neue Line erstellt wurde, wechselt der Editor automatisch in den INSERT Mode, in welchem man dann in das file schreiben kann.

9. Mit `x` kann man die characters unter dem cursor und mit `X` links von dem Cursor löschen.

10. Wenn man nur einen Charakter unter dem Cursor entfernen will, ohne in den insert mode zu gehen, kann man `r` dafür verwenden.

11. Mit `d` kann man alle möglichen Arten des Löschens betreiben, wenn man beispielsweise `dw` eingibt, dann löscht man das erste Wort auf der rechten Seite des Cursors.

12. Mit `.` kann man den vorherigen command noch einmal ausführen.

***

## Visual-mode:

- Hier wählt man zuerst den Text aus, bevor man entscheidet was man damit machen will.

- Der Text wird dann markiert und man kann beispielsweise den markierten Text löschen oder durch einen anderen Text ersetzen.

***

## Ablauf innerhalb eines Vim-files:

- Wenn man in das file kommt, muss man sich erst einmal für einen mode entscheiden

- Einfaches drücken von `i` bringt einen direkt in den insert mode, wenn man wieder in den normal mode will muss man die `Esc` Taste drücken.