"""
Define ClimadaBR.
"""
from climada.hazard import *
from climada.entity import *
from climada.engine import *
import numpy as np
import pandas as pd
from scipy import sparse
import xarray as xr
import os

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
    def __init__(self,
                 exp_lp: LitPop = None,
                 impf_set: ImpactFuncSet = None,
                 haz: Hazard = None):
        self.exp_lp = exp_lp
        self.impf_set = impf_set
        self.haz = haz

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
        self.exp_lp.plot_raster()

    def DefineHazards(self, ds, n_ev, haz_type):
        """Define the hazards based on xr.Dataset information and number of events

        Parameters
        ----------
        ds : xr.Dataset
            xarray dataset with all the hazard values
        n_ev: int
            number of events
        """

        intensity_sparse = sparse.csr_matrix(ds['intensity'].values)
        fraction_sparse = sparse.csr_matrix(ds['fraction'].values)
        centroids = Centroids.from_lat_lon(ds['latitude'].values, ds['longitude'].values)
        event_id = np.arange(n_ev, dtype=int)
        event_name = ds['event_name'].values.tolist()
        date = ds['event_date'].values
        orig = np.zeros(n_ev, dtype=bool)
        frequency = np.ones(n_ev) / n_ev

        self.haz = Hazard(haz_type=haz_type,
                    intensity=intensity_sparse,
                    fraction=fraction_sparse,
                    centroids=centroids,  # default crs used
                    units='impact',
                    event_id=event_id,
                    event_name=event_name,
                    date=date,
                    orig=orig,
                    frequency=frequency
        )

        self.haz.check()
        self.haz.centroids.plot()

    def DefineRandomHazards(self):
        """Define a random hypothetical hazard
        """
        lat = np.array([    -22.90685, -23.55052, -12.9714, -8.04728, -3.71722,
            -27.5954, -25.4296, -22.7556, -16.463, -2.81972,
            -9.6658, -12.2628, -8.0512, -22.8119, -3.71722,
            -15.601, -30.0346, -3.10194, -22.3789, -21.7611,
            -13.0166, -4.1008, -2.53073, -28.2639, -20.355,
            -23.8101, -22.9625, -14.8233, -19.0139, -11.4236,
            -23.7122, -21.7611, -22.9056, -23.967, -25.5163,
            -3.7973, -12.2552, -2.897, -14.8628, -1.4485,
            -7.71833, -25.4284, -17.2298, -8.7597, -20.6713,
            -12.9333, -21.6226, -18.7154, -4.3601, -25.9625])

        lon = np.array([    -43.1729, -46.63331, -38.5014, -34.8788, -38.5433,
            -48.548, -49.2713, -41.8787, -39.1523, -40.3097,
            -35.7353, -38.9577, -34.877, -43.1791, -38.5433,
            -38.097, -51.2177, -60.025, -41.778, -41.3307,
            -38.9224, -38.535, -44.3028, -48.6756, -40.2508,
            -45.7033, -42.3656, -40.0638, -39.7496, -37.3623,
            -45.8513, -41.3307, -43.1964, -46.2945, -48.6713,
            -38.5747, -38.9868, -41.1677, -40.8006, -48.5043,
            -34.9128, -49.064, -39.0104, -35.7025, -40.229,
            -38.9995, -41.059, -39.2536, -39.3044, -48.6356])

        # EM NOSSO PROJETO, CADA EVENTO SERA SEU PROPRIO CENTROIDE
        n_cen = 50 # number of centroids
        n_ev = 50 # number of events

        # A INTENSIDADE DOS EVENTOS, NO PROJETO, SERA ESTIMADA POR VALORES DEFINIDOS
        # NAS NOTICIAS, COM APOIO DE LLM. AQUI, GERAMOS RANDOM.
        intensity = sparse.csr_matrix(np.random.random((n_ev, n_cen)))
        fraction = intensity.copy()
        fraction.data.fill(1)

        event_name = []
        for i in range(1,n_ev+1): event_name.append('event_'+str(i))

        event_date = []
        for i in range(1,n_ev+1): event_date.append(721166+i)

        intensity_dense = intensity.toarray()
        fraction_dense = fraction.toarray()

        ds = xr.Dataset(
            {
                'intensity': (['event', 'centroid'], intensity_dense),
                'fraction': (['event', 'centroid'], fraction_dense),
                'event_date': (['event'], event_date)
            },
            coords={
                'latitude': (['centroid'], lat),
                'longitude': (['centroid'], lon),
                'event_name': (['event'], event_name)
            }
        )

        self.DefineHazards(ds, n_ev, "WS")

    def HazardFromExcel(self, excel_file, data_dir=SYSTEM_DIR):
        """Define a hazard from excel file
        """
        excel_file_path = os.path.join(data_dir, excel_file)

        df = pd.read_excel(excel_file_path)

        lat = df["lat"].to_numpy()

        lon = df["lon"].to_numpy()

        # EM NOSSO PROJETO, CADA EVENTO SERA SEU PROPRIO CENTROIDE
        n_cen = len(lat) # number of centroids
        n_ev = df['n_events'].values[0] # number of events

        # A INTENSIDADE DOS EVENTOS, NO PROJETO, SERA ESTIMADA POR VALORES DEFINIDOS
        # NAS NOTICIAS, COM APOIO DE LLM. AQUI, GERAMOS RANDOM.
        intensity = sparse.csr_matrix((n_ev, n_cen))
        for n in range(0, n_ev):
            intensity[n] = df["event"+str(n+1)].to_numpy()

        fraction = sparse.csr_matrix((n_ev, n_cen))

        event_name = []
        for i in range(1,n_ev+1): event_name.append("month"+str(i))

        event_date = []
        for i in range(1,n_ev+1): event_date.append(721166+i)

        intensity_dense = intensity.toarray()
        fraction_dense = fraction.toarray()

        ds = xr.Dataset(
            {
                'intensity': (['event', 'centroid'], intensity_dense),
                'fraction': (['event', 'centroid'], fraction_dense),
                'event_date': (['event'], event_date)
            },
            coords={
                'latitude': (['centroid'], lat),
                'longitude': (['centroid'], lon),
                'event_name': (['event'], event_name)
            }
        )

        haz_type = df["haz_type"].values[0]

        self.DefineHazards(ds, n_ev, haz_type)

    def AddImpactFunc(self, imp_fun):
        """Takes a impact function and store it in the ImpactFuncSet

        Parameters
        ----------
        imp_fun : ImpactFunc
            Contains the definition of one impact function
        """
        # check if the all the attributes are set correctly
        imp_fun.check()
        imp_fun.plot()

        # add the impact function to an Impact function set
        self.impf_set.append(imp_fun)
        self.impf_set.check()

    def DefineRandomImpactFuncSet(self):
        """Define a ImpactFuncSet with a single random ImpactFunc with id = 'WEBSENSORS'
        """

        haz_type = "WS"
        name = "WS Impact Function"
        intensity_unit = "ws impact"


        # provide RANDOM values for the hazard intensity, mdd, and paa
        # AQUI TAMBEM TEMOS QUE DEFINIR COM BASE NOS EVENTOS E COM APOIO DE LLM

        # PARAMETROS QUE IMPACT FUNCTION PRECISA
        # intensity: Intensity values
        # mdd: Mean damage (impact) degree for each intensity (numbers in [0,1])
        # paa: Percentage of affected assets (exposures) for each intensity (numbers in [0,1])

        intensity = np.linspace(0, 100, num=15)
        mdd = np.concatenate((np.array([0]), np.sort(np.random.rand(14))), axis=0)
        paa = np.concatenate((np.array([0]), np.sort(np.random.rand(14))), axis=0)

        imp_fun = ImpactFunc(
            id='WEBSENSORS',
            name=name,
            intensity_unit=intensity_unit,
            haz_type=haz_type,
            intensity=intensity,
            mdd=mdd,
            paa=paa,
        )
        self.impf_set = ImpactFuncSet()

        self.AddImpactFunc(imp_fun)

    def ImpactFuncSetFromExcel(self, excel_file, data_dir=SYSTEM_DIR):
        """Define a ImpactFuncSet from a excel file
            Right now for excel with single ImpactFunc
        """

        self.impf_set = ImpactFuncSet()

        excel_file_path = os.path.join(data_dir, excel_file)

        df = pd.read_excel(excel_file_path)

        num = int(df["num"].values[0])

        for i in range(0, num):
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

    def ComputeImpact(self):
        """Computes Impact based on haz, impf_set and exp_lp
        """
        # Get the hazard type and hazard id
        [haz_type] = self.impf_set.get_hazard_types()
        [haz_id] = self.impf_set.get_ids()[haz_type]
        self.exp_lp.gdf.rename(columns={"impf_": "impf_" + haz_type}, inplace=True)
        self.exp_lp.gdf['impf_' + haz_type] = haz_id
        self.exp_lp.gdf

        # Compute impact
        imp = ImpactCalc(self.exp_lp, self.impf_set, self.haz).impact(save_mat=False)  # Do not save the results geographically resolved (only aggregate values)

        imp.plot_raster_eai_exposure()

        print(f"Aggregated average annual impact: {round(imp.aai_agg,0)} $")