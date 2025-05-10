# CLIMADA-BR

Climada-BR is a project of LABIC (Laboratory of Computational Intelligence from USP São Carlos), that seeks to improve hazard assesment in Brazil using LLM's (Large Language Models) for extracting event data from auternative sources. **This repository is a fork from the original [CLIMADA](https://github.com/CLIMADA-project/climada_python) which stands for CLIMate ADAptation and is a probabilistic natural catastrophe impact model**, that also calculates averted damage (benefit) thanks to adaptation measures of any kind (from grey to green infrastructure, behavioural, etc.). The installation Guide is at the end of the page.

## Introduction

Our proposal addresses the challenge of improving hazard assessment by extracting event data from alternative sources to enhance risk analysis and climate adaptation in Brazil. Hazards, dynamic events, or circumstances that can cause harm, play a significant role as crucial input parameters in modeling the impact of climatic events. For example, changes in weather patterns or the detection of invasive vector species exemplify hazards that significantly influence these models.

Hazards are fundamental for calibrating models, acting as key parameters to better understand the risks associated with climate change impacts. In this context, [CLIMADA](https://github.com/CLIMADA-project/) model, short for CLIMate ADAptation, serves as a probabilistic natural catastrophe impact model, encompassing the evaluation of averted damage (benefit) resulting from diverse adaptation measures, ranging from grey to green infrastructure and behavioral adaptations [1]. With these models, public managers and researchers can conduct risk analyses, taking into account the effects of climatic events based on local data. This enables the formulation of preventive plans and awareness strategies. Presently, CLIMADA offers historical and probabilistic event sets for various time horizons, spanning past, present, and future climates. However, CLIMADA faces limitations when directly applied to the Brazilian context. These limitations stem from a scarcity of local data and the intricate regional complexities present in Brazil.

The overarching idea of the CLIMADA-BR proposal is to develop an open-source software tailored for Brazilian decision-makers. This software aims to act as a facilitating tool for community participation and crowd-sourcing data collection. By enabling the extraction of hazards from diverse local sources, such as news, bulletins, and reports from public managers, CLIMADA-BR strives to facilitate comprehensive climate risk modeling. This, in turn, enhances decision-making processes and fosters community involvement in tracking climate change impacts at the local level.

## Proposal Information

Currently, CLIMADA is the first global platform for probabilistic multi-hazard risk modeling, incorporating uncertainty and sensitivity analyses. This model enables the assessment of natural hazard risks and the evaluation of adaptation options by comparing averted impacts to implementation costs. Hazard, in CLIMADA, is modeled as a probabilistic set of events, each representing intensity at geographical locations with an associated probability of occurrence. The risk of a single event is defined as its impact multiplied by its probability of occurrence. CLIMADA allows for globally consistent risk assessment from city to continental scale, considering historical data, future projections, and various adaptation options.

Our proposal is straightforward and has a direct impact on public managers, researchers, and stakeholders interested in monitoring and understanding the impact of climate change in impoverished regions. We propose extending the model to CLIMADA-BR, integrating Large Language Models (LLMs) for real-time hazard extraction from news, bulletins, and reports. This adaptation will significantly enhance the model's sensitivity to localized climate events, resulting in improved risk assessments for various societal sectors. The idea is to leverage significant advancements in LLMs to enrich the model's hazard database.

Our hypothesis is that the integration of Large Language Models (LLMs) into the CLIMADA-BR framework enhances the capacity to collect, classify, and extract hazards. This integration aims to provide a more accurate representation of climate impacts on a local scale, considering diverse regions in Brazil.

The LLMs employed will extract hazard events in the 5W1H format (what, where, when, who, why, and how), an area where the project coordinator already has expertise, particularly in climate change events [2,3]. To assess the software's performance, we will conduct experiments on events modeling variables related to the detection of invasive vector species and disease transmission dynamics, providing insights for public officials to make informed decisions regarding public health impacts.

This project's development involves two Ph.D. students under the coordinator's supervision, who are currently engaged in the creation of artificial intelligence models for event extraction and sensing. These students bring valuable expertise to the initiative, contributing to the advancement of the project's objectives.

## Path to impact

First, we will conduct rigorous testing and validation of the CLIMADA-BR model, refining its functionalities based on feedback and real-world data. Simultaneously, we will collaborate with key stakeholders, including government agencies, public health institutions, and environmental organizations, to ensure the model's alignment with their needs. We will leverage existing collaborations with stakeholders such as the Center for Artificial Intelligence in Brazil ([C4AI](https://c4ai.inova.usp.br/research_2/#Climate_B_eng)), IBM, and FAPESP to ensure widespread implementation and impactful utilization of CLIMADA-BR in addressing climate-related hazards.

Once validated, the CLIMADA-BR framework will be disseminated through workshops, training sessions, and online platforms, targeting decision-makers, researchers, and the public. An open-source release of the model will be pivotal to encourage broader adoption and continuous improvement. To maximize the project's impact, we will establish partnerships with local communities, leveraging their knowledge and contributing to the model's enrichment.

## Descrição dos Módulos do Climada-BR

A classe `ClimadaBR` abrange todo o processo de armazenamento, processamento de dados e geração de resultados por meio de seus métodos. Ao instanciá-la, dois atributos obrigatórios devem ser fornecidos: o nome do arquivo contendo os dados de *hazard* (gerados por uma LLM) e o nome do arquivo com a *função de impacto* (criada com base em estudos que relacionam a intensidade dos eventos aos impactos causados). Além desses, diversos parâmetros secundários podem ser fornecidos para configurar o processamento dos dados.

Para exemplificação, apresentamos os resultados obtidos a partir de dois arquivos: um contendo dados sobre a dengue, processados por uma LLM a partir de notícias sobre o tema, e outro com a função de impacto baseada em um estudo da FIEMG, que correlacionava o número de casos de dengue com perdas econômicas — sejam estas decorrentes de tratamentos ou de afastamentos laborais.

![Arquitetura CLIMADA-BR](images/arquitetura.png)

### Hazard

O módulo *Hazard* armazena os dados dos fenômenos climáticos analisados. No Climada-BR, a interação com esse módulo se dá, principalmente, durante a instanciação do objeto ou via métodos como `ClimadaBR.Set_Hazard`.

No caso dos dados sobre dengue extraídos de notícias de 2023 por uma LLM, o formato adotado foi o de tabela, com linhas representando eventos e colunas contendo coordenadas, datas, descrições, severidade e intensidade:

![Tabela Hazard](images/arqHazard.png)

Essas tabelas são processadas para extrair e organizar as informações relevantes. Opcionalmente, uma etapa adicional pode ser realizada: o ajuste por uma GNN (Rede Neural de Grafo), mais especificamente uma GCN (Rede Convolucional de Grafo). A GCN é treinada com eventos de severidade extrema (muito alta ou muito baixa), utilizando como *features* uma codificação das descrições dos eventos e, como *labels*, os valores de severidade (1 para alta, 0 para baixa). Após o treinamento, o modelo define a severidade dos demais eventos, aumentando a coerência dos dados — visto que a LLM por classificar eventos de forma isolada pode ser incoerente em alguns casos.

O impacto desse ajuste pode ser visualizado com métodos como `ClimadaBR.Plot_HazReg`, que revela as alterações nos valores de severidade:

![Ajuste da GNN](images/GNN.png)

Depois de armazenadas as informações do *Hazard*, alguns métodos também podem ser utilizados para inspecionar esses dados, como o `ClimadaBR.Plot_Haz_Centroids`, que mostra as coordenadas de cada evento:

![Coordenadas dos Eventos](images/centroids.png)

E o `ClimadaBR.Dataframe_Print`, que exibe a estrutura dos dados armazenados, com linhas representando localizações e colunas contendo valores como latitude, longitude e intensidade de cada evento nessas coordenadas (observando-se que a maioria dos valores de intensidade é zero, pois cada evento afeta poucos locais, e a tabela contém 302 localizações):

![Dataframe Estruturado](images/HazDataframe.png)

### Entity

O módulo *Entity* é composto por dois elementos principais: *Exposure* (Área Afetada) e *Impact Function* (Função de Impacto).

#### Exposure

O módulo *Exposure* armazena informações sobre as áreas impactadas pelo fenômeno climático, podendo representar diversos parâmetros, como população, PIB, entre outros. No Climada-BR, utilizamos um método existente no CLIMADA que faz uso do arquivo `gpw_v4_population_count_rev11_2020_30_sec.tif`, que modela a distribuição populacional global em células de aproximadamente 1 km. Os parâmetros utilizados foram: país = Brasil, grade = 300 segundos de arco e valor socioeconômico = `'income_group'`, sendo que `'income_group'` representa o PIB multiplicado pelo grupo de renda do país (valores de grupo de renda vão de 1 a 4, sendo 1 igual a baixa e 4 a alta renda).

A visualização dos dados de *Exposure* pode ser feita com o método `ClimadaBR.Plot_Exposure`:

![Área Afetada](images/exposure.png)

#### Impact Function

A *Impact Function* é uma função que correlaciona a intensidade dos eventos com os valores de PAA (Porcentagem de Ativos Afetados) e MDD (Grau Médio de Dano). Essa função é definida por vários pontos que representam essa relação. No nosso projeto, ela foi construída de modo a aproximar os resultados de um conjunto de dados obtido do DATASUS, referente aos cinco primeiros meses de 2023, com os valores de dano financeiro propostos por um estudo da FIEMG, o qual relacionava 4,2 milhões de casos de dengue a um impacto financeiro de R$ 20,3 bilhões. No contexto do projeto, nosso objetivo foi adaptar a função de impacto para que resultasse em um impacto estimado de aproximadamente 900 milhões de dólares, valor correspondente à quantidade de infectados representada pelos dados do DATASUS.

Utilizamos, então, essa função previamente adaptada aos dados do DATASUS nos dados provenientes da análise de notícias realizada pela LLM. Caso os valores não se distanciem significativamente do esperado — como ocorreu —, isso serve como indicativo tanto da eficácia do projeto quanto da validade da função de impacto proposta. A *Impact Function* é fornecida ao objeto `ClimadaBR` durante sua instanciação ou por meio do método `ClimadaBR.Set_ImpFun`; em ambos os casos, é informado o nome de um arquivo contendo uma tabela com os pontos que definem a função, com colunas representando Intensidade, PAA e MDD.

Para visualizar a função, utiliza-se o método `ClimadaBR.Plot_ImpFun`, que gera o gráfico a seguir. O valor MDR (Taxa Média de Dano) é obtido pela multiplicação de MDD por PAA:

![Função de Impacto](images/ImpFun.png)

### Engine

O módulo *Engine*, ou *Impacto* (no CLIMADA original, a *Engine* engloba diversos submódulos; no Climada-BR, no entanto, ela foi restringida apenas ao módulo de *Impacto*, motivo pelo qual os termos são tratados como equivalentes), difere dos demais por armazenar os resultados dos cálculos, e não os dados de entrada. Ele é definido por meio do método `ClimadaBR.ComputeImpact`, que utiliza os dados previamente armazenados nos outros módulos para gerar um objeto de impacto. Esse objeto, ao ser criado, já executa os cálculos necessários para determinar diversos indicadores de impacto. Com o uso do método `ClimadaBR.Results`, obtém-se uma saída contendo um gráfico semelhante ao mostrado abaixo, além dos resultados em formato textual. No conjunto de dados utilizado, o valor da propriedade `aai_agg` (Impacto Médio Agregado) foi de aproximadamente 1,1 bilhão de dólares, representando o impacto médio anual:

![Impacto Computado](images/resultsIMG.png)

## Updates

### Minimalistic Example

At [CLIMADA-BR/doc/tutorial/TUTORIAL_BASE_CLIMADA_BR.ipynb](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/TUTORIAL_BASE_CLIMADA_BR.ipynb) we have a minimalistic example of how CLIMADA works through our ClimadaBR Class. You can also check Climada's official tutorials to learn more, you can start with [CLIMADA-BR/doc/tutorial/1_main_climada.ipynb](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/1_main_climada.ipynb).

To run every ClimadaBR tutorial in your machine you need to follow the installation guide below and also download the [gpw_v4_population_count_rev11_2020_30_sec.tif](https://drive.google.com/uc?id=1-3Skg9WOBDq8AyFV_WIdVsFDXG40qKCv&confirm=t&uuid=19db6326-d640-4af6-8fbf-51e7e479a338). This folder, along with some other files that are in the [CLIMADA-BR/doc/ClimadaBR_docs](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/ClimadaBR_docs) folder, need to be put in the SYSTEM_DIR of climada. Check out this README file [CLIMADA-BR/doc/ClimadaBR_docs/README.md](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/ClimadaBR_docs/README.md) to do it correctly.

### Climada-BR Class

At CLIMADA-BR/climada/ we have our class climadaBR which encapsulates the main functions used on our project, climadaBR has 5 python files: an 'init.py', 'climadaBR_def.py' (where the user can define the climadaBR object and interact with it), 'file_conversor.py' (which takes an file and organizes the data into a dataframe that can be passed to Climada to define a hazard), hazardRegularization.py (contain the process of using a GCN to regularize part of the data of some hazard file) and utils.py (which has some non excential tools used in the project).

The main functions a user will need to use climada are:

- ClimadaBR(haz_file, impctFunc_file, regulated, use_severity_threshold, severity_threshold, by_month_only, max_month, exp_lp, impf_set, haz): object creation, haz_file and impactFunc_file are the only necessary parameters, the rest is additional.
- ClimadaBR.Results(): to see the results of the Climada calculation.
- ClimadaBR.Plot_Exposure(): to see the Exposure used in the calculation.
- ClimadaBR.Plot_Haz_Centroids(): to see the centroids, which are the locations where our groups of events happened.
- ClimadaBR.Plot_ImpFun(): to see the impact function used.
- ClimadaBR.haz_reg.Results_Plots(): to see the changes made to the severity values by using a GCN to better classify the events.

This tutorial can show you how to use each of them [CLIMADA-BR/doc/tutorial/Tutorial_ClimadaBR.ipynb](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/Tutorial_ClimadaBR.ipynb).

If you want to see the other functions you can see the python files or our other tutorials to learn about them, but they are probably not necessary for you to use the application.

### DENGUE Hazard

In our project we thought of expanding the climate analysis function of Climada into a tool to analyse other types of events, in this case deseases and epydemics. So for our project we used dengue data from Brazil to compute the economic impact in a year, see this tutorial to have a full understanding of how we did that and which studies we took as base for our project [CLIMADA-BR/doc/tutorial/Tutorial_Dengue.ipynb](https://github.com/Labic-ICMC-USP/CLIMADA-BR/blob/main/doc/tutorial/Tutorial_Dengue.ipynb).
  
## Installation Guide

### Prerequisites

* Make sure you are using the **latest version** of your OS. Install any outstanding **updates**.
* Free up at least 10 GB of **free storage space** on your machine.
  Anaconda and the CLIMADA dependencies will require around 5 GB of free space, and you will need at least that much additional space for storing the input and output data of CLIMADA.
* Ensure a **stable internet connection** for the installation procedure.
  All dependencies will be downloaded from the internet.
  Do **not** use a metered, mobile connection!
* Install `Anaconda`, following the [installation instructions](https://docs.anaconda.com/anaconda/install/) for your OS.

### Instructions

1. If you are using a **Linux** OS, make sure you have ``git`` installed
   (Windows and macOS users are good to go once Anaconda is installed).
   On Ubuntu and Debian, you may use APT:
   
```
      apt update
      apt install git
```

   Both commands will probably require administrator rights, which can be enabled by prepending ``sudo``.

2. Create a **workspace directory**.
   To make sure that your user can manipulate it without special privileges, use a subdirectory of your user/home directory.
   Do **not** use a directory that is synchronized by cloud storage systems like OneDrive, iCloud or Polybox!

3. Open the command line and navigate to the workspace directory you created using ``cd``.
   Replace ``<path/to/workspace>`` with the path of the directory that contains the workspace folder:

```
      cd <path/to/workspace>
```

4. Clone CLIMADA-BR from its [GitHub repository](https://github.com/Labic-ICMC-USP/CLIMADA-BR.git).
   Enter the directory and check out the branch of your choice.

```
      git clone https://github.com/Labic-ICMC-USP/CLIMADA-BR.git
```

5. Create an Anaconda environment called ``climada_env`` for installing CLIMADA.
   Use the default environment specs in ``env_climada.yml`` to create it.
   Then activate the environment:

```
      conda env create -n climada_env -f requirements/env_climada.yml
      conda activate climada_env
```

6. Install the local CLIMADA source files as Python package using ``pip``:

```
      python -m pip install -e ./
```

hint:: Using a path ``./`` (referring to the path you are currently located at) will instruct ``pip`` to install the local files instead of downloading the module from the internet.
      The ``-e`` (for "editable") option further instructs ``pip`` to link to the source files instead of copying them during installation.
      This means that any changes to the source files will have immediate effects in your environment, and re-installing the module is never required.

7. Verify that everything is installed correctly by executing a single test:

```
      python -m unittest climada.engine.test.test_impact
```

   Executing CLIMADA for the first time will take some time because it will generate a directory tree in your home/user directory.
   If this test passes, great!
   You are good to go.


## References

[1] KROPF, Chahan M. et al. Uncertainty and sensitivity analysis for probabilistic weather and climate-risk modelling: an implementation in CLIMADA v. 3.1. 0. Geoscientific Model Development, v. 15, n. 18, p. 7177-7201, 2022.

[2] GÔLO, Marcos Paulo Silva; ROSSI, Rafael Geraldeli; MARCACINI, Ricardo Marcondes. Learning to sense from events via semantic variational autoencoder. Plos one, v. 16, n. 12, p. e0260701, 2021.

[3] MATTOS, Joao Pedro Rodrigues; MARCACINI, Ricardo M. Semi-supervised graph attention networks for event representation learning. In: 2021 IEEE International Conference on Data Mining (ICDM). IEEE, 2021. p. 1234-1239.
