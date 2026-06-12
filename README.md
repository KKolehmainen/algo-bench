# algo-bench
Sovellus omien algoritmien ja testiajojen tietojen tallentamiseen sekä vertailuun.

## Sovelluksen toiminnot
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sovellukseen
- Käyttäjä pystyy lisäämään, muokaamaan ja poistamaan algoritmeja sekä niiden testiajojen tietoja
- Käyttäjä pystyy tarkastelemaan muiden käyttäjien algoritmeja sekä testiajoja
- Käyttäjä pystyy hakemaan muiden käyttäjien algoritmeja hakusanoilla 
- Käyttäjä pystyy lisäämään muiden algoritmeihin omia testiajoja
- Sovellus näyttää käyttäjän tilastoja algoritmeista ja testiajoista käyttäjäsivulla
- Algoritmeja voidaan luokitella ohjelmointikielen perusteella, kieliluokat on määritelty tietokannassa

## Sovelluksen asennus
Asenna `flask`-kirjasto:
````
$ pip install flask
````

Luo tietokannan taulut ja alusta:
````
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
````

Käynnistä sovellus:
````
$ flask run
````