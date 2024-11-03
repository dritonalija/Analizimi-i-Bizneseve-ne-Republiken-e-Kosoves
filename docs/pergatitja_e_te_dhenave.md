# Para-Porcesimi i te dhenave

## Kerkesat

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






