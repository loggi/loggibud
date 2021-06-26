# Download IBGE census data.
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/RJ_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/DF_20171016.zip
wget -P ./data_raw -nc ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2010/Resultados_do_Universo/Agregados_por_Setores_Censitarios/PA_20171016.zip

# Download geographic data from IPEA
# These files are indexed in "http://www.ipea.gov.br/geobr/metadata/metadata_gpkg.csv"
wget -O ./data_raw/33.gpkg -nc 'https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/33census_tract_2010.gpkg'  # RJ
wget -O ./data_raw/53.gpkg -nc 'https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/53census_tract_2010.gpkg'  # DF
wget -O ./data_raw/15.gpkg -nc 'https://www.ipea.gov.br/geobr/data_gpkg/census_tract/2010/15census_tract_2010.gpkg'  # PA

# Unzip.
unzip -d ./data_raw -o ./data_raw/RJ_20171016.zip
unzip -d ./data_raw -o ./data_raw/DF_20171016.zip
unzip -d ./data_raw -o ./data_raw/PA_20171016.zip

# Ensure the standard of names of the directories generated 
STATES=('DF' 'PA' 'RJ')
for state in ${STATES[@]}; do
  if [[ -e "data_raw/${state}" ]]; then
    mv -v "$(find data_raw/${state}/Base*${state} -maxdepth 0)" "data_raw/${state}/Base informaçoes setores2010 universo ${state}"
  fi
done

