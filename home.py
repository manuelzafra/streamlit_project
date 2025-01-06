import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from typing import Literal

#Par ejecutar este script escribri streamlit run home.py 

# Configuración sticky headers
MARGINS = {
    "top": "2.875rem",
    "bottom": "0",
}

STICKY_CONTAINER_HTML = """
<style>
div[data-testid="stVerticalBlock"] div:has(div.fixed-header-{i}) {{
    position: sticky;
    {position}: {margin};
    background-color: white;
    z-index: 999;
}}
</style>
<div class='fixed-header-{i}'/>
""".strip()

# Contador para los contenedores sticky
count = 0

def sticky_container(
    *,
    height: int | None = None,
    border: bool | None = None,
    mode: Literal["top", "bottom"] = "top",
    margin: str | None = None,
):
    if margin is None:
        margin = MARGINS[mode]

    global count
    html_code = STICKY_CONTAINER_HTML.format(position=mode, margin=margin, i=count)
    count += 1

    container = st.container()
    container.markdown(html_code, unsafe_allow_html=True)
    return container

# Configuración de la página DEBE IR PRIMERO
st.set_page_config(
    page_title="Human Development – Exercises Database & Progress",
    page_icon="🏃",
    layout="centered"
)

# Aplicar CSS para ocultar anchor links y estilos adicionales
st.markdown("""
    <style>
    .stApp a.anchor-link {
        display: none;
    }
    div.stMarkdown {
        overflow: visible;
    }
    .table-of-contents {
        padding: 10px 0;
    }
    .table-of-contents + hr {
        margin: 0.5rem 0;
    }
    /* Estilos más específicos para el Go link */
    .table-of-contents a.go-link {
        color: #666666 !important;
        text-decoration: none !important;
        margin-left: 5px;
        transition: color 0.2s ease;
    }
    .table-of-contents a.go-link:hover {
        color: #000000 !important;
        text-decoration: none !important;
    }
    </style>
    <style>
    /* Ajustar el espaciado del divider */
    .table-of-contents + hr {
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar variables de entorno
#Para la versión local
#load_dotenv()
#GOOGLE_SHEET_CSV_URL = os.getenv("GOOGLE_SHEET_CSV_URL")

# Para la versión deployada
GOOGLE_SHEET_CSV_URL = st.secrets["GOOGLE_SHEET_CSV_URL"]

# Verificar si se cargó correctamente la URL
if not GOOGLE_SHEET_CSV_URL:
    st.error("Error: No se pudo cargar la URL del archivo .env")
    st.error("Verifica que:")
    st.error("1. El archivo .env existe en la carpeta correcta")
    st.error("2. El archivo contiene la línea: GOOGLE_SHEET_CSV_URL='tu_url_aquí'")
    st.error("3. No hay espacios alrededor del =")
    st.stop()

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        
        # Verificar si los datos parecen ser de la hoja correcta
        expected_columns = ["Field", "Subfield"]  # Columnas esperadas
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            st.error("Error: La hoja cargada no parece ser 'Exercises DB'")
            st.error(f"Faltan las columnas esperadas: {missing_columns}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.error("Verifica que la URL apunta a la hoja 'Exercises DB'")
        return None

# Variable global para contar ejercicios
exercise_counter = 0

def exercise_card(exercise_data):
    """Componente para mostrar un ejercicio en formato de tarjeta."""
    
    # Estilos CSS personalizados
    st.markdown("""
        <style>
        .section-bar {
            display: flex;
            justify-content: space-between;
            color: #666;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        .title-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .exercise-order {
            font-size: 1.125rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        .exercise-name {
            font-size: 1.5rem;
            font-weight: 700;
        }
        .rsqsms-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        .tag {
            background-color: rgba(66, 82, 110, 0.1);
            color: #42526E;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            display: inline-block;
            margin: 0.25rem;
        }
        .card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .notes-section {
            background-color: #F8F9FA;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
        <style>
        .gif-container {
            display: flex;
            justify-content: center;
            width: 100%;
            margin: 1rem 0;
        }
        .standards-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        .standards-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        }
        </style>
    """, unsafe_allow_html=True)

    global exercise_counter
    exercise_counter += 1  # Incrementar el contador para cada ejercicio

    with st.container():
        # Section Bar
        st.markdown(f"""
            <div class="section-bar">
                <span>{exercise_data['sectionInfo']['left']}</span>
                <span>{exercise_data['sectionInfo']['right']}</span>
            </div>
        """, unsafe_allow_html=True)

        
        # Title Bar con clave única para el botón
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div style="display: flex; align-items: center;">
                    <span class="exercise-order">{exercise_data['exerciseInfo']['order']}</span>
                    <span class="exercise-name">{exercise_data['exerciseInfo']['name']}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            # Usar el contador global para asegurar una clave única
            unique_key = f"btn_{exercise_counter}_{exercise_data['exerciseInfo']['order']}_{exercise_data['exerciseInfo']['name']}"
            unique_key = "".join(c for c in unique_key if c.isalnum() or c == '_')
            
            # Si se hace clic en el botón, mostrar el video
            if st.button(f"Watch video ({exercise_data['exerciseInfo']['videoLength']})", key=unique_key):
                if exercise_data['youtube_url']:
                    st.video(exercise_data['youtube_url'])
                else:
                    st.warning("No hay video disponible")

       # GIF/Video con mejor manejo de errores
        try:
            if pd.notna(exercise_data['gif_url']) and exercise_data['gif_url'] != 'no_gif_available':
                st.markdown('<div class="gif-container">', unsafe_allow_html=True)
                try:
                    st.image(exercise_data['gif_url'], use_container_width=True)
                except Exception as e:
                    st.warning(f"No se pudo cargar el GIF. Mostrando video alternativo.")
                    with st.expander("Ver Video"):
                        if exercise_data['youtube_url']:
                            st.video(exercise_data['youtube_url'])
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                with st.expander("Ver Video"):
                    if exercise_data['youtube_url']:
                        st.video(exercise_data['youtube_url'])
        except Exception as e:
            st.error(f"Error al mostrar el contenido multimedia: {str(e)}")
        
        # Standards (RS, QS, MS)
        st.markdown('<div class="standards-grid">', unsafe_allow_html=True)
        
        # RS y MS en la misma línea
        st.markdown(f"""
            <div class="standards-row">
                <div><strong>RS:</strong> {exercise_data['standards']['RS']}</div>
                <div><strong>MS:</strong> {exercise_data['standards']['MS']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # QS en su propia línea
        st.markdown(f"""
            <div class="standards-row">
                <div><strong>QS:</strong> {exercise_data['standards']['QS']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # RSQSMS Bar
        if exercise_data.get('rsqsms'):
            st.markdown('<div class="rsqsms-grid">', unsafe_allow_html=True)
            for key, value in exercise_data['rsqsms'].items():
                if pd.notna(value):  # Solo mostrar si el valor no es NA
                    st.markdown(f"""
                        <div><strong>{key.title()}:</strong> {value}</div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Description
        if exercise_data.get('description'):
            st.markdown(exercise_data['description'])

        # Tags
        if exercise_data.get('tags'):
            st.markdown("### Tags")
            st.markdown('<div style="margin: 0.5rem 0;">', unsafe_allow_html=True)
            for tag in exercise_data['tags']:
                st.markdown(f'<span class="tag">{tag}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
  

def main():
    # Título principal
    st.title("Human Development - 1st Year")
    st.header('Exercises Database & Progress')
    
    # Cargar datos
    df = load_data()
    
    if df is not None:
        first_column_values = df.iloc[:, 0].unique().tolist()
        field_tabs = st.tabs(first_column_values)
        
        for tab, field in zip(field_tabs, first_column_values):
            with tab:
                filtered_df = df[df.iloc[:, 0] == field]
                subfields = filtered_df["Subfield"].unique().tolist()
                
                subfield_tabs = st.tabs(subfields)
                
                for subtab, subfield in zip(subfield_tabs, subfields):
                    with subtab:
                        # Filtrar ejercicios para este subfield
                        exercises = filtered_df[filtered_df["Subfield"] == subfield]
                        
                        # Lista de Documents con links (sin numeración)
                        st.markdown('<div class="table-of-contents">', unsafe_allow_html=True)
                        documents = exercises["Document"].unique().tolist()
                        for doc in documents:
                            doc_id = doc.lower().replace(" ", "-")
                            st.markdown(
                                f'{doc} <a href="#{doc_id}" class="go-link">(Go)</a>',
                                unsafe_allow_html=True
                            )  

                        st.markdown('</div>', unsafe_allow_html=True)

                        # Divider con menos espaciado
                        st.markdown('<hr style="margin: 0.5rem 0;">', unsafe_allow_html=True) 
                                                
                        # Agrupar por Document
                        for document in documents:
                            # Contar ejercicios para este documento
                            doc_exercises = exercises[exercises["Document"] == document]
                            exercise_count = len(doc_exercises)
                            
                            # Subtítulo del documento con contador (sticky)
                            with sticky_container(mode="top", margin="5rem"):
                                st.markdown(f'<div id="{document.lower().replace(" ", "-")}">', unsafe_allow_html=True)
                                st.header(f"{document} ({exercise_count} exercises)")
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Mostrar cada ejercicio
                            for _, exercise in doc_exercises.iterrows():
                                    exercise_data = {
                                        'sectionInfo': {
                                            'left': f"{field} - {subfield}",
                                            'right': str(exercise['Skill/Difficulty']) if 'Skill/Difficulty' in exercise.index else 'No info'
                                        },
                                        'exerciseInfo': {
                                            'order': str(exercise['Exercise order']) if 'Exercise order' in exercise.index else '0',
                                            'name': str(exercise['Exercise Title']) if 'Exercise Title' in exercise.index else 'Sin título',
                                            'videoLength': str(exercise['Video Length']) if 'Video Length' in exercise.index else '00:00'  # Corregido aquí
                                        },
                                        'gif_url': str(exercise['GIF Link']) if 'GIF Link' in exercise.index else 'no_gif_available',
                                        'youtube_url': str(exercise['YouTube Link']) if 'YouTube Link' in exercise.index else '',
                                        'standards': {
                                            'RS': str(exercise['RS (Reps/Sets)']) if 'RS (Reps/Sets)' in exercise.index else 'N/A',
                                            'QS': str(exercise['QS (Quality Standards)']) if 'QS (Quality Standards)' in exercise.index else 'No info',
                                            'MS': str(exercise['MS (Mastery Standards)']) if 'MS (Mastery Standards)' in exercise.index else 'No info'
                                        },
                                        'description': str(exercise['Description']) if 'Description' in exercise.index else '',
                                        'tags': [tag.strip() for tag in str(exercise['Tags']).split(',') if tag.strip()] if 'Tags' in exercise.index else []
                                    }
                                    
                                    exercise_card(exercise_data) # Información de debugging al final
        st.divider()
        with st.expander("Información de Debug"):
            st.write("Columnas disponibles:", df.columns.tolist())
            st.write("Primeras filas:", df.head())
    else:
        st.error("No se pudieron cargar los datos de la hoja 'Exercises DB'")

if __name__ == "__main__":
    main()