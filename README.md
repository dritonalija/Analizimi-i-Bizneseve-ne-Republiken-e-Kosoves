# Analizimi i Bizneseve në Republikën e Kosovës
Studimi master 2024/2025. Lënda "Paraqitja dhe vizualizimi i të dhënave". Projekt grupor "Analizimi i Bizneseve në Republikën e Kosovës".

<table>
  <tr>
   <td>
     <img src="assets/uni-logo.png" alt="University Logo" width="200" >
    </td>
    <td>
      <h2>UNIVERSITETI I PRISHTINËS “HASAN PRISHTINA”</h2>
      <p><strong>Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike</p>
      <p><strong>Departamenti: </strong> Inxhinieri Kompjuterike</p>
      <p><strong>Programi: </strong>Inxhinieri Kompjuterike dhe Softuerike</p>
      <p><strong>Kodra e Diellit, p.n. - 10000 Prishtinë, Kosova</string>
    </td>
   
  </tr>
</table>
  

---

## Detajet e lëndës
- **Përgatitja dhe vizualizimi i të dhënave**
- **Dr. Sc. Mërgim H. HOTI**
- **Asst. Dr. Sc. Mërgim H. HOTI**
- **Niveli:** Master
- **Viti akademik:** 2024/2025

---


## Grupi punues
  - Driton Alija
  - Muhamed Zahiri
  - Jusuf Maksuti
  

Të dhënat zyrtare të ARBK-së
**Lidhja** 
- [ ] Faqja kryesore: `https://arbk.rks-gov.net`

Të dhënat e marra nga faqja `Open Businesses Kosova` 
**Lidhjet** 
- [ ] Faqja kryesore: `https://biznesetehapura.com`
- [ ] Faqja për marrjen e të dhënave: `https://biznesetehapura.com/info`

## Përmbajtja

