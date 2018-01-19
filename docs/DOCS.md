<header>
InformatiCup 2018 - Benzlim
------------------------------------------------------------

**Franck Awounang Nekdem**,  **Gerald Wiese**,  **Amin Akbariazirani** und **Lea Evers**





</header>



<main>



[TOC]



## Einführung

## Analyse

* **Benzinpreiseentwicklung**

* **Benzinpreisunterschiede**

  Der Preisunterschied vom Benzin ist getrieben von der Marke.





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



[][]

## Ansatz

So ist unser Ansatz für das bla bla bla bla

### Training

Die Daten werden gereinigt und optimal gespeichert für ihre weitere Verarbeitung. Für einen optimalen Zugriff auf Daten in folgenden Schritten, wird in der Trainingsphase eine lokale Datenbank mit Stationinformationen erzeugt. Die Stationinformationen werden um die Verfügbarkeit der Preise , sowie das Datum der Verfügbarkeit vom ersten gemelden Preis erweitert.

### Vorhersage

#### Klassifiezierung

Seien $S$ die Menge aller bekannten Stationen und $S_p$ die Menge aller Stationen mit Preisinformationen.

Die Klassifizierung gibt für eine Station $s \in S$ die passendste Station $s_p \in S_p$.

![classifier](images/classifier.png)

#### Vorhersage

##### Prediktor

Pro Vorhersage wird ein Model trainiert.

* Es werden Preise selektiert, die in dem gleichen Stundenzeitlot sind, wie der Zeitstempel für die Prädiktion
* Seien $yearly\_avg$,  $monthly\_avg$, $weekly\_avg$, $daily\_avg$, $hourly\_avg$ und $min\_avg$ jeweils die  jährlichen, monalichen, wochentlichen, täglichen und stündlichen durchschnittlichen Preise.
* Seien $monthly\_rel$, $weekly\_rel$, $daily\_rel$, $hourly\_rel$ und $min\_rel$ Unterschied zwischen jeweils den monalichen, wochentlichen, täglichen und stündlichen durchschnittlichen Preisen und den durchschnittlichen Preisen der höheren Zeiteinheit.
* $yearly\_avg$ wird zu einem Extrapolator übergeben, der ein Prädiktor für ein für den jährlichen durschnttlichen Preis erzeugt. Jede $*\_rel$  Tabelle berechnet sich aus die Unterschiede zwischen dem passenden $*\_avg$ und die Summe der Prädiktionen der höheren Zeiteinheiten.
* Alle $*\_rel$ werden zu einem Extrapolator übergeben, der ein Prädiktor für den Unterschied zwischen der jeweiligen Zeitheinheit und die höheren erzeugt.
* Der grundlagende Prädiktor summiert die durchschnittle jährliche Prädiktion und relative montaliche, wochentliche, tägliche, stündliche und minutliche Prädiktion.



![predictor](images/predictor.png)

#### Korrektion

- Ein Subprädiktor, der alle Preise hat und 
- Es wird den Durschnitt der benutzen Preisen berechnett, der als Fallback benutzt wird, wenn der prädizierte Preis schänkt von mehr als 20% vom ihm.

### Routing



## Ergebnisse


## Auswertung

Wir haben uns entschieden, für die Auswertung uns um die Vorhersagen zu konzentrieren.

Ausgewertet werden Vorhersagen mit verfügbaren Preise der jeweiligen Station und Vorhersagen ohne verfügbare Preise der jeweiligen Station.

* Vorhersage mit verfügbare Preise

  Wir haben 1000 Stationen mit Preisen ausgewählt und für jede Station ein Datum ausgweählt, aus dem 16 Mal vorhergesagt wurde, mit unterschiedlen Enddatum fürs Training. Für jede Station wurde den  maximalen und durchschnittlichen absoluten Fehler sowie den relativen durchschnittlichen Fehler gemessen.

* Vorhersage ohne verfügbare Preise

  Wir haben 1000 Stationen mit Preise ausgewählt und für jede Station ein Prediktor mit einer aternative Station vom Klassifier gegeben trainiert und 16 Mal Preise Vorhergesagt. Die Preise der originalen Station wurden benuzt als Referenzwerte für die Berechnung der Fehler. Für jede Station wurde den  maximalen und durchschnittlichen absoluten Fehler sowie den relativen durchschnittlichen Fehler gemessen.



Der Benchmark wurde mit folgender Anweisung ausgeführt:

`python benzlim benchmark --nb_stations 1000 --nb_predictions 16

Es werden danach zwei Dateien `benchmark_with_prices.csv ` und `benchmark_without_prices.csv` in `benzlim\out\` gespeichert.

Ein Abschnit aus den Ergibnissen ist in folgenden Tabellen gelistet, wo  $e$ der Unterschied zwischen einen prädizierten Preis $p_p$ und den Referenzpreis $p_r$.

* **Vorhersagen mit verfübare Preise**

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



Im Durchschnitt haben Vorhersagen mit Preisen einen alsoluten Fehler zwischen 25 und 40. Absolute Fehler der Vorhersagen ohne Preise bewegen sich im selben Interval.



#### Benkannte Probleme

* Der Speicherverbrauch ist proportionnel zur Anzahl der Prozessorkerne und kann zu Problemen führen beim Benchmarking
* Die Tankstrategie ist in ca. 5% der Fälle Inkonsistenz
* Multiprozessing führt zu Fehlern unter Windows. Auf die Platform wird nur Monoprozessing angewendet

## Abschluss



### Ausblick




</main>

<bold>hello</bold>

[^fn][msk_dritter_jahr]

<strong>strong</strong>

<footer>

[adac_tankstellen_vergleich]: http://www.faz.net/aktuell/finanzen/meine-finanzen/geld-ausgeben/adac-tankstellenvergleich-shell-und-aral-am-teuersten-14404375.html	"Adac Tankstellengvergleich"
[focus_guenstig_tanken]: https://www.focus.de/auto/praxistipps/benzinpreise-guenstig-tanken-zur-richtigen-zeit-am-richtigen-ort_id_4902163.html	"Benzinpreise, guenstig tanken"
[faz_preis_zyklen]: http://www.faz.net/aktuell/finanzen/devisen-rohstoffe/beim-benzinpreis-bis-zu-30-cent-unterschied-am-tag-14869994.html	"Benzinpreis! Unterschiede am Tag"
[mtsk_dritte_jahr]: http://www.bundeskartellamt.de/SharedDocs/Publikation/DE/Berichte/Dritter_Jahresbericht_MTS-K.pdf	" Das 3. Jahr Markttransparenzstelle"
