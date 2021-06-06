# Bisher verwendete Werte für improvements Dict.

Das Improvements Dict hat einen möglichst unique _key_, welcher im Format
_kategorie_._effekt_(._subeffekt_) ist, z.B.

quality.lucky
metatype.reach


# Pflichtfelder
Jeder Eintrag muss folgende beiden Keys haben:
__type__: Art der Verbesseung (s.u.)
__text__: Text/Label für die Quelle der Verbesserung für Tooltips etc.

Je nach Typ können weitere Felder hinzukommen.


# Optionen für das type Feld
## attribute
Verändert einen Attributswert des attributs _attribute_ um:

| propery      | Bedeutung
| ------       | -------
| augment      | Fügt _value_ zum Attribut hinzu  **IN**
| augment_max  | Fügt _value_ zum Maximum hinzu   **IN**

## derived
Verändert einen der abgeleiteten Werte. Welcher genau, steht in einem _property_
Feld, der Bonus steht im _value_ Feld.

| property         | Bedeutung
| ------           | -------
| reach            | Fügt _value_ zur Reichweite hinzu
| armor_ballistic  | Fügt _value_ zur ballistischen Panzerung hinzu
| armor_impact     | Fügt _value_ zur Stoß-Panzerung hinzu


## lifestyle
Verändert aspekte des Lebensstils. Was genau steht in einem _property_ Feld,
und die Veränderung in einem _value_ Feld.

| property         | Bedeutung
| ------           | -------
| cost_increase    | Verändert die Kosten des Lebensstils um _value_ Prozent (z.B. 50 = +50%)


## special
Besondere Effekte, meist eher in Bezug auf das Programm selbst. Dafür gibt es dann
einen Key _effect_, welcher das ganze triggert:

| effect           | Bedeutung
| ------           | -------
| enable_magic     | Fügt ein MAG Attribute mit Natürlichem Wert 1 hinzu.
| enable_resonance | Fügt ein MAG Attribute mit Natürlichem Wert 1 hinzu.
| crittertab       | Aktiviert die Tab für Critter