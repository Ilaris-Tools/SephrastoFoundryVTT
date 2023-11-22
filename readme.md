# SephrastoFoundryVTT
> Das Plugin kann jetzt direkt im Paket mit vielen anderen Sephrasto Plugins heruntergeladen werden. Dieses Repository bleibt noch online um alte Sephrasto Versionen zu unterstützen, zukünftige Updates gibt es direkt auf: https://github.com/brzGatsu/SephrastoPlugins


Ein Sephrasto Plugin um Charaktere automatisch in einem Format zu speichern, das direkt als Akteur im Ilaris System für FoundryVTT verwendet werden kann.

## Installation

Die Datei in den Plugin-Ordner entpacken. Wo dieser Ordner zu finden ist steht in Einstellungen von Sephrasto im Bereich Speicherpfade. Nach einem Neustart von Sephrasto kann das Plugin in den Einstellungen aktiviert werden.

## Benutzung

Wenn das Plugin aktiv ist, wird beim Speichern des Helden neben der `<name>.xml` automatisch eine zweite Datei `<name>_foundryvtt.json` erstellt, die in Foundry als Held importiert werden kann.

## Einschränkungen

Das Plugin ist noch in einem frühen Entwicklungsstadium und kaum getestet. Es soll Sephrasto Versionen >3.2.2 unterstützen. Aufgrund der technischen Unterschiede wird nur ein für Foundry relevanter Teil der Informationen exportiert. Das hat zur Folge, dass Foundry Charaktere nicht zurück in das Sephrasto Format konvertiert werden können. Die xml-Datei also nicht löschen!

Bisher nicht übertragen (und damit beim importieren ggf. zurückgesetzt) wird:

- Geld
- Aktuelle Zustände: Wunden, Furcht, Boni/Mali, Geld usw.
- Status von Waffen/Rüstungen (in/aktiv, haupthand/nebenhand, kampfstil)
- Einstellungen für Sephrasto (Welcher Bogen, Zonensystem, Regelanhänge usw..)
- Hausregeln (Eigene Vorteile, Talente usw. könnten aber funktionieren)

Waffeneigenschaften werden aktuell noch nicht übertragen!

## Versionen

Der Einfachheit halber sind die Versionen als Zielversion von Sephrasto angegeben, für die es entwickelt und getestet wurde. Nicht jede kleine Sephrasto-Version wird ein Update des Plugins erfordern, daher sind Sprünge möglich. Sollten mehrere Updates für die selbe Version kommen, werden Buchstaben angehangen.

- **3.4.0.a** Auf die Schnelle einige Datenbank änderungen eingebaut, aber noch unvollständig.
- **3.2.2.c** Waffen/Items haben kein Gewicht mehr, zugekaufte KaP und AsP werden übertragen.
- **3.2.2.b** Abwärtskompatibel und einige bugfixes nach dem ersten Test.
- **3.2.2.a** Automatischer JSON-Export beim Speichern des Charakters.
- **3.2.1.a** JSON-Export beim Schreiben der PDF. Enthält die meisten für Foundry relevanten Informationen. Nur für ein Beispielcharakter getestet.
