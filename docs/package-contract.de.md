# Sichere Annahme von Paketen

Bevor ein geteiltes Paket ein Prüfwerkzeug erreicht, öffnet Axioval es durch
eine feste Reihe von Sicherheitsstufen. Jede Stufe beantwortet eine einfache
Frage: Sind die Dateien am richtigen Ort, lassen sie sich sicher öffnen, passen
alle Verweise zusammen und ist das Ergebnis vollständig?

Eigene und fremde Pakete durchlaufen dieselben Stufen. Der Name des Repositorys
gibt einem Paket keine Sonderrechte.

<div class="diagram-frame" markdown>

![Ein Paket wird untersucht, sicher geöffnet, vollständig geprüft und an ein kompatibles Werkzeug übergeben](assets/images/trust-path.de.svg)

</div>

## Erforderliche Dateien

??? example "Quelltext oder Befehle anzeigen"
    ```text
    axioval.json      # statisches Erkennungsmanifest
    PklProject        # festgelegte Pkl-Projektgrenze
    <entry>.pkl       # von axioval.json benanntes Regelwerkmodul
    <definition>.pkl  # eine oder mehrere von axioval.json benannte Definitionsmodule
    ```

Das Manifest **muss** gegen `schema/registry-manifest.schema.json` validieren. Einstiegspunkte sind repository-relative Pkl-Pfade. Absolute Pfade, `..`-Traversal, unbekannte Felder, fehlende Module und Nicht-Pkl-Einstiegspunkte sind verboten.

## Geordnete Vertrauensgrenze

Die Reihenfolge ist Teil des Sicherheitsvertrags:

1. `axioval.json` als nicht vertrauenswürdige statische Daten parsen;
2. jedes Feld gegen das Manifest-JSON-Schema validieren;
3. **alle** Regelwerk- und Definitionspfade innerhalb der Repository-Wurzel auflösen;
4. Pkl nur mit `file:`-/`pkl:`-Modulen und `file:`-/`prop:`-Ressourcen sowie CPU-, Speicher-, Ausgabe- und Zeitlimits auswerten;
5. jedes Kandidaten-Definitionsdokument validieren;
6. deklarierte Pakete, Objekttypen, Eigenschaften, Property-Set-Qualifizierer, Vorlagen, Selektoren und typisierte Parameterwerte binden;
7. doppelte, fehlende, unbekannte, widersprüchliche, fehlerhafte oder nicht unterstützte Deklarationen ablehnen; und
8. semantisch validierte Ausgabe mit geprüften normalisierten Snapshots vergleichen.

!!! danger
    Evaluator-Ausgabe vor Schritt 6 ist **Kandidaten-JSON**, kein normalisiertes Austauschformat. Ein erfolgreicher Pkl-Prozess beweist nicht, dass ein Paket gültig ist.

## Trennung von Autorenerstellung und Laufzeit

Pkl-Quelltext darf Importe, lokale Werte und Hilfen für Autoren verwenden. Die Auswertung muss all dies zu deklarativen Daten absenken. Anwendungen führen nur Fähigkeiten aus, die sie bereits implementieren. Sie führen niemals vom Paket gelieferte Modellprüfungslogik aus.

## Vertrag zur Eigenschaftsauflösung

Eine Eigenschaftsreferenz benennt immer eine kanonische `PropertyDefinition`.

- Ohne `propertySet` lösen Adapter sie über unterstützte Container hinweg auf.
- Mit `propertySet` verlangen Adapter genau diese kanonische Containerbeziehung.
- Mehrere inkompatible Auflösungen sind Konflikte, keine beliebigen Gewinner.
- `referencedValueKind` muss mit der referenzierten Eigenschaftsdefinition übereinstimmen.

Property-Set-Qualifizierer besitzen keine Eigenschaften und sind keine Ausführungsordner.

## Quell- und kompilierte Formen

Pkl-Quelltext ist für die Bearbeitung maßgeblich. Eine Registry kann validiertes normalisiertes JSON zwischenspeichern, aber generierte Ausgabe allein beweist nicht, dass die Quelle sicher oder gültig ist. Cache-Schlüssel sollen die unveränderliche Quellrevision, Schemaversion, Pkl-Version und Validator-Version enthalten.

## Lizenzierung und Herkunft

Paketautoren wählen ihre eigene Lizenz und ihren Repository-Host. Eine Registry-Auflistung überträgt kein Eigentum und bedeutet keine Befürwortung. Axioval-eigene Pakete sind gewöhnliche Pakete, die durch dieselbe Pipeline validiert werden.
