import streamlit as st

st.title("🧱Concreto.")

st.header("Mezcla optima del concreto.")

st.subheader("¿Como es la mezcla optima del concreto?")

st.write("La mezcla optima del concreto es aquella que sea util según sus requerimientos.")

#Pestañas
tab1, tab2 = st.tabs(["Materiales del concreto.","¿Para que sea optima que necesita?."])

with tab1:
    st.subheader("Materiales:")
    st.write("- Arena" \
    "-Triturado o grava" \
    "-Cemento" \
    "-Agua")

with tab2:
    st.write("Lo que se necesita es saber su utilidad y así buscar cual es la mezcla optima para el concreto.")