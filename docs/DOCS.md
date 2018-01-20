<header>
InformatiCup 2018 - Benzlim
------------------------------------------------------------

**Franck Awounang Nekdem**,  **Gerald Wiese**,  **Amin Akbariazirani** und **Lea Evers**
</header>

<main>

[TOC]

## Einführung

Die Tankstrategie ist ein wichtiger Bestandteil jeder Reise. Wann, an welcher Tankstelle und wie viel Tanken zu müssen um am günstigsten und effizientesten ans Ziel zu gelangen macht auf lange Sicht einen großen finanziellen Unterschied.
Benzlim ist eine Python basierte Software Lösung die Verbraucher und Entwickler nutzen können, um Benzinpreise vorherzusagen und den Effizientesten Tankstrategie zu erstellen.

## Analyse

* **Benzinpreisentwicklung**

* **Benzinpreisunterschiede**

  Der entscheidende Faktor für den Preisunterschied der verscheidenen Tankstellen ist die Marke.

 ![infografik-das-auf-und-ab-der](images/infografik-das-auf-und-ab-der.jpg)

*Quelle:* [Frankfurt Allgemeine Zeitung][faz_preis_zyklen] 

![infografik-das-auf-und-ab-der_2](images/infografik-das-auf-und-ab-der_2.jpg)

*Quelle:* [Frankfurt Allgemeine Zeitung][faz_preis_zyklen]

![benzin_preise_daily](images/benzin_preise_daily.jpg)

*Quelle:* [Frankfurt Allgemeine Zeitung][adac_tankstellen_vergleich]

Benzinpreisänderungen am Tag sind unabhängig von der Marke

[][{demo}]

[blabla]: demo
[hello]: https://www.focus.de/auto/praxistipps/benzinpreise-guenstig-tanken-zur-richtigen-zeit-am-richtigen-ort_id_4902163.html

## Ansatz

Um die Preise vorhersagen zu können werden die durchschnittlichen Benzinpreise in bestimmten Zeitspannen (Jährlich, Monatlich, Wöchentlich, Täglich, Stündlich, Minütlich) berechnet. Die erzeugten Daten werden zu einem Extrapolator übergeben, der einen Prädiktor für die Differenz zwischen der jeweiligen Zeiteinheit und die höheren Zeiteinheiten erzeugt. Der grundlagende Prädiktor summiert die durchschnittlichen jährlichen Prädiktionen mit die montalichen, wöchentlichen, täglichen, stündlichen und minutlichen Prädiktion auf und erzeugt die Vorhersage.

### Training

Für die weitere Verarbeitung werden die Daten gereinigt und optimal gespeichert. Um auf die Daten optimal zugreifen zu können, werden in der Trainingsphase die folgenden Schritte durchgeführt: 
1. Eine lokale Datenbank mit Stationinformationen wird erzeugt
2. Die Stationinformationen werden um die Verfügbarkeit der Preise, sowie das Datum des ersten gemeldeten Preises erweitert.

### Vorhersage

#### Klassifizierung

"S" ist die Menge aller bekannten Stationen und "S<sub>p</sub>" ist die Menge aller Stationen sowie die dazugehörigen Preisinformationen.
Die Klassifizierung gibt für eine Station "s" in "S" die passendste Station "s<sub>p</sub>" in "S<sub>p</sub>" aus.

![classifier](images/classifier.png)

#### Vorhersage

##### Prediktor

Pro Vorhersage wird ein Model trainiert.

* Es werden Preise ausgewählt, die in dem gleichen Stundenzeitslot sind, wie der Zeitstempel für die Vorhersage.
* "yearly_avg", "monthly_avg", "weekly_avg", "daily_avg", "hourly_avg" und "min_avg" sind jeweils die jährlichen, monatlichen, wöchentlichen, täglichen und stündlichen durchschnittlichen Preise.
* "monthly_rel", "weekly_rel", "daily_rel", "hourly_rel" und "min_rel" sind die Differenz zwischen jeweils den durchschnittlichen monatlichen, wöchentlichen, täglichen und stündlichen Preisen und den durchschnittlichen Preisen der höheren Zeiteinheit.
* "yearly_avg" wird zu einem Extrapolator übergeben, der ein Prädiktor für den jährlichen Durchschnittspreis erzeugt. Jede "_rel" Tabelle wird durch die Berechnung der Differenz zwischen dem passenden "_avg" und die Summe der Prädiktionen der höheren Zeiteinheiten erzeugt.
* Alle "_rel" werden zu einem Extrapolator übergeben, der einen Prädiktor für die Differenz zwischen der jeweiligen Zeiteinheit und die höheren Zeiteinheiten erzeugt.
* Der grundlagende Prädiktor summiert die durchschnittlichen jährlichen Prädiktionen mit die montalichen, wöchentlichen, täglichen, stündlichen und minutlichen Prädiktion auf und erzeugt die Vorhersage.


![predictor](images/predictor.png)

#### Korrektion

* Ein Subprädiktor, mit allen gespeicherten Preisen
* Wenn die berechnete Vorhersage eine Abweichung von 20%+ von dem Durchschnittspreis hat, wird der Durchschnittspreis als alternative ausgewählt.

### Routing

Basierend auf die Entfernung bis zur nächsten günstigsten Tankstelle und die Tankkapazität des Autos, wird die richtige Strecke und der zutankende Menge, berechnet.

## Ergebnisse


