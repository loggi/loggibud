# Download IBGE census data.
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/RJ_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/DF_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/PA_20171016.zip

# Download geographic data from IPEA
# These files are indexed in "http://www.ipea.gov.br/geobr/metadata/metadata_gpkg.csv"
wget -P ./data_raw -nc https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/33.gpkg  # RJ
wget -P ./data_raw -nc https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/53.gpkg  # DF
wget -P ./data_raw -nc https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/15.gpkg  # PA

# Unzip.
unzip -d ./data_raw -o ./data_raw/RJ_20171016.zip
unzip -d ./data_raw -o ./data_raw/DF_20171016.zip
unzip -d ./data_raw -o ./data_raw/PA_20171016.zip

# Fix bug with DF file name
cd './data_raw/DF'
find . -maxdepth 1 -mindepth 1 -type d -execdir mv {} 'Base informaçoes setores2010 universo DF' \;
