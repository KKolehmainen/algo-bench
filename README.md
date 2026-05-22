# algo-bench
Sovellus omien algoritmien ja testiajojen tietojen tallentamiseen sekä vertailuun.

## Sovelluksen tulevat toiminnot
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sovellukseen
- Käyttäjä pystyy lisäämään, muokaamaan ja poistamaan algoritmeja sekä niiden testiajojen tietoja
- Käyttäjä pystyy tarkastelemaan muiden käyttäjien algoritmeja sekä testiajoja
- Käyttäjä pystyy hakemaan muiden käyttäjien algoritmeja hakusanoilla sekä mahdollisesti muilla kriteereillä
- Käyttäjä pystyy lisäämään muiden algoritmeihin omia testiajoja
- Sovellus näyttää käyttäjän tilastoja algoritmeista ja testiajoista
- Käyttäjä voi vertailla eri algoritmeja sekä testiajoja keskenään
- Algoritmeja sekä testiajoja voidaan luokitella eri luokkiin

## Sovelluksen asennus
Asenna `flask`-kirjasto:
````
$ pip install flask
````

Luo tietokannan taulut:
````
$ sqlite3 database.db < schema.sql
````

Käynnistä sovellus:
````
$ flask run
````