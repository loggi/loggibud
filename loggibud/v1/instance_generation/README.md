Instance generation
===================

This document describes how the data from our instances is synthesized from public data.
The sources of information are IBGE, IPEA, and OpenStreetMaps.


## Download public data

First we need to download the raw data from IBGE, IPEA and (\~350Mb - compressed). If you
are running a UNIX-based system and have `wget` and `unzip`, you can do:


```bash
./download.sh

```

If you don't, you can manually download the data through the following links and unzip
them into a `data_raw/` directory:

* IBGE Census microdata: ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/
* IBGE Census Geodata (by IPEA):
https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/33census_tract_2010.gpkg

> OBS: To maintain compliance with the defined file structure,
> the IPEA geographic data files must be renamed for "33.gpkg" format 
> (Removing the "census_tract_2010" substring).

Make sure your final file structure looks like:

```
data_raw/
├── 33.gpkg
├── RJ
│   └── Base informaçoes setores2010 universo RJ
│       ├── CSV
│       │   ├── Basico_RJ.csv
│       │   ├── Domicilio01_RJ.csv
│       │   ├── Domicilio02_RJ.csv
│       │   ├── DomicilioRenda_RJ.csv
│       │   ├── Entorno01_RJ.csv
│       │   ├── Entorno02_RJ.csv
│       │   ├── Entorno03_RJ.csv
│       │   ├── Entorno04_RJ.csv
│       │   ├── Entorno05_RJ.csv
│       │   ├── Pessoa01_RJ.csv
│       │   ├── Pessoa02_RJ.csv
│       │   ├── Pessoa03_RJ.csv
│       │   ├── Pessoa04_RJ.csv
│       │   ├── Pessoa05_RJ.csv
│       │   ├── Pessoa06_RJ.csv
│       │   ├── Pessoa07_RJ.csv
│       │   ├── Pessoa08_RJ.csv
│       │   ├── Pessoa09_RJ.csv
│       │   ├── Pessoa10_RJ.csv
│       │   ├── Pessoa11_RJ.csv
│       │   ├── Pessoa12_RJ.csv
│       │   ├── Pessoa13_RJ.csv
│       │   ├── PessoaRenda_RJ.csv
│       │   ├── Responsavel01_RJ.csv
│       │   ├── Responsavel02_RJ.csv
│       │   └── ResponsavelRenda_RJ.csv
│       └── EXCEL
│           ├── Basico_RJ.xls
│           ├── Domicilio01_RJ.xls
│           ├── Domicilio02_RJ.xls
│           ├── DomicilioRenda_RJ.XLS
│           ├── Entorno01_RJ.XLS
│           ├── Entorno02_RJ.XLS
│           ├── Entorno03_RJ.xls
│           ├── Entorno04_RJ.xls
│           ├── Entorno05_RJ.xls
│           ├── Pessoa01_RJ.xls
│           ├── Pessoa02_RJ.xls
│           ├── Pessoa03_RJ.xls
│           ├── Pessoa04_RJ.xls
│           ├── Pessoa05_RJ.xls
│           ├── Pessoa06_RJ.xls
│           ├── Pessoa07_RJ.xls
│           ├── Pessoa08_RJ.xls
│           ├── Pessoa09_RJ.xls
│           ├── Pessoa10_RJ.xls
│           ├── Pessoa11_RJ.xls
│           ├── Pessoa12_RJ.xls
│           ├── Pessoa13_RJ.xls
│           ├── PessoaRenda_RJ.xls
│           ├── Responsavel01_RJ.xls
│           ├── Responsavel02_RJ.xls
│           └── ResponsavelRenda_RJ.xls
├── RJ_20171016.zip
```

# Setup an OSRM distance server

To be able to compute distances over streets, you should download and run an
OSRM Server based on OpenStreetMaps. This can be done with the following steps:

1. Download and install docker according to your operational system.
2. Download the [precompiled distance files](https://loggibud.s3.amazonaws.com/osrm/osrm.zip) (5.3Gb compressed, 12.6Gb decompressed).
3. Extract the files into an `osrm` directory.
3. Run an OSRM backend container with the following command:

```
docker run --rm -t -id \
    --name osrm \
    -p 5000:5000 \
    -v "${PWD}/osrm:/data" \
    osrm/osrm-backend osrm-routed --algorithm ch /data/brazil-201110.osrm --max-table-size 10000
```

# Running the generation pipeline

Next, you can effectively generate the instances with a simple Python script:

```
python -m loggibud.v1.instance_generation.generate
```
