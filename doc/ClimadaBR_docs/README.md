# Documentation

This README.md contains all the documentation needed for running ClimadaBR. The following sections will have explanations about each file, also scripts and tutorials related to acquaring them. Most of them are already in the ClimadaBR_docs folder (meaning you just need to copy and past them to the climada SYSTEM_DIR), the exception is the gpw-v4-population-count-rev11_2020_30_sec_tif foulder which needs to download externally cause its too big.

# FILES

The data needed for running [ClimadaBR Tutorial](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/Tutorial_ClimadaBR.ipynb) is taken from 3 main sources and are related to the following files / foulder:
- gpw-v4-population-count-rev11_2020_30_sec_tif foulder
- dengue_hazzards_news.xlsx
- DengueFunc.xlsx

## gpw-v4-population-count-rev11_2020_30_sec_tif foulder

This foulder contains the information used to define the type of exposure used in our calculations, you can dowload it here [gpw_v4_population_count_rev11_2020_30_sec.tif](https://drive.google.com/uc?id=1-3Skg9WOBDq8AyFV_WIdVsFDXG40qKCv&confirm=t&uuid=19db6326-d640-4af6-8fbf-51e7e479a338) or follow Climada's official explanation of how to get it:

1. Go to the [download page](https://beta.sedac.ciesin.columbia.edu/data/set/gpw-v4-population-count-rev11/data-download) on Socioeconomic Data and Applications Center (sedac).
2. You'll be asked to log in or register. Please register if you don't have an account.
3. Wait until several drop-down menus show up.
4. Choose in the drop-down menus: Temporal: single year, FileFormat: GeoTiff, Resolution: 30 seconds. Click “2020” and then "create download".
5. Copy the file "gpw_v4_population_count_rev11_2020_30_sec.tif" into the folder "~/climada/data". (Or you can run the block once to find the right path in the error message)

If you want know more about Exposures see the [Exposures tutorial](climada_entity_Exposures.ipynb).

## dengue_hazzards_news.xlsx

This file contains all the information for modeling the hazard, its sources are from news articles. Our objective is to have this information when computated by CLIMADA produce similar results to the data from researches. Many similar files which are not here were generated to achieve the desired results.

If you want know more about Hazards see the [Hazard tutorial](climada_hazard_Hazard.ipynb).

## DengueFunc.xlsx

This file was made by trial and error to aproximate the impact calculation to a desired value. The desired value was taken from an [research](https://www.fiemg.com.br/wp-content/uploads/2024/03/Impactos-Economicos-Arboviroses-somente-efeito-induzido.pdf) made by FIEMG which estimates the economic impact of arboviruses based on the number of infected people.

Takin the value of 4.2 million infected people, the research arrives at the loss of 20.3 billion reais. Adapting to the data from the DENGBR23.dbc file, we were going to need an impact of 5.068112500 billion reais or 913.173423 million dolars, which the functions in this file gets quite close to.

If you want know more about Impact Functions see the [Impact tutorial](climada_engine_Impact.ipynb).

# Putting those files in the climada SYSTEM_DIR

The SYSTEM_DIR is the folder "~/climada/data", copy the files into the folder. If an error of file not found show up when running one of the tutorials just check the correct folder in the error message.

# Extra Dengue Tutorial

During development we runned some simulations using datasus data, if you wish to see those simulations you can access the [Dengue Tutorial](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/Tutorial_Dengue.ipynb) . This research data was used as our goal during the process, our objective was to make the data taken from articles generate similar results to this research data. The next section will tell you about the files used and how to acquire them.

# OTHER FILES

- DENGBR23.dbc (DENGUE2023.xlsx)
- municipios.csv

## DENGBR23.dbc (DENGUE2023.xlsx)

This file is the source file for the hazard data, it contains DENGUE notifications from Brazil in the year of 2023. It is available for download from [datasus](https://datasus.saude.gov.br/transferencia-de-arquivos/#), in this site you can download many data files, the one we are using is in the 'SINAN' source, 'data' modality, 'DENG - Dengue' archive type, '2023' year and 'BR' federative unit.

After downloading, you will have an '.dbc' file which will need to be converted to a '.dbf' file using the [pysus](https://github.com/danicat/pysus) github repository. With an '.dbf' file you can open it with excel and then save it as a 'DENGBR23.xlsx' file for easier access.

This file is very big so for modeling our data I opened it and deleted the columns which aren't needed, the results are in file DENGUE2023.xlsx', which contains only the dates of the notifications of dengue cases and the ID of the municipality where it happened.

## municipios.csv

This file can be taken form the [mapaslivres](https://github.com/mapaslivres/municipios-br/blob/main/tabelas/municipios.csv) github, it contains information on all brazilian municips, including municipality id, name, population in 2021 and coordinates. Together with the DENGBR23.dbc it contains all data necessary for modeling the hazard.