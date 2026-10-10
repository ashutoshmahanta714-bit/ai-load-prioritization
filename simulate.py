import csv,random,math
from pathlib import Path
from controller import DEFAULT_LOADS,allocate,metrics

def run():
    rng=random.Random(42)
    result=[]
    for t in range(96):
        loads=[dict(r,demand_kw=round(r['demand_kw']*(1+.15*math.sin(t/96*2*math.pi)+rng.uniform(-.04,.04)),3)) for r in DEFAULT_LOADS]
        supply=max(0,75+20*math.sin(t/96*2*math.pi)- (35 if 40<=t<52 else 0))
        for method,fixed in [('Weighted priorities',False),('Fixed criticality',True)]:
            rows=allocate(loads,supply,fixed=fixed)
            result.append(dict(step=t,available_kw=supply,method=method,**metrics(rows,supply)))
    out=Path(__file__).parent/'simulation_results.csv'
    with out.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=result[0].keys());writer.writeheader();writer.writerows(result)
    print('Saved 96 simulated intervals for each of 2 methods:',out.name)
if __name__=='__main__':run()
