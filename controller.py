"""Research demonstrator: allocation is not an electrical protection system."""
import math

DEFAULT_LOADS = [
 dict(name='Hospital',demand_kw=25,criticality=1.,efficiency=.9,stability=.9,controllable=False),
 dict(name='Water pump',demand_kw=20,criticality=.9,efficiency=.8,stability=.8,controllable=False),
 dict(name='Residential',demand_kw=30,criticality=.65,efficiency=.65,stability=.65,controllable=True),
 dict(name='Commercial shops',demand_kw=15,criticality=.55,efficiency=.55,stability=.55,controllable=False),
 dict(name='Street lighting',demand_kw=10,criticality=.35,efficiency=.35,stability=.35,controllable=True)]

def allocate(loads,available_kw,weights=(.5,.3,.2),fixed=False):
    if not math.isfinite(available_kw) or available_kw<0: raise ValueError('Available power must be finite and nonnegative')
    if len(weights)!=3 or any(not math.isfinite(w) or w<0 for w in weights) or sum(weights)<=0: raise ValueError('Invalid weights')
    weights=[w/sum(weights) for w in weights]
    rows=[]
    for load in loads:
        r=dict(load)
        if not math.isfinite(r['demand_kw']) or r['demand_kw']<0: raise ValueError('Invalid demand')
        scores=[r[k] for k in ('criticality','efficiency','stability')]
        if any(not math.isfinite(v) or not 0<=v<=1 for v in scores): raise ValueError('Scores must be between zero and one')
        r['priority']=r['criticality'] if fixed else sum(w*v for w,v in zip(weights,scores))
        rows.append(r)
    rows.sort(key=lambda r:(-r['priority'],r['name']))
    remaining=available_kw
    for r in rows:
        d=r['demand_kw']
        power=min(d,remaining) if r['controllable'] else (d if d<=remaining else 0.)
        r['allocated_kw']=power
        r['status']='Full' if power>=d else ('Partial' if power>0 else 'Shed')
        remaining-=power
    return rows

def metrics(rows,available_kw):
    demand=sum(r['demand_kw'] for r in rows)
    served=sum(r['allocated_kw'] for r in rows)
    critical=[r for r in rows if r['criticality']>=.8]
    cd=sum(r['demand_kw'] for r in critical)
    return dict(demand_kw=demand,served_kw=served,unserved_kw=demand-served,
                unused_kw=max(0,available_kw-served),critical_coverage=sum(r['allocated_kw'] for r in critical)/cd if cd else 1.)
