import streamlit as st
from modulos.config.conexion import obtener_conexion
from datetime import date

def registrar_producto():
    if "usuario" not in st.session_state:
        st.warning("⚠️ Debes iniciar sesión.")
        st.stop()

    st.header("Registrar nuevo producto")

    # Formulario
    id_producto = st.text_input("ID del Producto")
    nombre_producto = st.text_input("Nombre del producto")
    descripcion = st.text_area("Descripción")
    precio = st.number_input("Precio", min_value=0.0, step=0.01)
    tipo_producto = st.selectbox("Tipo de producto", ["Perecedero", "No perecedero"])
    id_emprendimiento = st.text_input("ID del Emprendimiento (asociado)")

    # Campos adicionales si es perecedero
    fecha_entrada = None
    fecha_vencimiento = None
    if tipo_producto == "Perecedero":
        fecha_entrada = st.date_input("Fecha de entrada", value=date.today())
        fecha_vencimiento = st.date_input("Fecha de vencimiento", value=date.today())

    if st.button("Registrar"):
        if not (id_producto and nombre_producto and descripcion and precio and tipo_producto and id_emprendimiento):
            st.warning("⚠️ Por favor, comple

