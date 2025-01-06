import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from typing import Literal
#from streamlit_lucide import lucide  # Para los iconos

# Definición de iconos SVG
ICONS = {
    'clock': """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
    </svg>""",
    
    'tag': """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>
        <line x1="7" y1="7" x2="7.01" y2="7"/>
    </svg>""",
    
    'bookmark': """<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
    </svg>"""
}

# Configuración de la página
st.set_page_config(
    page_title="Human Development — Exercises Database & Progress",
    page_icon="🏃",
    layout="centered"
)

# Estilos CSS actualizados
st.markdown("""
    <style>
    /* Card container */
    .exercise-card {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 24px;
        background: white;
    }
    
    /* Standards grid */
    .standards-grid {
        display: grid;
        grid-template-rows: auto auto;
        gap: 16px;
        margin: 24px 0;
    }
    .standards-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    .standard-item {
        padding: 12px;
        border-radius: 6px;
    }
    
    /* Footer section */
    .footer-section {
        background: #F9FAFB;
        padding: 16px;
        border-radius: 8px;
        margin-top: 24px;
    }
    
    /* Tags */
    .tags-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
    }
    .tag {
        background: #E5E7EB;
        color: #374151;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 14px;
    }
    
    /* Sticky header */
    .sticky-header {
        position: sticky;
        top: 0;
        background: white;
        z-index: 999;
        padding: 16px 0;
        border-bottom: 1px solid #E0E0E0;
    }
    
    /* Video button */
    .video-button {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        background: white;
        color: #374151;
        text-decoration: none;
        transition: all 0.2s;
    }
    .video-button:hover {
        background: #F9FAFB;
    }
    </style>
""", unsafe_allow_html=True) 

# Cargar variables de entorno
load_dotenv()
GOOGLE_SHEET_CSV_URL = os.getenv("GOOGLE_SHEET_CSV_URL")

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
    
