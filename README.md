# Labyrinth Game

## Esittely
Olen tekemässä ohjelma, joka luo ja piirtää ruudulle labyrintin, sekä asettaa
pelaajan labyrintin vapaaseen ruutuun. Käyttäjän tehtävä on ohjata hiiri pois
labyrintistä. Hänellä on mahdollisuus luovuttaa, jolloin ohjelma näyttää oikea
ratkaisu kuljettamalla hiiri pois labyrintistä. Labyrintti tukee myös toisiaan
ylittäviä ja alittavia reittejä eli ei ole vain tasomainen. Labyrintin koon on
vapaasti annettavissa. Myös labyrintti voidaan tallentaa ohjelmasta tiedostoon.

Ohjelma käynnistetään Eclipsen tai python konsolin avulla. Käyttäjä pystyy
syöttämään nimen, muuttaa labyrintin kokoa ja lähtöpistettä. Myös on
mahdollista katsoa, miten labyrintti luodaan ja asettaa “häntä”,joka näyttää
kuluneen matkan.

Pelin aikana käyttäjä näkee peliajan ja konsolin, missä ovat pelin kommentit.
Oikeassa alakulmassa ovat kaksi painiketta “New Game” ja “Give Up”. Yllä on
taulukko, jossa näkyy parhaat pisteet.

## Tiedosto- ja kansiorakenne

- Koodit löytyy src kansiossa, jossa on vain pelin käynnistämisen tarvitavat koodit

## Asennusohje

- Ohjelma tarvitsee vain PyQt5 kirjastoa, joka saa asennettua ajamalla komentorivissa
seuraava komento:
//Huom: Nämä komennot ajetaan suoraan komentoriviltä, ei Python-tulkista
pip install pyqt5

- Komentorivi Windowsilla
	- Paina näppäínyhdistelmää ’Windowskey + r’. Kirjoita avautuneeseen laatikkoon ’cmd’ ja paina ok.
	
## Käyttöohje

- Painamalla oikeassa yläkulmassa download-painiketta "download.zip"
- Pura kansion sisältö esim. työpöydälle
- Avaa Eclpise ohjelma -> luon uusi PyDeV Project -> nimea sen esim. LabyrinthGame
- Siirrä kaikki tiedostot src-kansiosta "LabyrinthGame"-kansioon (Huom: vain sisältö, ilman srs-kansioa)
- Avaa main.py ja painaa "Run"-painiketta