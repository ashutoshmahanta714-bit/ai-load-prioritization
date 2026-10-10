"""Synthetic demand forecasting experiment; not trained on site measurements."""
import math,random,json
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def run():
    rng=random.Random(42)
    series=[100+18*math.sin(t*2*math.pi/96)+7*math.cos(t*2*math.pi/(96*7))+rng.gauss(0,2) for t in range(96*30)]
    x=[];y=[]
    for t in range(96,len(series)):
        x.append([series[t-1],series[t-2],series[t-96],math.sin(t*2*math.pi/96),math.cos(t*2*math.pi/96)])
        y.append(series[t])
    split=int(len(x)*.8)
    model=RandomForestRegressor(n_estimators=60,max_depth=8,random_state=42,n_jobs=-1)
    model.fit(x[:split],y[:split])
    report={'data':'synthetic only','split':'chronological 80/20','model':'RandomForestRegressor','test_mae_kw':mean_absolute_error(y[split:],model.predict(x[split:])),'persistence_mae_kw':mean_absolute_error(y[split:],[v[0] for v in x[split:]]),'deployment_status':'offline experiment; not connected to live allocation'}
    path=Path(__file__).parent/'forecast_metrics.json';path.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':run()
