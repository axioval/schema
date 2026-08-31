---
hide:
  - edit
---

# Roadmap

Axioval soll Validierungsanforderungen portabel machen, ohne Pakete ausführbar zu machen oder einen Anbieter, ein Modellformat oder Repository-Eigentümer zu bevorzugen.

Diese Roadmap beschreibt eine Absicht, keine Kompatibilitätsgarantie. Inhalte von Meilensteinen können sich verschieben, wenn Konformitätstests fehlende Grundlagen aufdecken.

## Jetzt: Vertrauenswürdige Grundlage für Autoren (`0.1.x`)

- [x] Typisierte Pkl-Autorenmodule und deterministisches normalisiertes JSON.
- [x] Statische Manifestprüfung zuerst und auf das Repository begrenzte Auswertung.
- [x] Fail-closed Bindung von Paket, Definition, Parameter, Selektor und Snapshot.
- [x] Wiederverwendbares Objekt-/Eigenschaftsvokabular mit externen Schemanamen.
- [x] Optionale genaue Qualifizierung eines Eigenschaftscontainers.
- [x] Umfangreiche öffentliche Dokumentation und ein vollständiges Tutorial vom Vokabular zur Instanz.
- [ ] Unveränderliches `v0.1.0` nach externer Prüfung durch Verbraucher veröffentlichen.

## Als Nächstes: Governance portabler Fähigkeiten (`0.2.x`)

- Registry für Fähigkeiten mit stabilen semantischen Verträgen und Konformitätsvektoren definieren, nicht mit Engine-Implementierungen.
- Deterministischen Austausch von Diagnosen und Ergebnissen spezifizieren.
- Einheiten-/Mengensystem-IDs und Umrechnungsverträge ergänzen.
- Konflikt-, fehlende, nicht unterstützte und ungültige Informationszustände ausdrücklich definieren.
- Abhängigkeitsidentitäten, Prüfsummen und Sperrdaten für Pakete ergänzen.
- Migrationswerkzeuge für normalisierte Schemaänderungen veröffentlichen.

## Danach: Ökosystem und Registry (`0.3.x`)

- Einreichungs- und Entdeckungsabläufe für `axioval/registry` starten.
- Unveränderliche Repository-Revisionen in isolierten Workern validieren.
- Signierte Validierungsnachweise und normalisierte Artefakt-Hashes veröffentlichen.
- Deklarierte Fähigkeitsunterstützung von Anwendungen indizieren.
- Paket-Kompatibilitätsmatrizen ohne eigentumsbasiertes Vertrauen ergänzen.
- Externe Vokabularpakete unterstützen, die viele Regelwerke gemeinsam verwenden.

## Stabiler Vertrag (`1.0.0`)

Ein Release `1.0.0` erfordert:

- dokumentierte Regeln für Schemaversion-Aushandlung und Migration;
- mehrere unabhängige Paketautoren und Verbraucher von Prüf-Engines;
- eine öffentliche Konformitätssuite mit fail-closed negativen Vektoren;
- stabile Fähigkeiten- und Diagnosesemantik;
- reproduzierbare Paketvalidierung; und
- eine ausdrückliche Verfalls- und Sicherheitsreaktionspolitik.

## Offene Designfragen

- Wie sollen kanonische Konzepte auf bSDD, IDS und Nicht-IFC-Vokabulare verweisen, ohne einen Dienst verpflichtend zu machen?
- Welche Fälle doppelter Eigenschaften sind Konflikte, welche Vorrangregeln?
- Wie sollen Eigenschaftsquellen auf Typ- gegenüber Vorkommensebene dargestellt werden?
- Welche Funktionen zur Zusammensetzung von Vorlagen lassen sich sauber zu deklarativen normalisierten Daten absenken, ohne eine versteckte Programmiersprache zu werden?
- Wie sollen lokalisierte Diagnosen und Hinweise zur Abhilfe standardisiert werden?

## Nichtziele

- Von Paketen bereitgestellte ausführbare Prüfungslogik ausliefern.
- IFC-Analyse, Geometriekernels oder Laufzeit-IRs von Anwendungen besitzen.
- Ordner oder Property Sets als universelle semantische Hierarchien behandeln.
- Axioval-eigenen Repositories besonderes Registry-Vertrauen geben.
- Behaupten, dass ein Dokumentationsbeispiel eine normative DIN- oder IFC-Konformitätsregel ist.
