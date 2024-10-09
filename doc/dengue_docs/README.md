# Dengue documentation

This file contains all the documentation from DENGUE hazard data and impact functions, to scripts and tutorials related to acquaring and modeling that data.

# FILES

The DENGUE data was taken from 4 main sources and are related to the following files:
- DENGBR23.dbc (DENGUE2023.xlsx)
- municipios.csv
- dengue_hazzards_news.xlsx
- DengueFunc.xlsx

## DENGBR23.dbc (DENGUE2023.xlsx)

This file is the source file for the hazard data, it contains DENGUE notifications from Brazil in the year of 2023. It is available for download from [datasus](https://datasus.saude.gov.br/transferencia-de-arquivos/#), in this site you can download many data files, the one we are using is in the 'SINAN' source, 'data' modality, 'DENG - Dengue' archive type, '2023' year and 'BR' federative unit.

After downloading, you will have an '.dbc' file which will need to be converted to a '.dbf' file using the [pysus](https://github.com/danicat/pysus) github repository. With an '.dbf' file you can open it with excel and then save it as a 'DENGBR23.xlsx' file for easier access.

This file is very big so for modeling our data I opened it and deleted the columns which aren't needed, the results are in file DENGUE2023.xlsx', which contains only the dates of the notifications of dengue cases and the ID of the municipality where it happened.

## municipios.csv

This file can be taken form the [mapaslivres](https://github.com/mapaslivres/municipios-br/blob/main/tabelas/municipios.csv) github, it contains information on all brazilian municips, including municipality id, name, population in 2021 and coordinates. Together with the DENGBR23.dbc it contains all data necessary for modeling the hazard.

## dengue_hazzards_news.xlsx

This file contains all the information for modeling the hazard, but its sources are from news articles and not researchs like 'DENGBR23.dbc'. Our objective is to have this information when computated by CLIMADA produce similar results to the data from the previous files.

## DengueFunc.xlsx

This file was made by trial and error to aproximate the impact calculation to a desired value. The desired value was taken from an [research](https://www.fiemg.com.br/wp-content/uploads/2024/03/Impactos-Economicos-Arboviroses-somente-efeito-induzido.pdf) made by FIEMG which estimates the economic impact of arboviruses based on the number of infected people.

Takin the value of 4.2 million infected people, the research arrives at the loss of 20.3 billion reais. Adapting to the data from the DENGBR23.dbc file, we were going to need an impact of 5.068112500 billion reais or 913.173423 million dolars, which the functions in this file gets quite close to.