def exercise_card(exercise_data):
    with st.container():
        st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
        
        # Header
        st.markdown(f"""
            <div class="section-header">
                <span>{exercise_data['sectionInfo']['left']}</span>
                <span>{exercise_data['sectionInfo']['right']}</span>
            </div>
        """, unsafe_allow_html=True)

        # Title y Video Button
        cols = st.columns([3, 1])
        with cols[0]:
            st.markdown(f"""
                <div class="exercise-title">
                    <span class="exercise-order">{exercise_data['exerciseInfo']['order']}</span>
                    <span class="exercise-name">{exercise_data['exerciseInfo']['name']}</span>
                </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            if pd.notna(exercise_data['youtube_url']):
                st.markdown(f"""
                    <a href="{exercise_data['youtube_url']}" target="_blank" class="video-button">
                        {ICONS['clock']} Watch video ({exercise_data['exerciseInfo']['videoLength']})
                    </a>
                """, unsafe_allow_html=True)

        # GIF/Image
        if pd.notna(exercise_data['gif_url']) and exercise_data['gif_url'] != 'no_gif_available':
            st.image(exercise_data['gif_url'], use_column_width=True)

        # Standards Grid
        st.markdown(f"""
            <div class="standards-grid">
                <div class="standards-row">
                    <div class="standard-item">
                        <strong>RS:</strong> {exercise_data['standards']['RS']}
                    </div>
                    <div class="standard-item">
                        <strong>MS:</strong> {exercise_data['standards']['MS']}
                    </div>
                </div>
                <div class="standard-item">
                    <strong>QS:</strong> {exercise_data['standards']['QS']}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Description
        if exercise_data.get('description'):
            st.markdown(f"<div class='description'>{exercise_data['description']}</div>", 
                       unsafe_allow_html=True)

        # Footer section (Tags and Notes)
        st.markdown('<div class="footer-section">', unsafe_allow_html=True)
        
        # Tags
        if exercise_data.get('tags'):
            st.markdown(f"""
                <div class="tags-container">
                    {ICONS['tag']}
                    {''.join(f'<span class="tag">{tag}</span>' for tag in exercise_data['tags'])}
                </div>
            """, unsafe_allow_html=True)

        # Notes
        if exercise_data.get('notes'):
            st.markdown(f"""
                <div class="notes-section">
                    {ICONS['bookmark']} <strong>Notes</strong>
                    <p>{exercise_data['notes']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)

def parse_exercise_order(order_str):
    """Función auxiliar para ordenar ejercicios."""
    order = str(order_str).lower()
    import re
    base_match = re.match(r'([a-z])(\d+)', order)
    if not base_match:
        return ('z', 999, 'zzz')
    
    letter = base_match.group(1)
    number = int(base_match.group(2))
    
    variant_priority = {
        'regression': 1,
        'easy': 2,
        'basic': 3,
        'hard': 4
    }
    
    variant = 'basic'
    for key in variant_priority.keys():
        if key in order:
            variant = key
            break
    
    return (letter, number, variant)

@st.cache_data
def load_data():
    """Carga y valida los datos del Google Sheet."""
    try:
        df = pd.read_csv(GOOGLE_SHEET_CSV_URL)
        expected_columns = ["Field", "Subfield"]
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Error: Faltan las columnas esperadas: {missing_columns}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

def main():
    # Título principal
    st.title("Human Development - 1st Year")
    st.header('Exercises Database & Progress')
    
    # Cargar datos
    df = load_data()
    
    if df is not None:
        # Debug: mostrar las columnas disponibles
        st.write("Columnas disponibles:", df.columns.tolist())
        
        # Crear tabs principales
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
                        
                        # Lista de Documents con links
                        documents = exercises["Document"].unique().tolist()
                        for doc in documents:
                            doc_id = doc.lower().replace(" ", "-")
                            st.markdown(
                                f'{doc} <a href="#{doc_id}" class="go-link">(Go)</a>',
                                unsafe_allow_html=True
                            )
                        
                        # Mostrar ejercicios por documento
                        for document in documents:
                            doc_exercises = exercises[exercises["Document"] == document]
                            
                            for _, exercise in doc_exercises.iterrows():
                                exercise_data = {
                                    'sectionInfo': {
                                        'left': f"{field} - {subfield}",
                                        'right': str(exercise.get('Skill/Difficulty', 'No hay información'))
                                    },
                                    'exerciseInfo': {
                                        'order': str(exercise.get('Exercise order', '0')),
                                        'name': str(exercise.get('Exercise Title', 'Sin título')),
                                        'videoLength': str(exercise.get('Video Length', '00:00'))
                                    },
                                    'gif_url': str(exercise.get('GIF Link', 'no_gif_available')),
                                    'youtube_url': str(exercise.get('YouTube Link', '')),
                                    'standards': {
                                        'RS': str(exercise.get('RS (Reps/Sets)', 'No hay información')),
                                        'QS': str(exercise.get('QS (Quality Standards)', 'No hay información')),
                                        'MS': str(exercise.get('MS (Mastery Standards)', 'No hay información'))
                                    },
                                    'description': str(exercise.get('Description', '')),
                                    'tags': [tag.strip() for tag in str(exercise.get('Tags', '')).split(',') 
                                            if tag.strip()] if pd.notna(exercise.get('Tags')) else [],
                                    'notes': str(exercise.get('Notes', ''))
                                }
                                
                                exercise_card(exercise_data)

   
    if df is not None:
        # Ordenar primero
        df = df.sort_values(
            by=['Field', 'Subfield', 'Document', 'Section / Body District', 'Skill/Difficulty', 'Exercise order'],
            key=lambda x: x.map(str) if x.name != 'Exercise order' else x.map(parse_exercise_order)
        )
        
        # Crear tabs principales
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
                        
                        # Lista de Documents con links
                        st.markdown('<div class="table-of-contents">', unsafe_allow_html=True)
                        documents = exercises["Document"].unique().tolist()
                        for doc in documents:
                            doc_id = doc.lower().replace(" ", "-")
                            st.markdown(
                                f'{doc} <a href="#{doc_id}" class="go-link">(Go)</a>',
                                unsafe_allow_html=True
                            )
                        st.markdown('</div><hr style="margin: 0.5rem 0;">', unsafe_allow_html=True)
                        
                        # Mostrar ejercicios por documento
                        for document in documents:
                            doc_exercises = exercises[exercises["Document"] == document]
                            exercise_count = len(doc_exercises)
                            
                            # Título del documento con ancla
                            st.markdown(f'<div id="{document.lower().replace(" ", "-")}">', unsafe_allow_html=True)
                            st.header(f"{document} ({exercise_count} exercises)")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Mostrar cada ejercicio
                            for _, exercise in doc_exercises.iterrows():
                                exercise_data = {
                                    'sectionInfo': {
                                        'left': f"{field} - {subfield}",
                                        'right': str(exercise['Skill/Difficulty']) if pd.notna(exercise['Skill/Difficulty']) else 'No hay información'
                                    },
                                    'exerciseInfo': {
                                        'order': str(exercise['Exercise order']) if pd.notna(exercise['Exercise order']) else '0',
                                        'name': str(exercise['Exercise Title']) if pd.notna(exercise['Exercise Title']) else 'Sin título',
                                        'videoLength': str(exercise['Video Length']) if pd.notna(exercise['Video Length']) else '00:00'
                                    },
                                    'gif_url': str(exercise['GIF Link']) if pd.notna(exercise['GIF Link']) else 'no_gif_available',
                                    'youtube_url': str(exercise['YouTube Link']) if pd.notna(exercise['YouTube Link']) else '',
                                    'standards': {
                                        'RS': str(exercise['RS (Reps/Sets)']) if pd.notna(exercise['RS (Reps/Sets)']) else 'No hay información',
                                        'QS': str(exercise['QS (Quality Standards)']) if pd.notna(exercise['QS (Quality Standards)']) else 'No hay información',
                                        'MS': str(exercise['MS (Mastery Standards)']) if pd.notna(exercise['MS (Mastery Standards)']) else 'No hay información'
                                    },
                                    'description': str(exercise['Description']) if pd.notna(exercise['Description']) else '',
                                    'tags': [tag.strip() for tag in str(exercise['Tags']).split(',') if tag.strip() and pd.notna(exercise['Tags'])],
                                    'notes': str(exercise['Notes']) if pd.notna(exercise['Notes']) else ''
                                }
                                
                                exercise_card(exercise_data)
     # Sticky header para Document
        st.markdown(f"""
            <div class="sticky-header" id="{document.lower().replace(' ', '-')}">
                <h2>{document} ({exercise_count} exercises)</h2>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()