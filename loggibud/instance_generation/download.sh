# Download IBGE census data.
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/SP_Capital_20190823.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/MG_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/RJ_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/DF_20171016.zip

# Download geographic data from IPEA
wget -P ./data_raw -nc https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/33.gpkg

# Unzip.
unzip -d ./data_raw -o ./data_raw/SP_Capital_20190823.zip
unzip -d ./data_raw -o ./data_raw/MG_20171016.zip
unzip -d ./data_raw -o ./data_raw/RJ_20171016.zip
unzip -d ./data_raw -o ./data_raw/DF_20171016.zip