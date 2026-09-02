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
          typeSystem = "https://github.com/axioval/mcs/tree/main/examples"
          name = "axioval:example.ifc.load-bearing"
        }
      }
    }
    ```

Die Definition ist nicht in einem Property Set verschachtelt. Ihre stabile ID kann von Selektoren, Vorlagen und Instanzen wiederverwendet werden. Ihr `ExternalName` gehört zum Beispielvokabular; die Definition bleibt daher projektlokal: `openbim.ifc` `0.2.0` enthält absichtlich keine verifizierten PSD/QTO-Vorkommen, und MCS erzeugt keinen externen IFC-Namen aus einem freien String.

## Lose Referenz: Die Eigenschaft zählt, der Container nicht

??? example "Quelltext oder Befehle anzeigen"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.is-external"
    }
    ```

Ein modellspezifischer Consumer löst das projektlokale Konzept auf und durchläuft die nativen Beziehungen des Modells. Die Eigenschaft darf in jedem unterstützten Container gefunden werden.

Implementierungen müssen ein deterministisches Verhalten bei Konflikten definieren. Löst dieselbe kanonische Eigenschaft mehr als einmal zu inkompatiblen Werten auf, sollen sie einen Konflikt zurückgeben. Sie dürfen nicht stillschweigend einen Wert auswählen.

## Strenge Referenz: Die Zugehörigkeit ist Teil der Anforderung

??? example "Quelltext oder Befehle anzeigen"
    ```pkl
    new Values.PropertyReferenceValue {
      property = "axioval:example.ifc.load-bearing"
      propertySet = "axioval:example.ifc.pset-wall-common"
    }
    ```

Jetzt sind beide lokalen Vokabularfakten normativ:

1. das Eigenschaftskonzept ist `axioval:example.ifc.load-bearing`; und
2. es ist mit dem lokalen Containerkonzept `axioval:example.ifc.pset-wall-common` verbunden.

Eine passende Eigenschaft in einem anderen Set reicht nicht aus.

=== "Eine lose Referenz verwenden, wenn"

    - die Anforderung semantische Information betrifft, nicht das Autorenlayout;
    - Exporteure gleichwertige Eigenschaften berechtigt in unterschiedlichen Sets ablegen; oder
    - eine Projektzuordnungsschicht Quellen bereits kanonisiert.

=== "Eine strenge Referenz verwenden, wenn"

    - das Projektvokabular genau einen Eigenschaftscontainer vorschreibt;
    - Interoperabilität von der genauen Container-Platzierung abhängt; oder
    - die Prüfung gezielt die Schemakonformität kontrolliert.

## Container-unabhängige Auflösung bleibt fail-closed

Wenn `propertySet` fehlt, muss ein Adapter:

1. das projektlokale Eigenschaftskonzept für den aktiven Modelladapter auflösen;
2. Vorkommen über unterstützte Eigenschaftscontainer hinweg sammeln;
3. „fehlend“ melden, wenn kein Vorkommen vorhanden ist;
4. typkorrekte Vorkommen nur zusammenführen, wenn ihre semantischen Werte übereinstimmen; und
5. „widersprüchlich“ oder „ungültig“ melden, wenn Werte nicht übereinstimmen oder nicht typisiert werden können.

Er darf niemals einfach die erste gleichnamige Eigenschaft akzeptieren, auf die er trifft.

## IFC-Beziehungskontext

In IFC ist ein Objekt über [`IfcRelDefinesByProperties`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcRelDefinesByProperties.htm) mit Eigenschaftsdefinitionen verbunden, und ein Property Set gruppiert benannte Eigenschaften. Axioval entfernt diese Beziehung nicht. Jede Anforderung kann entscheiden, ob die **Containeridentität** wesentlich ist.

Die offizielle IFC-4.3.2-Dokumentation zu [`Pset_WallCommon`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/Pset_WallCommon.htm) führt sowohl `LoadBearing` als auch `IsExternal` als boolesche Einzelwert-Eigenschaften auf. Das belegt die Quellenangabe des Beispiels, ist aber kein typisiertes Paketvorkommen und berechtigt MCS nicht, eine externe IFC-Identität zu erzeugen. Diese Bindung muss ein künftiger paket-eigener Template-Katalog liefern.
