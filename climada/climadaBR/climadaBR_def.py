"""
Define ClimadaBR.
"""
from climada.hazard import *
from climada.entity import *
from climada.engine import *
from climada.climadaBR.file_conversor import Conversor
from climada.climadaBR.hazardRegularization import HazReg
from climada.climadaBR.utils import progressBar
import numpy as np
import pandas as pd
from scipy import sparse
import xarray as xr
import os
from datetime import datetime

class ClimadaBR():
    """
    API of the ClimadaBR project.

    Attributes
    ----------
    exp_lp : LitPop
        Holds geopandas GeoDataFrame with metada and columns (pd.Series) defined in Attributes of Exposures class.
        LitPop exposure values are disaggregated proportional to a combination of nightlight intensity (NASA) and
        Gridded Population data (SEDAC). Total asset values can be produced capital, population count, GDP, or 
        non-financial wealth.
    impf_set : ImpactFuncSet
        Contains impact functions of type ImpactFunc.
    haz : Hazard
        Contains events of some hazard type defined at centroids.
    """

    def DefineExposures(self, countries, res_arcsec=30, fin_mode='pc', data_dir = SYSTEM_DIR):
        """Define the exposures, currently only by country name (countries) and socio-economic value (fin_mode)

        Parameters
        ----------
        countries: list with str or int
            list containing country identifiers:
            iso3alpha (e.g. 'JPN'), iso3num (e.g. 92) or name (e.g. 'Togo')
        res_arcsec: float, optional
            Horizontal resolution in arc-sec.
            The default is 30 arcsec, this corresponds to roughly 1 km.
        fin_mode: str, optional
            Socio-economic value to be used as an asset base that is disaggregated
            to the grid points within the country:

            * 'pc': produced capital (Source: World Bank), incl. manufactured or
              built assets such as machinery, equipment, and physical structures
              `pc` is in constant 2014 USD.
            * 'pop': population count (source: GPW, same as gridded population).
              The unit is 'people'.
            * 'gdp': gross-domestic product (Source: World Bank) [USD]
            * 'income_group': gdp multiplied by country's income group+1 [USD].
              Income groups are 1 (low) to 4 (high income).
            * 'nfw': non-financial wealth (Source: Credit Suisse, of households only) [USD]
            * 'tw': total wealth (Source: Credit Suisse, of households only) [USD]
            * 'norm': normalized by country (no unit)
            * 'none': LitPop per pixel is returned unchanged (no unit)

            Default: 'pc'
        data_dir : Path, optional
            redefines path to input data directory. The default is SYSTEM_DIR.
        """

        # using gpw_v4_population_count_rev11_2020_30_sec.tif (NASA)
        self.exp_lp = LitPop.from_countries(countries=countries, res_arcsec=res_arcsec, fin_mode=fin_mode, data_dir = data_dir)
        self.exp_lp.check()

    def Set_Exposure(self, exp_lp : LitPop):
        
        print("=================\nDefining Exposure\n=================")

        self.exp_lp = exp_lp

        if(exp_lp == None):
            self.DefineExposures(['BRA'], 300, 'income_group')

    def Plot_Exposure(self):
        self.exp_lp.plot_raster()

    def HazardFromDF(self, df):
        """Define a hazard from dataframe
        """

        lat = df["lat"].to_numpy()
        lat = lat[~np.isnan(lat)]

        lon = df["lon"].to_numpy()
        lon = lon[~np.isnan(lon)]
        
        n_cen = len(lat) # number of centroids
        n_ev = df['n_events'].values[0] # number of events

        # A INTENSIDADE DOS EVENTOS, NO PROJETO, SERA ESTIMADA POR VALORES DEFINIDOS
        # NAS NOTICIAS, COM APOIO DE LLM. AQUI, GERAMOS RANDOM.
        intensity = sparse.csr_matrix((n_ev, n_cen))
        for n in progressBar(range(0, n_ev), prefix = 'Creating Hazard Object:', suffix = 'Complete', length = 50):
            intensity_aux = df["event"+str(n+1)].to_numpy()
            intensity_aux = intensity_aux[~np.isnan(intensity_aux)]
            intensity[n] = intensity_aux

        fraction = sparse.csr_matrix((n_ev, n_cen))

        event_name = []
        for i in range(1,n_ev+1): event_name.append("event"+str(i))

        event_date = []
        for i in range(0,n_ev): event_date.append(df.loc[i, 'date'])

        haz_type = df["haz_type"].values[0]

        self.haz = Hazard(haz_type=haz_type,
                    intensity=intensity,
                    fraction=fraction,
                    centroids=Centroids.from_lat_lon(lat, lon),  # default crs used
                    units='impact',
                    event_id=np.arange(n_ev, dtype=int),
                    event_name=event_name,
                    date=event_date,
                    orig=np.zeros(n_ev, dtype=bool),
                    frequency=np.ones(n_ev) / n_ev
        )

        self.haz.check()

    def Set_Hazard(self, haz_file, haz : Hazard = None, regulated = False, use_severity_threshold = False, severity_threshold = 0.1, by_month_only = False, max_month = 12):
        
        print("===============\nDefining Hazard\n===============")
        
        self.haz = haz

        if(haz == None):
            if(haz_file != None):
                if(regulated):
                    self.haz_reg = HazReg(haz_file)
                    haz_dt = self.haz_reg.get_df()
                else:
                    file_path = os.path.join(SYSTEM_DIR, haz_file)

                    # Load dengue data
                    haz_dt = pd.read_excel(file_path)

                self.haz_dt = Conversor.convert_news_data(haz_dt, use_severity_threshold, severity_threshold, by_month_only, max_month, regulated)

                self.HazardFromDF(self.haz_dt)

    def Set_Datasus_Hazard(self, haz_file, by_month_only = True, max_month = 12, minimum_cases = 100, by_pop_size=False):
        
        print("===============\nDefining Hazard\n===============")
        
        self.haz_dt = Conversor.convert_datasus_data(haz_file, by_month_only, max_month, minimum_cases, by_pop_size)
        self.HazardFromDF(self.haz_dt)

    def Plot_Haz_Centroids(self):
        self.haz.centroids.plot()

    def AddImpactFunc(self, imp_fun):
        """Takes a impact function and store it in the ImpactFuncSet

        Parameters
        ----------
        imp_fun : ImpactFunc
            Contains the definition of one impact function
        """
        # check if the all the attributes are set correctly
        imp_fun.check()

        # add the impact function to an Impact function set
        self.impf_set.append(imp_fun)
        self.impf_set.check()

    def ImpactFuncSetFromExcel(self, excel_file, data_dir=SYSTEM_DIR):
        """Define a ImpactFuncSet from a excel file
            Right now for excel with single ImpactFunc
        """

        self.impf_set = ImpactFuncSet()

        excel_file_path = os.path.join(data_dir, excel_file)

        df = pd.read_excel(excel_file_path)

        num = int(df["num"].values[0])

        for i in progressBar(range(0, num), prefix = 'Progress:', suffix = 'Complete', length = 50):
            str_i =str(i+1)

            haz_type = df["haz_type"].values[i]
            name = df["name"].values[i]
            intensity_unit = df["intensity_unit"].values[i]

            # PARAMETROS QUE IMPACT FUNCTION PRECISA
            # intensity: Intensity values
            # mdd: Mean damage (impact) degree for each intensity (numbers in [0,1])
            # paa: Percentage of affected assets (exposures) for each intensity (numbers in [0,1])

            intensity = df["intensity" + str_i].to_numpy()
            mdd = df["mdd" + str_i].to_numpy()
            paa = df["paa" + str_i].to_numpy()

            imp_fun = ImpactFunc(
                id=str_i,
                name=name,
                intensity_unit=intensity_unit,
                haz_type=haz_type,
                intensity=intensity,
                mdd=mdd,
                paa=paa,
            )

            self.AddImpactFunc(imp_fun)

    def Set_ImpFun(self, impctFunc_file, impf_set : ImpactFuncSet = None):

        print("============================\nDefining Impact Function Set\n============================")
        
        self.impf_set = impf_set

        if(impf_set == None):
            if(impctFunc_file != None):
                self.ImpactFuncSetFromExcel(impctFunc_file)

    def Plot_ImpFun(self):
        self.impf_set.plot()

    def ComputeImpact(self):
        """Computes Impact based on haz, impf_set and exp_lp
        """

        if(self.impf_set == None or self.haz == None):
            print("ImpactFuncSet or Hazard were not setup, you can use Set_Hazard or Set_ImpFun to set them later to ComputeImpact.")
        else:

            print("================\nComputing Impact\n================")

            # Get the hazard type and hazard id
            [haz_type] = self.impf_set.get_hazard_types()
            [haz_id] = self.impf_set.get_ids()[haz_type]
            self.exp_lp.gdf.rename(columns={"impf_": "impf_" + haz_type}, inplace=True)
            self.exp_lp.gdf['impf_' + haz_type] = haz_id
            self.exp_lp.gdf

            # Compute impact
            self.imp = ImpactCalc(self.exp_lp, self.impf_set, self.haz).impact(save_mat=False)  # Do not save the results geographically resolved (only aggregate values)

    def Results(self):
        self.imp.plot_raster_eai_exposure()

        if(self.by_month_only):
            print(f"The impact of {len(self.haz.event_id)} groups of events were analised.")
            print("The events were grouped only by month (maybe because of data size),")
            print("for a more complete analysis use 'by_month_only = False'.")
        else:
            print(f"The impact of {len(self.haz.event_id)} groups of events were analised across {len(self.haz.centroids.lat)} different locations.")
            print("The events were grouped by month and location.")
        
        print("The results calculated by climada are the following:")
        print(f"Aggregated average annual impact calculated: {round(self.imp.aai_agg,0)} $")

    def __init__(self, haz_file, impctFunc_file, regulated = False, use_severity_threshold = False, severity_threshold = 0.1, by_month_only = False, max_month = 12,
                 exp_lp: LitPop = None,
                 impf_set: ImpactFuncSet = None,
                 haz: Hazard = None):

        self.by_month_only = by_month_only

        self.Set_Exposure(exp_lp)

        self.Set_Hazard(haz_file, haz, regulated, use_severity_threshold, severity_threshold, by_month_only, max_month)

        self.Set_ImpFun(impctFunc_file, impf_set)

        self.ComputeImpact()