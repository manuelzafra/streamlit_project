import streamlit as st
import pandas as pd

# Configurar URL del Google Sheet
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQENySjFc7OKgton5OMkzTsK1ddUm58YZwQH1Zx5MsJC8iIt47srYzH6qUlj4dpr482YoG3y_eOhYb2/pub?gid=789450175&single=true&output=csv"

@st.cache_data
def load_exercises():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        # Añadir debugging
        st.write("Estructura del DataFrame:")
        st.write("Columnas:", df.columns.tolist())
        st.write("Primeras filas:", df.head())
        return df
    except Exception as e:
        st.error(f"No se pudo cargar los datos. Error: {e}")
        st.stop()

def main():
    st.title("Human Developmet – Exercises")
    
    # Cargar ejercicios
    exercises = load_exercises()
    
    # Mostrar información de debugging
    st.write("Columnas disponibles:", exercises.columns.tolist())
    
    # Verificar columnas y mostrar mensajes de log
    required_columns = {
        "Subfield/Document": "Nombre del subproyecto",
        "Exercise Title": "Título del ejercicio",
        "Section/Body District": "Sección del cuerpo",
        "Skill/Difficulty": "Nivel de dificultad",
        "GIF/Video link": "Enlace al video",
        "Tags": "Etiquetas"
    }
    
    for col, description in required_columns.items():
        if col not in exercises.columns:
            st.warning(f"⚠️ No se encontró la columna '{col}' ({description}). Algunas funciones podrían estar limitadas.")
    
    # Intentar usar las columnas que existan
    if "Subfield/Document" in exercises.columns:
        subprojects = exercises["Subfield/Document"].unique()
    else:
        subprojects = ["Proyecto Principal"]
        st.error("No se encontró la columna de subproyectos. Mostrando todos los ejercicios juntos.")
    
    st.header("Proyectos de Ejercicio")
    for subproject in subprojects:
        if "Subfield/Document" in exercises.columns:
            sub_df = exercises[exercises["Subfield/Document"] == subproject]
        else:
            sub_df = exercises
            
        # Calcular progreso solo si existe la columna Tags
      # Calcular progreso solo si existe la columna Tags
        if "Tags" in exercises.columns:
            try:
                # Convertir la columna Tags a string
                sub_df["Tags"] = sub_df["Tags"].astype(str)
                completed = sub_df[sub_df["Tags"].str.contains("completado", na=False)].shape[0]
            except:
                completed = 0
                st.warning("Error al procesar las etiquetas. No se mostrará el progreso correctamente.")
        else:
            completed = 0
            st.info("No se encontró la columna 'Tags'. No se mostrará el progreso.")
        # HASTA AQUÍ

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
        
        if "Subfield/Document" in exercises.columns:
            sub_df = exercises[exercises["Subfield/Document"] == subproject]
        else:
            sub_df = exercises
            
        for _, row in sub_df.iterrows():
            if "Exercise Title" in exercises.columns:
                st.subheader(row.get("Exercise Title", "Sin título"))
            
            if "Section / Body District" in exercises.columns:
                st.write(f"Sección: {row.get('Section / Body District', 'No especificada')}")
                
            if "Skill/Difficulty" in exercises.columns:
                st.write(f"Habilidad/Dificultad: {row.get('Skill/Difficulty', 'No especificada')}")
                
            if "GIF/Video link" in exercises.columns and pd.notna(row.get("GIF/Video link")):
                st.image(row["GIF/Video link"], use_column_width=True)
                
            if "Tags" in exercises.columns:
                st.write(row.get("Tags", "Sin etiquetas"))
                
            note = st.text_area(f"Notas para {row.get('Exercise Title', 'ejercicio')}", "")
            if st.button(f"Marcar como completado: {row.get('Exercise Title', 'ejercicio')}"):
                st.success(f"Ejercicio {row.get('Exercise Title', 'seleccionado')} marcado como completado.")

if __name__ == "__main__":
    main()