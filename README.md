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


# Miten tätä saadaan käyttökuntoon
1. Asenna virtuaaliympäristö ja riippuvaisuudet juurijakemistosta. Saatat joutua kirjoittamaan **python3** pelkän **python** sijasta

Linux/macOS:
```bash
python -m venv venv
# Odota että kansio on luotu
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
python --version
flask --version
```

Windows (PowerShell):
```powershell
python -m venv venv
# Odota että kansio on luotu
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install flask
python --version
flask --version
```

Windows (Command Prompt):
```bat
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install flask
python --version
flask --version
```

2. Jos käytät uv:tä, projektiriippuvuudet ja virtuaaliympäristö voidaan asentaa komennolla **`uv sync`**.
3. SIIRRY hakemistoon **"src"**. "src" toimii tässä toteutuksessa sovelluksen juurihakemistona siinä missä itse juurihakemisto on koko projektin juurihakemisto. Kaikki mitä ajat tämän jälkeen terminaalissa on tarkoitus ajaa kansion **src** sisällä

4. Luo tietokanta ajamalla pythonilla 

``` 
python create_database.py
```

Tai  suoraan sqlitellä:

```
sqlite3 database.db < schema.sql
```

5. Täytä tietokanta ajamalla pythonilla
``` 
python populate_database.py
```

Tai  suoraan sqlitellä:

```
sqlite3 database.db < populate.sql
```

6. Jos jokin menee pieleen (kuten vaikka luot tietokannan vahingossa juurihakemistoon etkä **src** kansioon josta mainittiin pari kohtaa aikaisemmin) tietokannan voi poistaa manuaalisesti tai alustaa uudestaan ajamalla
```
python wipe_database.py
```

# Miten tätä käytetään/testataan
1. Käynnistä serveri komennolla "flask run"
2. Navigoi osoitteeseen "[http://127.0.0.1:5000]" haluamallasi selaimella
3. Luo tunnus tai kirjaudu sisään sivuston ohjeiden mukaan
    - Tunne itsesi vapaaksi testaamaan vääriä salasanoja, virheellistä tunnuksenluontia tai perusluontoisia SQL-injektioita ja kerro palautteessasi tuloksista

4. Mallitunnuksen nimi on *Mikko* ja salasana *4*
5. Käyttäjän etusivulla pystyy tarkastelemaan olemassaolevia SQL-MONeja (tietokohteet) ja treenaamaan niitä (tietokohteiden muuttaminen)
6. Etusivulla on myös linkki uuden SQL-MONin luomiseen (tietokohteen lisääminen)
    - Nimen tulisi olla merkkijono ja arvojen positiivisia kokonaislukuja.
    - Koeta syöttää kykykenttiin jotain ei-numeerista
    - Koeta lähettää sivulle POST-request johon olet livauttanut merkkijonon pyydettyyn arvoon jonka pitäisi olla numeerinen. Ilmestyykö SQL-MON etusivullesi? Kaatuuko ohjel,a?