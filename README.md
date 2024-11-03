# Analizimi i Bizneseve në Republikën e Kosovës
Studimi master 2024/2025. Lënda "Paraqitja dhe vizualizimi i të dhënave". Projekt grupor "Analizimi i Bizneseve në Republikën e Kosovës".

Të dhënat zyrtare të ARBK-së
**Lidhja** 
- [ ] Faqja kryesore: `https://arbk.rks-gov.net`

Të dhënat e marra nga faqja `Open Businesses Kosova` 
**Lidhjet** 
- [ ] Faqja kryesore: `https://biznesetehapura.com`
- [ ] Faqja për marrjen e të dhënave: `https://biznesetehapura.com/info`

## Përmbajtja

- [Analizimi i Bizneseve në Republikën e Kosovës](#analizimi-i-bizneseve-në-republikën-e-kosovës)
  - [Përmbajtja](#përmbajtja)
  - [Rreth Projektit](#rreth-projektit)
  - [Struktura e Projektit](#struktura-e-projektit)
  - [Dokumentimi](#dokumentimi)
  - [Kërkesat](#kërkesat)
  - [Instalimi](#instalimi)

## Rreth Projektit

Projekti ka për qëllim mbledhjen, përgatitjen dhe pastrimin e të dhënave të bizneseve të Kosovës për të krijuar një dataset të pastër dhe të përgatitur për analiza të mëtejshme. Për këtë qëllim, janë përdorur teknika të ndryshme të para-procesimit për të përmirësuar cilësinë e të dhënave dhe për të krijuar fusha të reja të dobishme për analizë.

Ky projekt ka për synim të gjenerojë statistika të ndryshme për bizneset e Kosovës, duke përfshirë:

- **Analizën e bizneseve sipas aktiviteteve**  
- **Analizën sipas statusit dhe gjinisë**  
- **Analizën sipas komunave**  
- **Analizën e regjistrimeve ndër vite**  
- **Rritjen e bizneseve në kohë**  
- **Analizën sipas kapitalit dhe numrit të punëtorëve**  

Këto statistika do të ndihmojnë në kuptimin më të mirë të strukturës dhe trendeve të bizneseve në Kosovë.


## Struktura e Projektit

- `data/`: Dosja që përmban dataset-in e papërpunuar (`raw`) dhe atë të përpunuar (`processed`).
- `notebooks/`: Përmban notebook-e për analiza dhe vizualizime. TODO
- `docs/`: Dokumentacioni i fazave të projektit.
- `src/`: Skriptet Python për mbledhjen dhe përgatitjen e të dhënave, analizën, dhe përpunimin.
- `LICENSE`: Skedari i licencës së projektit.
- `README.md`: Skedari kryesor i përshkrimit të projektit.
- `requirements.txt`: Kërkesat për bibliotekat e nevojshme Python.

## Dokumentimi

Këtu mund të gjeni dokumentimin e fazave te projektit. 

[Faza e pare](docs/pergatitja_e_te_dhenave.md)


## Kërkesat

- [Python 3.8+](https://www.python.org/)
- Libraritë e përmendura në `requirements.txt`

## Instalimi

1. Klononi këtë depo nga GitHub:
   ```bash
   git clone https://github.com/dritonalija/Analizimi-i-Bizneseve-ne-Republiken-e-Kosoves.git

2. cd Analizimi-i-Bizneseve-ne-Republiken-e-Kosoves

   pip install -r requirements.txt
3. cd src 

   python data_preparation.py


> Ky projekt është i licencuar nën Licencën MIT. Kjo licencë u lejon përdoruesve të kopjojnë, modifikojnë dhe shpërndajnë këtë softuer për çdo qëllim, duke përfshirë edhe përdorime komerciale. Ndryshimet dhe përshtatjet e kodit janë të lejuara, për sa kohë që deklarata e të drejtës së autorit origjinal ruhet në të gjitha kopjet. Licenca MIT nuk garanton asnjë përgjegjësi ose garanci për përdorimin e këtij softueri.
