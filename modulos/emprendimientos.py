def mostrar_emprendimientos():
    st.header("Emprendimientos registrados")

    try:
        con = obtener_conexion()
        cursor = con.cursor()
        cursor.execute("SELECT ID_Emprendimiento, Nombre_emprendimiento, Nombre_emprendedor, Telefono, Estado FROM EMPRENDIMIENTO")
        emprendimientos = cursor.fetchall()

        if emprendimientos:
            for emp in emprendimientos:
                st.markdown(f"""
                    **ID:** {emp[0]}  
                    **Nombre:** {emp[1]}  
                    **Emprendedor:** {emp[2]}  
                    **Teléfono:** {emp[3]}  
                    **Estado:** {emp[4]}  
                    ---
                """)
        else:
            st.info("No hay emprendimientos registrados.")

    except Exception as e:
        st.error(f"❌ Error al cargar emprendimientos: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
