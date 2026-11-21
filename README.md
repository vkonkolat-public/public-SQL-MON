# public-SQL-MON
Harjoitusprojekti TIetokannat ja Web-ohjelmointi -kurssille
Pieni HTML, Flask ja SQLite -pohjainen pelillistetty taulukoiden luomis- ja vertailu-toteutus


-    Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
-    Käyttäjä pystyy lisäämään sovellukseen käyttäjätiliinsä sidottuja SQLmoneja (pääsijaiset tietokohteet), antamaan näille muutamia vertailuun käytettäviä arvoja ja kirjoittamaan lyhyen kuvauksen. 
-    Käyttäjä pystyy hallinnoimaan omia SQLmonejaan tai päästämään ne vapaaksi (poistamaan). Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät SQLmonit.
-    Käyttäjä pystyy etsimään SQLmoneja niiden ominaisuuksien (WIP), kuten haastevalmiuden, perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että, muiden käyttäjien lisäämiä SQLmoneja.
-    Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän omistamat SQLmonit.
-    Käyttäjän on mahdollista valita SQLmoneilleen erilaisia luokitteluja, kuten lepo, treenaaminen ja haastevalmius
-    Käyttäjät voivat luoda toisen käyttäjän SQLmonille haasteen omalla SQLmonillaan, kahden SQLmonin väliset kamppailut ovat toissijaisia tietokohteita


# Miten tätä käytetään
1. Asenna reposition riippuvuudet ja luo virtuaaliympäristö juurihakemistosta käsin
- Kehityksessä on käytetty uv-kehityksenhallintajärjestelmää jolla riittää komento "uv sync"
- TODO: pip ohjeet ja virtuaaliympäristön luominen muilla tavoilla

2. SIIRRY hakemistoon "src" ja tarkista että virtuaaliympäristö on aktivoitu ja että projektinkehityksessä käytetty Python-versio on käytössä
- "flask --version" --> Kuuluu kertoa oma versionsa ja riippuvaisuuksiensa versiot
- "python --version" --> Kuuluu palauttaa 3.14

3. Aja pythonilla create_database.py
3. 1. Tai [database.db < schema.sql]
3. 2. Tai [cmd /c "sqlite3 database.db < schema.sql"]
4. Käynnistä serveri komennolla "flask run"
5. Navigoi osoitteeseen "[http://127.0.0.1:5000]" haluamallasi selaimella
6. Luo tunnus tai kirjaudu sisään sivuston ohjeiden mukaan

7. TODO: Selitys apin seisäisetstä toiminnasta 