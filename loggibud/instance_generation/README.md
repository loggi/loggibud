Instance generation
===================

This document includes steps on how we generate instances to to our problems. It also allows you to reproduce the instances provided on your problem sets.


# Generating instances


## Download public data

First we need to download the raw data from IBGE, IPEA and (\~350Mb - compressed). If you are running a UNIX-based system and have have `wget` and `unzip`, you can do:


```bash
./download.sh

```

If you don't, you can manually download the data through the following links:
* ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/


Make sure your final file structure looks like:

```
```