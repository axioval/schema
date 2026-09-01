---
hide:
  - edit
---

# Zu Axioval MCS beitragen

Vielen Dank, dass Sie den herstellerneutralen Vertrag für Erstellung und Austausch verbessern. Vertragsänderungen betreffen Paketautoren, Registries und prüfende Anwendungen. Beiträge brauchen daher ausführbare Nachweise, nicht nur Text.

## Vor einer Änderung

1. Suchen Sie bestehende Issues und die [Roadmap](https://github.com/axioval/mcs/blob/main/ROADMAP.md).
2. Erläutern Sie, welche Schicht sich ändert: Vokabular, Vorlage, Instanz, Manifest, Normalisierung oder Anwendungsfähigkeit.
3. Beschreiben Sie Folgen für Kompatibilität und Sicherheit.
4. Verlinken Sie bei fachlichen Behauptungen nach Möglichkeit eine maßgebliche öffentliche Quelle und unterscheiden Sie normative Anforderungen von Beispielen.

## Repository-Grenzen

- `schema/` besitzt wiederverwendbare Pkl-Verträge.
- `scripts/` besitzt statische Prüfung und fail-closed semantisches Binden.
- `examples/` ist der **einzige** Ort für konkrete Regelinstanzen.
- Produktive Regelwerke liegen in getrennten Repositories.
- IFC-Parsing, Geometrie und Prüfalgorithmen gehören nicht hierher.
- Axioval-eigene Pakete erhalten kein Registry- oder Vertrauensprivileg.

## Entwicklungsumgebung

Voraussetzungen:

- Pkl `0.32.1` (in `.pkl-version` festgelegt);
- Python 3.11 oder neuer; und
- [`uv`](https://docs.astral.sh/uv/) für temporäre Werkzeuge.

Schema-Sperre ausführen:

??? example "Quelltext oder Befehle anzeigen"
    ```bash
    PATH="$HOME/.local/bin:$PATH" ./scripts/check.sh
    ```

Dokumentation genau wie CI bauen und linten:

??? example "Quelltext oder Befehle anzeigen"
    ```bash
    npx --yes markdownlint-cli2@0.18.1
    python -m pip install --disable-pip-version-check -r requirements-docs.txt
    mkdocs build --strict
    ```

Python-Änderungen linten und formatieren:

??? example "Quelltext oder Befehle anzeigen"
    ```bash
    uvx ruff format scripts tests
    uvx ruff check scripts tests
    ```

## Checkliste für Vertragsänderungen

Jede wesentliche Schemaänderung sollte enthalten:

- ein gültiges Pkl-Beispiel oder Fixture;
- neu erzeugte deterministische JSON-Snapshots;
- mindestens einen negativen Test, der beweist, dass der alte ungültige Zustand fail-closed fehlschlägt;
- synchronisierte Annahme durch Pkl und Python-Binder;
- Dokumentation des Verhaltens für Autoren und Verbraucher;
- einen `Unreleased`-Eintrag im Changelog; und
- einen sauberen strengen Dokumentationsbuild und `git diff --check`.

!!! note
    Ist ein strukturelles Pkl-Feld optional, muss der normalisierte Binder dieselbe Optionalität akzeptieren. Erfordert der Binder eine semantische Beziehung, die Pkl nicht lokal beweisen kann, ergänzen Sie deterministisches dokumentübergreifendes Binden und einen Ablehnungstest.

## Modellierung von Eigenschaften und Objekten

Bevorzugen Sie stabile kanonische Konzepte plus ausdrückliche externe Bindungen.

- Lassen Sie ein Property Set keine Eigenschaft besitzen.
- Verwenden Sie einen optionalen Property-Set-Qualifizierer nur, wenn die genaue Platzierung normativ ist.
- Halten Sie Darstellungsordner kosmetisch.
- Legen Sie erwartete Informationen in einer Regelbehauptung ab, nicht in der Anwendbarkeit, wenn dadurch verletzende Objekte verborgen würden.

## Dokumentationsstil

Die Pages-Seite wird aus `docs/` mit MkDocs Material gebaut. Verwenden Sie:

- kurze, auf Aufgaben ausgerichtete Seiten;
- einfache Sprache auf Startseite und Einstiegsreise;
- lokale zugängliche SVG-Diagramme mit lesbaren mobilen Varianten;
- eingeklappte Quelltextbereiche in Schritt-für-Schritt-Tutorials;
- keine Halbgeviert- oder Geviertstriche in Repository-Markdown;
- Hinweise zu Vertrauensgrenzen und normativen Einschränkungen;
- vollständige geprüfte Beispiele statt Pseudo-APIs;
- Verweise auf maßgebliche Spezifikationen für fachliche Behauptungen; und
- Diagramme nur, wenn sie Datenfluss oder Eigentum verdeutlichen.

## Pull Requests

Halten Sie Änderungen prüfbar und atomar. Beschreiben Sie:

- das Verhalten vorher und nachher;
- den vermiedenen Fehlermodus;
- ausgeführte Befehle und ihre echten Ergebnisse; und
- Migrations- oder Rollback-Überlegungen.

Mit einem Beitrag stimmen Sie zu, dass Ihr Beitrag unter [AGPL-3.0-or-later](https://github.com/axioval/mcs/blob/main/LICENSE) lizenziert ist.
