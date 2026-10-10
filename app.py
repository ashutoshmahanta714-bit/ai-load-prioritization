import streamlit as st
import pandas as pd
from controller import DEFAULT_LOADS,allocate,metrics
st.set_page_config(page_title='Adaptive Load Allocation',layout='wide')
st.title('Adaptive Load Allocation')
st.caption('Research prototype • simulated inputs • no live electrical switching')
st.info('Partial allocation represents a controllable load reducing demand. Switchable loads receive full supply or zero.')
power=st.sidebar.slider('Available power (kW)',0.,150.,70.)
weights=[st.sidebar.slider(label,0.,1.,value) for label,value in [('Criticality weight',.5),('Efficiency weight',.3),('Stability weight',.2)]]
loads=st.data_editor(pd.DataFrame(DEFAULT_LOADS),num_rows='dynamic',hide_index=True)
try:
    rows=allocate(loads.to_dict('records'),power,weights)
    m=metrics(rows,power)
    cols=st.columns(3)
    cols[0].metric('Demand',f"{m['demand_kw']:.1f} kW")
    cols[1].metric('Served',f"{m['served_kw']:.1f} kW")
    cols[2].metric('Critical coverage',f"{100*m['critical_coverage']:.1f}%")
    result=pd.DataFrame(rows)
    st.dataframe(result,hide_index=True)
    st.bar_chart(result.set_index('name')[['demand_kw','allocated_kw']])
    st.download_button('Download allocation CSV',result.to_csv(index=False),'allocation.csv')
    st.subheader('Fixed criticality baseline comparison')
    st.dataframe(pd.DataFrame([{'method':'Weighted priorities',**m},{'method':'Fixed criticality',**metrics(allocate(loads.to_dict('records'),power,fixed=True),power)}]),hide_index=True)
    st.caption('Stability is a user-supplied score. This dashboard does not calculate power flow or prove voltage/frequency stability.')
except (ValueError,TypeError,KeyError) as e:
    st.error(f'Check load entries and weights: {e}')
