# Schemaoberfläche

Diese genaue Referenz richtet sich an Menschen, die Software mit Axioval
verbinden. Wenn Sie nur eine Prüfung verstehen oder vorbereiten möchten,
beginnen Sie stattdessen bei den [vier Bausteinen](../guide/building-blocks.de.md).

Die Quelltextbeispiele bleiben eingeklappt, bis Sie sie bewusst öffnen.

## Module

| Modul | Zuständig für |
| --- | --- |
| `Types.pkl` | Bezeichner, semantische Versionen, lokalisierter Text, Paketmetadaten |
| `Values.pkl` | Markierte Skalar- und Listenwerte sowie Objekt- und Eigenschaftsreferenzen |
| `Selectors.pkl` | Selektoren für Objekttyp, Eigenschaft, Klassifikation und boolesche Zusammensetzung |
| `Definitions.pkl` | Vokabulare und wiederverwendbare Fähigkeitsvorlagen |
| `RuleSets.pkl` | Konkrete Regelinstanzen und rein kosmetische Ordner |

## Definitionspaket

Ein normalisiertes Definitionsdokument hat diese Felder der obersten Ebene:

??? example "Quelltext oder Befehle anzeigen"
    ```json
    {
      "schemaVersion": "0.1.0",
      "package": {},
      "objectTypes": {},
      "properties": {},
      "propertySets": {},
      "definitions": {}
    }
    ```

Mindestens eine wiederverwendbare Komponente muss vorhanden sein. Map-Schlüssel müssen den Komponenten-IDs entsprechen. Doppelte Komponenten-IDs über geladene Pakete hinweg werden abgelehnt.

### `ObjectTypeDefinition`

Ordnet eine stabile Axioval-Objekttyp-ID externen Schemanamen wie `IfcWall` zu. Objekttypreferenzen können festlegen, ob Untertypen akzeptiert werden.

### `PropertyDefinition`

Ordnet eine stabile Eigenschafts-ID externen Namen und einer `valueKind` zu. Mengeneigenschaften benötigen außerdem eine qualifizierte `unitDimension`. Die Eigenschaft ist von jedem Container unabhängig.

### `PropertySetDefinition`

Ordnet eine stabile Qualifizierer-ID externen Containernamen zu. Sie enthält keine Mitgliederliste und begründet keine Eigentumsbeziehung.

### `RuleDefinition`

Deklariert eine Fähigkeit und eine typisierte Parameter-Map. `referencedValueKind` ist nur für einen `propertyReference`-Parameter gültig und beschränkt den katalogisierten Typ der referenzierten Eigenschaft.

## Referenzwerte

=== "Objekttyp"

    ??? example "JSON anzeigen"
        ```json
        {
          "type": "objectTypeReference",
          "objectType": "axioval:example.ifc.wall",
          "includeSubtypes": true
        }
        ```

=== "Eigenschaft, lose"

    ??? example "JSON anzeigen"
        ```json
        {
          "type": "propertyReference",
          "property": "axioval:example.ifc.is-external"
        }
        ```

=== "Eigenschaft, streng"

    ??? example "JSON anzeigen"
        ```json
        {
          "type": "propertyReference",
          "property": "axioval:example.ifc.load-bearing",
          "propertySet": "axioval:example.ifc.pset-wall-common"
        }
        ```

## Selektoren

Selektoren sind deklarativ und werden rekursiv validiert:

- `all`
- `entityType` mit einer kanonischen Objekttyp-ID
- `property` mit kanonischer Eigenschafts-ID und optionalem Set-Qualifizierer
- `classification`
- `allOf`, `anyOf` und `not`

Ein Vergleichswert auf einem Eigenschaftsselektor muss zur katalogisierten `valueKind` der referenzierten Eigenschaft passen. `exists` lehnt einen Vergleichswert ab. Jeder andere Operator benötigt einen.

## Umfangreiche Anwendbarkeit

Eine Regel mit mehreren Populationen verwendet ein `Applicability`-Objekt. Die
Map `groups` gibt jeder Population eine stabile lokale ID, einen lokalisierten
Namen, eine optionale Beschreibung und einen rekursiv validierten Selektor.
Anforderungen und vertrauenswürdige Host-Adapter können diese Gruppen über ihre
ID ansprechen.

Eine Regel für die Schlitz- und Durchbruchsplanung kann zum Beispiel getrennte
Gruppen für durchdrungene Bauteile, durchdringende Bauteile und Öffnungen
benennen, statt sie als eine flache Auswahl darzustellen. Map-Schlüssel müssen
den Gruppen-IDs entsprechen. Leere Gruppen-Maps, unbekannte Begriffe und
fehlerhafte Selektoren werden abgelehnt.

Bestehende Regeln dürfen weiterhin direkt einen einzelnen Selektor angeben.
Anforderungen benötigen die umfangreiche Form, weil ein flacher Selektor keine
adressierbaren Gruppen-IDs hat.

## Anforderungen

Eine `Requirement` besitzt eine stabile ID, eine lokalisierte Aussage, eine
optionale Beschreibung und eine oder mehrere `targetGroups`. Jede referenzierte
Gruppe muss in derselben Regel vorhanden sein. Anforderungs-IDs und
Gruppenreferenzen müssen eindeutig sein.

Anforderungen erklären den erwarteten Zustand. Sie führen keinen Paketcode aus
und ersetzen nicht den Vertrag `RuleDefinition.capability`, den eine
vertrauenswürdige Anwendung umsetzt.

## Erklärende Bilder

Eine Regel kann `ExplanatoryImage`-Einträge mit lokalisiertem Alternativtext und
einer optionalen lokalisierten Bildunterschrift enthalten. Bilder sind im Paket
enthaltene Dateien mit normalisiertem relativem Pfad und deklariertem Medientyp.
PNG, JPEG, WebP und SVG werden unterstützt.

Die Normalisierung lehnt absolute Pfade, Traversierung, Rückwärtsschrägstriche,
Abweichungen zwischen Erweiterung und Medientyp, doppelte Bild-IDs, fehlende
Dateien, aus dem Paket führende symbolische Links, aktive SVG-Inhalte, externe
SVG-Referenzen und falsche Raster-Signaturen ab. Bilder erklären nur und ändern
weder Anwendbarkeit noch Ausführung.

## Ordner sind kosmetisch

`RuleFolder` dient Darstellung und Organisation. Seine Position ändert weder Selektorumfang, Regelidentität, Ausführungssemantik noch Vertrauen. Verbraucher können alternative Ansichten darstellen, ohne die Regeln umzuschreiben.

## Kompatibilitätsstatus

Die aktuelle Schemaversion ist `0.1.0` und noch nicht stabil. Die geplante Kompatibilitätspolitik steht in der [Roadmap](../community/roadmap.de.md), Vertragsänderungen im [Changelog](../community/changelog.de.md).
