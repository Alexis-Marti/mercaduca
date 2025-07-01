import streamlit as st

# Importación de módulos
from modulos.login import login
from modulos.ventas import mostrar_ventas
from modulos.reporte_ventas import reporte_ventas
from modulos.abastecimiento import mostrar_abastecimiento
from modulos.registro_emprendimiento import registrar_emprendimiento
from modulos.registro_producto import registrar_producto
from modulos.emprendimientos import mostrar_emprendimientos
from modulos.productos import mostrar_productos
from modulos.inventario import mostrar_inventario

# Configuración de la página
st.set_page_config(page_title="MERCADUCA", layout="centered")

# Título principal con estilo
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
    .centered-title {
        text-align: center;
        font-size: 4em;
        font-weight: bold;
        color: #4b7045;
        margin-bottom: 0;
        font-family: 'Montserrat', sans-serif;
    }
    .subtext {
        text-align: center;
        font-size: 1.2em;
        color: #777777;
        margin-top: 0;
        font-style: italic;
    }
    </style>
    <div class="centered-title">MERCAGESTIÓN</div>
    <div class="subtext">Para MERCADUCA</div>
    """,
    unsafe_allow_html=True
)

# Estilo para logo en esquina inferior izquierda
st.markdown(
    """
    <style>
    .logo-bottom-left {
        position: fixed;
        bottom: 15px;
        left: 15px;
        width: 120px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True
)

# Mostrar logo
st.markdown(
    '<img class="logo-bottom-left" src="https://raw.githubusercontent.com/devilchez/mercaduca-1/main/img/logo.png">',
    unsafe_allow_html=True
)

# Control de sesión
if "usuario" not in st.session_state or "tipo_usuario" not in st.session_state:
    login()
else:
    tipo = st.session_state["tipo_usuario"]

    st.sidebar.title("Menú")
    opcion = st.sidebar.radio(
        "Ir a:",
        [
            "Ventas",
            "Reporte de ventas",
            "Abastecimiento",
            "Registrar Emprendimiento",
            "Gestionar Emprendimiento",
            "Registrar Productos",
            "Gestionar Productos",
            "Inventario",
        ]
    )

    st.sidebar.markdown("<br><hr><br>", unsafe_allow_html=True)

    if st.sidebar.button("🔓 Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

    # Navegación por roles
    if opcion == "Ventas" and tipo in ["Asistente", "Administrador"]:
        mostrar_ventas()
    elif opcion == "Reporte de ventas" and tipo in ["Administrador"]:
        reporte_ventas()
    elif opcion == "Abastecimiento" and tipo in ["Administrador"]:
        mostrar_abastecimiento()
    elif opcion == "Registrar Emprendimiento" and tipo in ["Administrador"]:
        registrar_emprendimiento()
    elif opcion == "Gestionar Emprendimiento" and tipo in ["Administrador"]:
        mostrar_emprendimientos()
    elif opcion == "Registrar Productos" and tipo in ["Administrador"]:
        registrar_producto()
    elif opcion == "Gestionar Productos" and tipo in ["Administrador"]:
        mostrar_productos()
    elif opcion == "Inventario" and tipo in ["Administrador"]:
        mostrar_inventario()
    else:
        st.warning("No tienes permiso para acceder a esta sección.")
