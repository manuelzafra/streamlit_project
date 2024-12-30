import streamlit as st

# Título de la página
st.title("Diseño de Presentación")

# Subtítulos y descripción
st.header("Ficha del Ejercicio")
st.write("Experimenta con la presentación de datos y formatos.")

# Diseño con columnas
col1, col2 = st.columns(2)
with col1:
    st.subheader("Atributo Principal")
    st.write("• Nivel: **Intermedio**")
    st.write("• Área: *Piernas*")
    st.write("• Material: Mancuerna")
with col2:
    st.image("https://via.placeholder.com/150", caption="Imagen de ejemplo")

# Video o GIF
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Panel lateral con filtros
st.sidebar.header("Panel de Control")
filtro = st.sidebar.selectbox("Selecciona un filtro", ["Nivel", "Área", "Material"])
st.sidebar.write(f"Has seleccionado: {filtro}")
#design_playground.py