- [Analizimi i Bizneseve në Republikën e Kosovës](#analizimi-i-bizneseve-në-republikën-e-kosovës)
  - [Detajet e lëndës](#detajet-e-lëndës)
  - [Grupi punues](#grupi-punues)
  - [Përmbajtja](#përmbajtja)
  - [Rreth Projektit](#rreth-projektit)
  - [Struktura e Projektit](#struktura-e-projektit)
- [Faza e parë - Para-Porcesimi i te dhenave](#faza-e-parë---para-porcesimi-i-te-dhenave)
  - [Kërkesat](#kërkesat)
  - [Struktura e te dhenave](#struktura-e-te-dhenave)
  - [Përgatitja e të Dhënave](#përgatitja-e-të-dhënave)
    - [Funksionet Kryesore:](#funksionet-kryesore)
    - [Standardizimi dhe Trajtimi i Vlerave që Mungojnë](#standardizimi-dhe-trajtimi-i-vlerave-që-mungojnë)
    - [Transformimi, Agregimi dhe Reduktimi i Dimensionit](#transformimi-agregimi-dhe-reduktimi-i-dimensionit)
  - [Mostrimi](#mostrimi)
  - [Statistika](#statistika)
  - [Datatype info](#datatype-info)
  - [Korrelacioni](#korrelacioni)
  - [Kërkesat](#kërkesat-1)
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

# Faza e parë - Para-Porcesimi i te dhenave
## Kërkesat

Para-procesimi për përgatitjen e të dhënave për analizë.

Mbledhja e të dhënave, definimi i tipeve të dhënave, kualiteti i të
dhënave.

Integrimi, agregimi, mostrimi, pastrimi, identifikimi dhe strategjia e
trajtimit për vlerat e zbrazëta.

Reduktimi i dimensionit, zgjedhja e nën bashkësisë së vetive, krijimi
i vetive, diskretizimi dhe binarizimi, transformimi.

## Struktura e te dhenave

Datat jane marre nga https://biznesetehapura.com/info per 10 vitet e fundit. Keto data jane bashkuar sebashku duke perdorur scripten merge_data.py

Struktura e te dhenave ne csv

| Emri i biznesit            | Statusi | Numri fiskal | Tipi i biznesit     | Kapitali | Numri i punëtorëve | Pronarë       | Gjinia e pronarit | Personat e autorizuar | Data e regjistrimit | Linku në ARBK                                                                 | Numri i regjistrimit | Komuna | Aktivitetet         |
|-----------------------------|---------|--------------|---------------------|----------|--------------------|---------------|-------------------|-----------------------|----------------------|--------------------------------------------------------------------------------|-----------------------|---------|----------------------|
| John Doe B.I.        | Aktiv   | 600917621    | Biznes individual  | 0        | 1                  | John Doe  | Mashkull          | John                 | 2013-01-01  | (http://arbk.rks-gov.net/page.aspx?id=1,38,103658)                        | 70920638              | Lipjan  | Aktivitete juridike |


Struktura pas procesimit

| Emri i biznesit | Statusi   | Tipi i biznesit         | Data e regjistrimit | Data e mbylljes | Komuna     | Kapitali | Numri i punëtorëve | Pronarë Mashkull | Pronarë Femër | Aktivitetet Encoded |
|-----------------|-----------|-------------------------|----------------------|-----------------|------------|----------|--------------------|------------------|---------------|----------------------|
| John Doe B.I.   | 1    | 1       | 2013-01-01          | 2023-01-01      | 1           | 0        | 1                  | 1                | 0             | [6]                 |


## Përgatitja e të Dhënave

Për të përgatitur të dhënat është përdorur skripta `data_preparation.py`.

Janë përdorur librari të ndryshme të Python-it si dhe ChatGPT për këshillime.

### Funksionet Kryesore:

- **load_data(file_path)**: Ngarkon të dhënat nga një skedar CSV.
- **datatype_format(df)**: Formaton kolonat në tipe të sakta (data dhe numra).
- **normalize_status(df)**: Normalizon kolonën `Statusi` dhe nxjerr datën për `Data e mbylljes`.
- **update_gender_column(df)**: Përcakton gjininë e pronarëve bazuar në emrat.
- **count_genders(df)**: Numëron pronarët sipas gjinisë në kolonat `Pronarë Mashkull` dhe `Pronarë Femër`.
- **encode_aktivitetet(df)**: Kodon kolonën `Aktivitetet` dhe ruan hartimin.
- **remove_duplicates(df)**: Heq rreshtat e dyfishtë bazuar në `Uid`.
- **handle_missing_values(df)**: Trajton vlerat që mungojnë.

### Standardizimi dhe Trajtimi i Vlerave që Mungojnë

Për të trajtuar vlerat që mungojnë janë përdorur disa strategji.

P.sh., për mungesën e gjinisë së pronarit, është përdorur libraria `gender-guesser` e Python-it për të përcaktuar gjininë nga emri (gjinia e pronarit nuk është në faqen zyrtare të ARBK).

Për mungesën e komunës, është krijuar një `crawler` (`arbk_crawler.py`) i cili, duke përdorur framework-un Playwright, shkon në faqen e ARBK, kërkon me emër biznesi dhe pasqyron ato të dhëna nga përgjigja në CSV. Kjo për shkak se ARBK ka mekanizma që mbrojnë fuqishëm marrjen e të dhënave nga crawler-at dhe gjithashtu përdor Google Recaptcha.

`Data e mbylljes` është përcaktuar nga `Statusi`, p.sh., `pasiv-2022/06/01`.

Të gjitha vlerat e bashkësive, sikurse `Statusi`, `Komunat`, `Tipi i Biznesit`, janë pasqyruar në një skedar `JSONL` dhe në të dhënat e procesuara vendosen vlera numerike për performancë më të mirë.

`Aktivitetet` i kodojmë si një listë.

### Transformimi, Agregimi dhe Reduktimi i Dimensionit

Duke u bazuar në strukturën aktuale, kemi krijuar disa kolona të reja, p.sh., `Pronarë Femër`, `Pronarë Mashkull` (për të përcaktuar numrin e pronarëve në një biznes).

Kemi larguar kolona të panevojshme, sikurse `Numri Fiskal`, `Numri i Regjistrimit`, emrat e pronarëve, etj.

Në `data_transformation.py`, kemi gjithashtu shembuj të binarizimit të kolonave, sikurse `Kapitali`, `Numri i punëtorëve` dhe `Business Age`.

## Mostrimi

Në skedarin `data_samples.py` janë bërë disa forma të thjeshta të zgjedhjes së mostrës.


## Statistika

Në skedarin `data_stats.py` janë bërë disa statistika me datat e procesuara.

## Datatype info

Në skedarin `dataset_info.py` janë gjinden përshkruhen të gjitha vetitë e dataset.

## Korrelacioni

Në skedarin `correlation_matrix.py` jipet matrixa e korrelacionit.



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
