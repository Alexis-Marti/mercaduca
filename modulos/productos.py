import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def obtener_productos():
    con = obtener_conexion()
    df = pd.read_sql("SELECT * FROM PRODUCTO", con)
    con.close()

    # Aseguramos que estas columnas estén presentes antes de convertir
    if "Fecha_entrada" in df.columns:
        df["Fecha_entrada"] = pd.to_datetime(df["Fecha_entrada"], errors="coerce")
    if "Fecha_vencimiento" in df.columns:
        df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

    return df

def actualizar_productos(df):
    con = obtener_conexion()
    cursor = con.cursor()
    registros_actualizados = 0

    for _, row in df.iterrows():
        try:
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
                str(row.get("Nombre_producto", "")),
                str(row.get("Descripcion", "")),
                float(row.get("Precio", 0)),
                str(row.get("Tipo_producto", "")),
                str(row.get("ID_Emprendimiento", "")),
                row["Fecha_entrada"].date() if pd.notnull(row.get("Fecha_entrada")) else None,
                row["Fecha_vencimiento"].date() if pd.notnull(row.get("Fecha_vencimiento")) else None,
                str(row.get("ID_Producto", ""))
            ))
            registros_actualizados += cursor.rowcount
        except Exception as e:
            st.error(f"Error al actualizar fila con ID {row.get('ID_Producto')}: {e}")

    con.commit()
    con.close()

    if registros_actualizados > 0:
        st.success(f"✅ Cambios guardados correctamente ({registros_actualizados} registro(s)).")
    else:
        st.warning("⚠️ No hubo registros actualizados.")

def eliminar_productos(ids_a_eliminar):
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
        st.warning("⚠️ No se eliminó ningún producto.")

def mostrar_productos():
    st.header("📦 Productos")

    # Cargar productos solo una vez
    if "df_productos" not in st.session_state:
        st.session_state.df_productos = obtener_productos()

    df = st.session_state.df_productos.copy()

    # Filtro
    nombres_unicos = df["Nombre_producto"].dropna().unique()
    nombre_seleccionado = st.selectbox("🔍 Buscar producto por nombre:",
                                       options=["Todos"] + sorted(nombres_unicos.tolist()), index=0)

    if nombre_seleccionado != "Todos":
        df = df[df["Nombre_producto"] == nombre_seleccionado]

    # Agregar columna de eliminación
    df["Eliminar"] = False

    edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed", key="editor_productos")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Guardar Cambios"):
            for _, row in edited_df.iterrows():
                producto_id = row["ID_Producto"]
                mask = st.session_state.df_productos["ID_Producto"] == producto_id
                st.session_state.df_productos.loc[mask, :] = row

            # Enviar los cambios reales a la BD
            actualizar_productos(st.session_state.df_productos.drop(columns=["Eliminar"]))

    with col2:
        if st.button("🗑️ Eliminar seleccionados"):
            productos_a_eliminar = edited_df[edited_df["Eliminar"] == True]["ID_Producto"].tolist()
            if productos_a_eliminar:
                eliminar_productos(productos_a_eliminar)
                # Quitar eliminados de session_state también
                st.session_state.df_productos = st.session_state.df_productos[
                    ~st.session_state.df_productos["ID_Producto"].isin(productos_a_eliminar)
                ]
            else:
                st.info("Selecciona al menos un producto para eliminar.")

# Para ejecución directa
if __name__ == "__main__":
    mostrar_productos()


