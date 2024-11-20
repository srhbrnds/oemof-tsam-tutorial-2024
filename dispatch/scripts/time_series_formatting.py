import pandas as pd
from pathlib import Path

DATAPACKAGE_FOLDER = Path(__file__).parent.parent
pv_profile=pd.read_csv(Path(DATAPACKAGE_FOLDER,"data","sequences","solar-pv_ground_profile.csv"), encoding='utf-8', delimiter=';',index_col='timeindex')
wind_profile=pd.read_csv(Path(DATAPACKAGE_FOLDER,"data","sequences","wind-onshore_profile.csv"), encoding='utf-8',delimiter=';',index_col='timeindex')

pv_profile['wind-profile']=wind_profile['ABW-wind-onshore-profile']
volatile_profile=pv_profile.rename(columns={'ABW-solar-pv_ground-profile':'pv-profile'})
volatile_profile.to_csv('volatile_profile.csv', encoding='utf-8', index=True)
print('check')

