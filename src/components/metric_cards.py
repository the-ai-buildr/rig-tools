import streamlit as st
from numpy.random import default_rng as rng

def rig_stats():
    changes = list(rng(4).standard_normal(40))
    data = [sum(changes[:i]) for i in range(20)]
    delta = round(data[-1], 2)
    width =200
    row = st.container(horizontal=True, gap="small",width='stretch', vertical_alignment="distribute")
    with row:
        st.metric(
            "H&P 643", 456, 500, chart_data=data, chart_type="line", border=True)
        st.metric(
            "H&P 604", 10, delta, chart_data=data, chart_type="line", border=True)
        st.metric(
            "H&P 637", 10, delta, chart_data=data, chart_type="line", border=True)
        st.metric(
            "H&P 390", 10, delta,  chart_data=data, chart_type="line", border=True)
        st.metric(
            "Ensign 142", 10, delta,  chart_data=data, chart_type="line", border=True)
        st.metric(
            "Ensign 125", 10, delta, chart_data=data, chart_type="line", border=True)
    return row