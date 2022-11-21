# Todo-Liste für den Zettelkasten


## neue Funktionen

- Integration in Vim
- Bash script, dass auf Suite zugreift:
	- Argument 1: Auswahl des Sub-Programm
	- Weitergabe alle anderen Argumente an Sub-Programm
- Funktion um einzelne Inhalte zu ändern (Zentiy / Terminal):
	- Argument 1: id (zur Bearbeitung)
	- Argument 2: Terminal oder Popup?
	- Argument 3: Spalte, die geändert werden soll
- Funktion für Backup:
	- Standardpfad im Config File
	- Ausführung vor bestimmten Funktionen, um Datenverlust zu vermeiden
- Bash-Script um im Browser eine Website als Quelle hinzuzufügen:
	- automatisches Auswählen des Links
	- hinzufügen per Script
	- Abfrage von Titel / Autor
	- automatisches Hinzufügen von Datum als "zuletzt aufgerufen"
	- Auswahl der Bibliografie, zu der Quelle hinzugefügt werden soll (Default: Online)
- Funktion, um Zitate / datapoints + Daten (Autor, Jahr, Buch, etc) schön ins Terminal zu printen

## Verbesserungen / Überarbeitungen

- argparse verbessern:
	- defaults
	- Optionen zum Auswählen
- add_citation verbessern:
	- Option für Extraktion aus LaTeX - formatierten Zitaten
