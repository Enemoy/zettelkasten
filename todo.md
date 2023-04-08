# Todo-Liste für den Zettelkasten


## neue Funktionen

- Bash-Script um im Browser eine Website als Quelle hinzuzufügen:
	- automatisches Auswählen des Links
	- hinzufügen per Script
	- Abfrage von Titel / Autor
	- automatisches Hinzufügen von Datum als "zuletzt aufgerufen"
	- Auswahl der Bibliografie, zu der Quelle hinzugefügt werden soll (Default: Online)

## Verbesserungen / Überarbeitungen

- argparse verbessern:
	- defaults
	- Optionen zum Auswählen
- add_citation verbessern:
	- Option für Extraktion aus LaTeX - formatierten Zitaten
- query Funktion verbessern:
	- default Argumente
	- Suchen in allen Tabellen
- tags zu .bib-Einträgen hinzuzufügen:
	- Weiterverarbeitung in der Tags aus Bibtex
- rows über eine bestimmte Range löschen / mehrere angeben
- argparse mit "" Strings konfigurieren
- Wenn citekey (wegen z.B. Änderung) nicht gefunden wird, Fehlermeldung über nicht vorhanden citekey bei query Funktion
- read query args for -s option from stdin
