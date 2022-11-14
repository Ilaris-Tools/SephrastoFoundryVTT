# SephrastoFoundryVTT

Ein Sephrasto Plugin um Charaktere automatisch in einem Format zu speichern, das direkt als Akteur im Ilaris System für FoundryVTT verwendet werden kann.

## Installation

Die Datei in den Plugin-Ordner entpacken. Wo dieser Ordner zu finden ist steht in Einstellungen von Sephrasto im Bereich Speicherpfade. Nach einem Neustart von Sephrasto kann das Plugin in den Einstellungen aktiviert werden.

## Benutzung

Wenn das Plugin aktiv ist, wird beim Speichern des Helden neben der `<name>.xml` automatisch eine zweite Datei `<name>_foundryvtt.json` erstellt, die in Foundry als Held importiert werden kann.

## Einschränkungen

Das Plugin ist noch in einem frühen Entwicklungsstadium und kaum getestet. Es soll Sephrasto Versionen >3.2.2 unterstützen. Aufgrund der technischen Unterschiede wird nur ein für Foundry relevanter Teil der Informationen exportiert. Das hat zur Folge, dass Foundry Charaktere nicht zurück in das Sephrasto Format konvertiert werden können. Die xml-Datei also nicht löschen!

Bisher nicht übertragen wird:

- [ ] Geld
- [ ] Status von Waffen/Rüstungen (in/aktiv, haupthand/nebenhand, kampfstil)
- [ ] Einstellungen für Sephrasto (Welcher Bogen, Zonensystem, Regelanhänge usw..)