## Auswertung

Bei der Auswertung liegt der Fokus auf die vorhersage der Preise.
Ausgewertet sind sowohl Stationen mit verfügbaren Preisinformationen als auch Stationen die keine Daten zu deren Preisen zur verfügung gestellt haben.

* Vorhersagen mit verfügbaren Preisen

  Wir haben 1000 Stationen mit verfügbaren Preisinformationen ausgewählt und für jede dieser Stationen einen Zufallsdatum erzeugt.
  Mit der o. g. Informationen wurden 16 Vorhersagen mit jeweils unterschiedlichen Enddaten für das Training durchgeführt. Für jede Station wurden die maximalen und durchschnittlichen absoluten Fehler sowie die relativen durchschnittlichen Fehler gemessen.

* Vorhersagen ohne verfügbare Preise

  Wir haben 1000 Stationen mit verfügbaren Preisinformationen ausgewählt und für jede dieser Stationen einen Prediktor mit einer alternativen Station vom Klassifier ausgesucht.
  Mit der o. g. Informationen wurden 16 Vorhersagen durchgeführt. Diesbezüglich wurden die Preise der originalen Stationen als Bezugswert für die Berechnung der Fehler benutzt. Für jede Station wurden die maximalen und durchschnittlichen absoluten Fehler sowie die relativen durchschnittlichen Fehler gemessen.


Der Benchmark wurde mit folgender Anweisung ausgeführt:

`python benzlim benchmark --nb_stations 1000 --nb_predictions 16`

Durch die Ausführung der o. g. Anweisung werden die zwei Dateien `benchmark_with_prices.csv` und `benchmark_without_prices.csv` in `benzlim\out\` gespeichert.

Ein Abschnitt aus den Ergebnissen ist in der folgenden Tabelle aufgelistet. Hier ist "e" die Differenz zwischen der vorhergesagten Preisen "p<sub>p</sub>" und der Referenzpreis "p<sub>r</sub>".

* **Vorhersagen mit verfügbaren Preisen**

| station_id       | 6421  | 14554  | 6799   | 5049   | 10823  | 79     | 3607   | 12682  | 2885   |
| ---------------- | ----- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| $max(\|e\|)$     | 62    | 26     | 42     | 42     | 69     | 98     | 39     | 29     | 27     |
| $avg(\|e\|)$     | 30    | 18     | 29     | 15     | 34     | 27     | 24     | 20     | 20     |
| $avg(\|e\|/p_r)$ | 0.023 | 0.0135 | 0.0202 | 0.0108 | 0.0237 | 0.0217 | 0.0191 | 0.0151 | 0.0161 |

* **Vorhersagen ohne verfügbare Preise**

| base_station_id  | 2953   | 7655   | 58     | 30     | 0.0209 | 14018  | 15133 | 71     | 33     |
| :--------------- | ------ | ------ | ------ | ------ | ------ | ------ | ----- | ------ | ------ |
| used_station_id  | 7655   | 15133  | 13424  | 4      | 15164  | 14459  | 14184 | 14716  | 14184  |
| $max(\|e\|)$     | 58     | 71     | 46     | 72     | 60     | 39     | 43    | 37     | 45     |
| $avg(\|e\|)$     | 30     | 33     | 19     | 40     | 53     | 12     | 16    | 16     | 24     |
| $avg(\|e\|/p_r)$ | 0.0209 | 0.0238 | 0.0144 | 0.0303 | 0.0325 | 0.0082 | 0.012 | 0.0124 | 0.0178 |


Im Durchschnitt haben Preisvorhersagen für sowohl Stationen mit Preisinformationen als auch Stationen ohne Preisinformationen eine absolute Fehlerrate von 25 bis 40.

#### Bekante Probleme

* Der Speicherverbrauch ist proportionnel zur Anzahl der Prozessorkerne und kann beim Benchmarking zu Problemen führen
* Die Tankstrategie ist in ca. 5% der Fälle Inkonsistent
* "Multiprocessing" führt unter Windows zu Fehlern. Dementsprechend wird für Windows nur "Monoprocessing" verwendet

## Abschluss

### Ausblick

Benzlim ist der Stützpunkt für viele weitere Projekte die ein Effizienteres Routing für Autofahrer erbringen können. Diese wären bessere Routingalgorithmen, Reiseplanung Software usw.

</main>


[^fn][msk_dritter_jahr]

<strong>strong</strong>

<footer>

[adac_tankstellen_vergleich]: http://www.faz.net/aktuell/finanzen/meine-finanzen/geld-ausgeben/adac-tankstellenvergleich-shell-und-aral-am-teuersten-14404375.html	"Adac Tankstellengvergleich"
[focus_guenstig_tanken]: https://www.focus.de/auto/praxistipps/benzinpreise-guenstig-tanken-zur-richtigen-zeit-am-richtigen-ort_id_4902163.html	"Benzinpreise, guenstig tanken"
[faz_preis_zyklen]: http://www.faz.net/aktuell/finanzen/devisen-rohstoffe/beim-benzinpreis-bis-zu-30-cent-unterschied-am-tag-14869994.html	"Benzinpreis! Unterschiede am Tag"
[mtsk_dritte_jahr]: http://www.bundeskartellamt.de/SharedDocs/Publikation/DE/Berichte/Dritter_Jahresbericht_MTS-K.pdf	" Das 3. Jahr Markttransparenzstelle"
