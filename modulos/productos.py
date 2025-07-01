import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def obtener_productos():
    """Obtiene todos los registros de PRODUCTO desde la base de datos."""
    con = obtener_conexion()
    df = pd.read_sql("SELECT * FROM PRODUCTO", con)
    con.close()

    # Convertimos las fechas a tipo datetime solo si existen
    if "Fecha_entrada" in df.columns:
        df["Fecha_entrada"] = pd.to_datetime(df["Fecha_entrada"], errors="coerce")
    if "Fecha_vencimiento" in df.columns:
        df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

    return df

def actualizar_productos(df):
    """Actualiza los registros de PRODUCTO en la base de datos."""
    con = obtener_conexion()
    cursor = con.cursor()
    registros_actualizados = 0

    for _, row in df.iterrows():
        cursor.execute("""
            UPDATE PRODUCTO 
            SET Nombre_producto=%s,
                Descripcion=%s,
                Precio=%s,
                Tipo_producto=%s,
                ID_Emprendimiento=%s,
                Fecha_entrada=%s,
                Fecha_vencimiento=%s
            WHERE ID_Producto=%s
        """, (
            str(row["Nombre_producto"]),
            str(row["Descripcion"]),
            float(row["Precio"]),
            str(row["Tipo_producto"]),
            str(row["ID_Emprendimiento"]),
            row["Fecha_entrada"].date() if pd.notnull(row["Fecha_entrada"]) else None,
            row["Fecha_vencimiento"].date() if pd.notnull(row["Fecha_vencimiento"]) else None,
            str(row["ID_Producto"])
        ))
        registros_actualizados += cursor.rowcount

    con.commit()
    con.close()

    if registros_actualizados > 0:
        st.success(f"✅ Cambios guardados correctamente ({registros_actualizados} registro(s) actualizado(s)).")
    else:
        st.warning("⚠️ No hubo registros actualizados. Verifica que los ID coincidan.")

def eliminar_productos(ids_a_eliminar):
    """Elimina productos por sus ID desde la base de datos."""
    if not ids_a_eliminar:
        return

    con = obtener_conexion()
    cursor = con.cursor()
    formato_ids = ','.join(['%s'] * len(ids_a_eliminar))

    cursor.execute(f"DELETE FROM PRODUCTO WHERE ID_Producto IN ({formato_ids})", tuple(ids_a_eliminar))
    registros_eliminados = cursor.rowcount

    con.commit()
    con.close()

    if registros_eliminados > 0:
        st.success(f"🗑️ Se eliminaron {registros_eliminados} producto(s).")
    else:
        st.warning("⚠️ No se eliminó ningún producto. Revisa si los ID existen.")

def mostrar_productos():
    """Muestra la tabla de PRODUCTO para edición y eliminación."""
    st.header("📦 Productos")

    if "df_productos" not in st.session_state:
        st.session_state.df_productos = obtener_productos()
        st.session_state.df_productos["Eliminar"] = False

    df = st.session_state.df_productos

    # Filtro por nombre de producto
    nombres_unicos = df["Nombre_producto"].dropna().unique()
    nombre_seleccionado = st.selectbox(
        "🔍 Buscar producto por nombre:",
        options=["Todos"] + sorted(nombres_unicos.tolist()),
        index=0
    )

    if nombre_seleccionado != "Todos":
        df_vista = df[df["Nombre_producto"] == nombre_seleccionado].copy()
    else:
        df_vista = df.copy()

    edited_df = st.data_editor(
        df_vista,
        num_rows="fixed",
        use_container_width=True,
        key="editor_productos"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Guardar Cambios"):
            # Actualiza los datos en session_state
            for idx, row in edited_df.iterrows():
                st.session_state.df_productos.loc[idx] = row

            # Luego actualiza en base de datos
            actualizar_productos(st.session_state.df_productos.drop(columns=["Eliminar"]))

    with col2:
        if st.button("🗑️ Eliminar seleccionados"):
            productos_a_eliminar = edited_df[edited_df["Eliminar"] == True]["ID_Producto"].tolist()
            if productos_a_eliminar:
                eliminar_productos(productos_a_eliminar)
                # Quita los eliminados de session_state
                st.session_state.df_productos = st.session_state.df_productos[
                    ~st.session_state.df_productos["ID_Producto"].isin(productos_a_eliminar)
                ]
            else:
                st.info("Selecciona al menos un producto para eliminar.")

# Para ejecución directa
if __name__ == "__main__":
    mostrar_productos()


