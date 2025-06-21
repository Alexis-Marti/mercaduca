import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulos'))

import streamlit as st
from modulos.login import login
from modulos.ventas import mostrar_ventas
from modulos.abastecimiento import mostrar_abastecimiento
from modulos.registro_emprendimiento import registrar_emprendimiento

st.set_page_config(page_title="MERCADUCA", layout="centered")

# 🔐 Control de sesión
if "usuario" not in st.session_state or "tipo_usuario" not in st.session_state:
login() # Mostrar login si no hay sesión iniciada
else:
tipo = st.session_state["tipo_usuario"]
    
    st.sidebar.title("Menú")
    opcion = st.sidebar.selectbox("Ir a:", ["Ventas", "Abastecimiento", "Registrar Emprendimiento", "Cerrar sesión"])

    if opcion == "Ventas" and tipo == "Administrador":
        mostrar_ventas()
    elif opcion == "Abastecimiento" and tipo in ["Asistente", "Administrador"]:
        mostrar_abastecimiento()
    elif opcion == "Registrar Emprendimiento" and tipo in ["Asistente", "Administrador"]:
        registrar_emprendimiento()
    elif opcion == "Cerrar sesión":
        st.session_state.clear()
        st.rerun()
    else:
        st.warning("No tienes permiso para acceder a esta sección.")
