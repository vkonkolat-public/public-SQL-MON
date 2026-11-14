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
Synkkaa juurifolderista, siitä joka sisältää pyproject.toml "uv sync" tai asentamalla riippuvuudet muulla tavalla jonka olet valinnut käyttää
Rakenna tietokanta ajamalla "src/create_database.py"
