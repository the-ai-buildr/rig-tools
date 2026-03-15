"""
Home page card components — layout cards for the homepage.
Migrated from sections/home/cards.py into the canonical components/ location.

Produced by: frontend-agent / streamlit-components skill
"""
import streamlit as st
from components.page_card import card


def home_page_cards():
   
    def card_1_content():
        cont = st.container()
        with cont:
            st.markdown("Card 1 content goes here")
            st.markdown("Card 1 content goes here")
            st.button("Button 1",type='primary', use_container_width=True, key="122")
        return cont 

    def card_1_footer():
        cont = st.container()
        with cont:
            st.button("The Ai Buildr © 2026",type='primary', use_container_width=True, key="125")
        return cont

    def card_2_content():
        cont = st.container()
        with cont:
            st.markdown("Card 2 content goes here")
            st.markdown("Card 2 content goes here")
            st.button("Button 2",type='primary',  use_container_width=True,key="123")
        return cont

    def card_2_footer():
        cont = st.container()
        with cont:
            st.button("The Ai Buildr © 2026",type='primary', use_container_width=True, key="124")
        return cont

    c1, c2 = st.columns(2, gap="small")
    cont = st.container()
    with cont:
        with c1:
            card(
                content=card_1_content(),
                footer=card_1_footer(),
            )
        with c2:
            card(
                content=card_2_content(),
                footer=card_2_footer(),
            )

    return cont
