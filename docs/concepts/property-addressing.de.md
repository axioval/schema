# Wenn der Ort einer Eigenschaft wichtig ist

Dieselbe Information kann in einem Gebäudemodell an unterschiedlichen Stellen auftreten. Manchmal interessiert eine Anforderung nur die Information. Manchmal verlangt sie auch genau einen Ort. Axioval unterstützt beide Entscheidungen.

Stellen Sie es sich vor wie die Suche nach einem Buch:

- **Jedes Regal ist in Ordnung:** Finde dieses Buch, wo auch immer die Bibliothek es aufbewahrt.
- **Ein bestimmtes Regal ist erforderlich:** Finde dieses Buch in der Präsenzabteilung.

Technisch trennt Axioval **Eigenschaftsidentität** von **Container-Qualifizierung**. Property Sets sind in IFC echte Beziehungsobjekte, aber ihre Namen müssen nicht zur universellen Identität einer Eigenschaft werden.

## Kanonische Eigenschaftsidentität

Ein Vokabular definiert die Eigenschaft einmal:

??? example "Quelltext oder Befehle anzeigen"
    ```pkl
    ["axioval:example.ifc.load-bearing"] = new Definitions.PropertyDefinition {
      id = "axioval:example.ifc.load-bearing"
      name = new Types.LocalizedText { default = "Load bearing" }
      valueKind = "boolean"
      externalNames {
        new Definitions.ExternalName {
          typeSystem = "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3"
          name = "LoadBearing"
        }
      }
    }
    ```

Die Definition ist nicht in einem Property Set verschachtelt. Ihre stabile ID kann von Selektoren, Vorlagen und Instanzen wiederverwendet werden.

## Lose Referenz: Die Eigenschaft zählt, der Container nicht

??? example "Quelltext oder Befehle anzeigen"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.is-external"
    }
    ```

Ein Adapter löst den externen Namen auf und durchläuft die nativen Beziehungen des Modells. Die Eigenschaft darf in jedem unterstützten Container gefunden werden.

Implementierungen müssen ein deterministisches Verhalten bei Konflikten definieren. Löst dieselbe kanonische Eigenschaft mehr als einmal zu inkompatiblen Werten auf, sollen sie einen Konflikt zurückgeben. Sie dürfen nicht stillschweigend einen Wert auswählen.

## Strenge Referenz: Die Zugehörigkeit ist Teil der Anforderung

??? example "Quelltext oder Befehle anzeigen"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.load-bearing"
      propertySet = "axioval:example.ifc.pset-wall-common"
    }
    ```

Jetzt sind beide Tatsachen normativ:

1. die Eigenschaft ist `LoadBearing`; und
2. sie ist über den externen Container verbunden, der `Pset_WallCommon` zugeordnet ist.

Eine passende Eigenschaft in einem anderen Set reicht nicht aus.

=== "Eine lose Referenz verwenden, wenn"

    - die Anforderung semantische Information betrifft, nicht das Autorenlayout;
    - Exporteure gleichwertige Eigenschaften berechtigt in unterschiedlichen Sets ablegen; oder
    - eine Projektzuordnungsschicht Quellen bereits kanonisiert.

=== "Eine strenge Referenz verwenden, wenn"

    - Lieferanforderungen ein Standard-Property-Set vorschreiben;
    - Interoperabilität von der genauen Container-Platzierung abhängt; oder
    - die Prüfung gezielt die Schemakonformität kontrolliert.

## Container-unabhängige Auflösung bleibt fail-closed

Wenn `propertySet` fehlt, muss ein Adapter:

1. das kanonische Eigenschaftskonzept dem aktiven Modellschema zuordnen;
2. Vorkommen über unterstützte Eigenschaftscontainer hinweg sammeln;
3. „fehlend“ melden, wenn kein Vorkommen vorhanden ist;
4. typkorrekte Vorkommen nur zusammenführen, wenn ihre semantischen Werte übereinstimmen; und
5. „widersprüchlich“ oder „ungültig“ melden, wenn Werte nicht übereinstimmen oder nicht typisiert werden können.

Er darf niemals einfach die erste gleichnamige Eigenschaft akzeptieren, auf die er trifft.

## IFC-Beziehungskontext

In IFC ist ein Objekt über [`IfcRelDefinesByProperties`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelDefinesByProperties.htm) mit Eigenschaftsdefinitionen verbunden, und ein Property Set gruppiert benannte Eigenschaften. Axioval entfernt diese Beziehung nicht. Jede Anforderung kann entscheiden, ob die **Containeridentität** wesentlich ist.

Die offizielle IFC-4.3.2-Dokumentation zu [`Pset_WallCommon`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/Pset_WallCommon.htm) führt sowohl `LoadBearing` als auch `IsExternal` als boolesche Einzelwert-Eigenschaften auf. Das macht sie zu einer guten Demonstration, aber nicht zu einem Grund, Eigentum von Eigenschaften durch Property Sets im allgemeinen Schema festzuschreiben.
