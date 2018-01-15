<header>

**Motivation**

Ein Privathaushalt in Deutschland gibt jeden Monat rund 100 € für Autokra

</header>



<main>



[TOC]



## Einführung

## Analyse

* Benzinpreiseentwicklung
* A
* B
* C




![benzin_preise_daily](images/benzin_preise_daily.jpg)

Quelle: [Adac Tankstellenvergleich][adac_tankstellen_vergleich]



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



![predictor](images/predictor.png)

#### Korrektion

### Routing



## Ergebnisse


## Auswertung

Wir haben uns entschieden, für die Auswertung uns um die Vorhersagen zu konzentrieren.

Ausgewertet werden Vorhersagen mit verfügbaren Preise der jeweiligen Station und Vorhersagen ohne verfügbare Preise der jeweiligen Station.

* Vorhersage mit verfügbare Preise

  Wir haben 100 Stationen mit Preisen ausgewählt und für jede Station ein Datum ausgweählt, aus dem 10 Mal vorhergesagt wurde, mit unterschiedlen Enddatum fürs Training. Für jede Station wurde den minimal, maximal und durschnittliche absoluten Fehler gemessen.

* Vorhersage ohne verfügbare Preise

  Wir haben 100 Stationen mit Preise ausgewählt und für jede Station ein Prediktor mit einer aternative Station vom Klassifier gegeben trainiert und 10 Mal Preise Vorhergesagt. Die Preise der originalen Station wurde benuzt als echte Werte für die Berechnung der Fehler. Für jede Station wurde den minimal, maximal und durchschnittliche abolute Fehler gemessen.

  ​

Der Benchmark wurde mit folgender Anweisung ausgeführt:

`python benzlim benchmark $informaticup2018_dir`


## Abschluss




</main>

<bold>hello</bold>

<strong>strong</strong>

<footer>

[adac_tankstellen_vergleich]: http://www.faz.net/aktuell/finanzen/meine-finanzen/geld-ausgeben/adac-tankstellenvergleich-shell-und-aral-am-teuersten-14404375.html	"Adac Tankstellengvergleich"
[focus_guenstig_tanken]: https://www.focus.de/auto/praxistipps/benzinpreise-guenstig-tanken-zur-richtigen-zeit-am-richtigen-ort_id_4902163.html	"Benzinpreise, guenstig tanken"
[demo]: blablabla	"{a, b, c, d, e, f, 2017}"
