# Keskustelusovellus

### Tämä on Tietokantasovellus-kurssin web-sovelluksen harjoitustyö.

Keskustelusovellus on yksi kurssin kolmesta annetusta harjoitustyön esimerkkiaiheesta. 

## Sovelluksen kuvaus/tarkoitus
Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

## Sovelluksen ominaisuuksia (Lopullinen palautus):

### Käytössä olevat ominaisuudet
- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen
- Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun
- Käyttäjä voi poistaa lähettämänsä viestin tai muokata sen sisältöä
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana
- Käyttäjä voi tykätä viesteistä ja poistaa tykkäyksen
- Käyttäjä voi muokata luomansa ketjun otsikkoa. Käyttäjä voi myös poistaa ketjun.
- Käyttäjän syötteet validoidaan

### Kurssityön ulkopuolelle jääneet ominaisuudet
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
  - Nyt ylläpidolliset toimenpiteet tulee toteuttaa suoraan tietokannan kautta
- Salaiset keskusteluryhmät valituille käyttäjille

## Tuotantoversiota pääset testaamaan
https://juttu-app.fly.dev/

## Testausohjeet
- Kloonaa tämä repositorio omalle koneellesi 
```
git clone git@github.com:JuhoPaananen/Keskustelusovellus.git
```
- Luo kansioon .env-tiedosto ja määritä sen sisältö seuraanvanlaiseksi:
  - DATABASE_URL=postgresql:///user   [jossa user korvataan omalla käyttäjänimellä]
  - SECRET_KEY=salainen-avain
  
  Pyydetyn salaisen avaimen voi luoda esim. seuraavasti:
  ```
  python3
  import secrets
  secrets.token_hex(16)
  ```
- Seuraavaksi luodaan ja käynnistetään virtuaaliympäristö sekä asennetaan vaaditut riippuvuudet virtuaaliympäristöön
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
- Sovellus vaatii käynnissä olevan tietokannan toimiakseen. Käynnistä Postgre seuraavalla komennolla jos olet asentanut postgren kurssin ohjeiden mukaisesti:
  ```
  start-pg.sh
  ```

- Seuraavaksi voidaan luoda sovelluksen vaatima tietokantaskeema
```
psql < schema.sql
```

- Mikäli sovelluksen skeema sisältää saman nimisiä tauluja kuin testaajan ympäristössä jo on, testaaja joutuu luomaan uuden tietokannan ja valitsemaan sen testaamisen ajaksi.
```
psql < CREATE DATABASE name
psql < \connect name
```
Jos vaihdoit tietokantaa, tulee tämä uuden tietokannan nimi vaihtaa .env tiedostoon <user> kohdalle. Esim. jos luotiin tietokanta "testi", tulee .env tiedoston ensimmäinen rivi olla seuraava: DATABASE_URL=postgresql:///testi

- Skeeman luonnin jälkeen sovellus vaatii toimiakseen vielä vähintään yhden kategorian. Seuraavalla koodilla niitä syntyy kolme:
```
psql < INSERT INTO categories (name) VALUES ('Testaajan unelma'), ('Höpöhöpöt'), ('Täällä ei ole yhtään viestiä');
```

- Nyt sovellus on valmis käynnistettäväksi:
```
flask run
```
            
### Aloitathan rekisteröimällä uuden käyttäjän - HAPPY TESTING!
