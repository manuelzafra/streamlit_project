import streamlit as st
import pandas as pd

# Configurar URL del Google Sheet
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQENySjFc7OKgton5OMkzTsK1ddUm58YZwQH1Zx5MsJC8iIt47srYzH6qUlj4dpr482YoG3y_eOhYb2/pub?output=csv"

# Cargar datos desde el Google Sheet
@st.cache_data
def load_exercises():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        return df
    except Exception as e:
        st.error("No se pudo cargar los datos. Verifica la URL.")
        st.stop()

# Interfaz de Streamlit
def main():
    st.title("Gestión de Ejercicios Físicos")
    
    # Cargar ejercicios
    exercises = load_exercises()

    # Página de inicio con tarjetas por Subfield/Document
    subprojects = exercises["Subfield/Document"].unique()
    st.header("Proyectos de Ejercicio")
    for subproject in subprojects:
        sub_df = exercises[exercises["Subfield/Document"] == subproject]
        completed = sub_df[sub_df["Tags"].str.contains("completado", na=False)].shape[0]
        total = sub_df.shape[0]
        progress = (completed / total) * 100 if total > 0 else 0

        with st.container():
            st.subheader(subproject)
            st.write(f"{completed}/{total} ejercicios completados")
            st.progress(progress / 100)
            if st.button(f"Ver {subproject}"):
                st.session_state["current_subproject"] = subproject
                st.experimental_rerun()

    # Página de subproyecto
    if "current_subproject" in st.session_state:
        subproject = st.session_state["current_subproject"]
        st.header(f"Subproyecto: {subproject}")
        sub_df = exercises[exercises["Subfield/Document"] == subproject]
        for _, row in sub_df.iterrows():
            st.subheader(row["Exercise Title"])
            st.write(f"Sección: {row['Section / Body District']}")
            st.write(f"Habilidad/Dificultad: {row['Skill/Difficulty']}")
            st.image(row["GIF/Video link"], use_column_width=True)
            st.write(row["Tags"])
            note = st.text_area(f"Notas para {row['Exercise Title']}", "")
            if st.button(f"Marcar como completado: {row['Exercise Title']}"):
                st.success(f"Ejercicio {row['Exercise Title']} marcado como completado.")

if __name__ == "__main__":
    main()
