import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="📘 Quiz de Bases de Datos", layout="centered", initial_sidebar_state="collapsed")

# CSS personalizado oscuro
st.markdown("""
<style>
    * {
        color: #E6F0F5;
    }
    body {
        background-color: #191E1E;
    }
    .stApp {
        background-color: #191E1E;
    }
    .stButton>button {
        background-color: #4296F5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2980B9;
    }
</style>
""", unsafe_allow_html=True)

# Preguntas Parcial 1
preguntas_p1 = [
    ("Si una interrelación uno a muchos tiene un atributo genera un atributo en la tabla del lado de muchos.", "V"),
    ("Las dependencias funcionales son un caso especial de las dependencias multivaluadas.", "V"),
    ("Un DDL(data definition language) provee un lenguaje para indicar los atributos de una tabla entre otras cosas.", "V"),
    ("En un DER una interrelación uno a uno de tipo 'es un' genera un nuevo campo o conjunto de campos en la tabla que tiene menor cantidad de registros y es una clave foránea que apunta a la clave de la tabla que tiene mayor cantidad de registros.", "V"),
    ("La dependencia funcional X -> Y es trivial si Y es un subconjunto de X(Y c X).", "V"),
    ("Si tengo una relación de la forma EMPLEADO(Legajo,DNI,Nombre, Apellido, Telefono) donde un empleado puede tener más de un teléfono la clave será el conjunto de atributos ('Legajo', 'Teléfono') y el conjunto ('DNI', 'Teléfono') es clave candidata.", "V"),
    ("Una relación uno a muchos en un DER da origen a una nueva tabla.", "F"),
    ("En el análisis de las Formas Normales cada relación se analiza de manera separada del resto de las relaciones.", "V"),
    ("Un DDL(data definition language) provee un lenguaje para la formulación de consultas entre otras cosas.", "F"),
    ("En un DER una interrelación muchos a muchos genera un nuevo atributo/s en la tabla que más tuplas tiene y que es clave foránea hacia la clave principal de la tabla que tiene menos registros.", "F"),
]

# Preguntas Parcial 2
preguntas_p2 = [
    ("Un índice hash bitmap la pseudoclave es un número binario.", "V"),
    ("Los predicados de junta pueden tener un operador que no sea de igualdad.", "V"),
    ("En una ejecución optimizada los predicados locales se ejecutan primero.", "V"),
    ("El uso del Left Join siempre produce filas con campos con valor null.", "F"),
    ("Las transacciones sólo pueden actuar sobre una tabla.", "F"),
    ("Los predicados locales solo pueden ser comparaciones de igualdad.", "F"),
    ("No hay conflicto cuando una transacción quiere tomar un cierre de escritura y otra tiene un cierre de lectura sobre el mismo ítem.", "F"),
    ("Hay un conflicto cuando una transacción quiere tomar un cierre de lectura y otra ya tiene un cierre de escritura sobre el mismo ítem.", "V"),
    ("Hay conflicto cuando una transacción quiere tomar un cierre de escritura y otra ya tiene un cierre de lectura sobre el mismo ítem.", "V"),
    ("A los usuarios de una base de datos se les debe otorgar los mínimos privilegios necesarios.", "V"),
]

# Inicializar sesión
if "estado" not in st.session_state:
    st.session_state.estado = "menu"
    st.session_state.preguntas = []
    st.session_state.respuestas = []
    st.session_state.indice = 0
    st.session_state.respondidas = []

# Menú Principal
if st.session_state.estado == "menu":
    st.markdown("<h1 style='text-align: center; color: #4296F5;'>📘 Quiz de Bases de Datos</h1>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns(2)
    
    if col1.button("📖 Parcial 1", use_container_width=True, key="btn_p1"):
        st.session_state.preguntas = random.sample(preguntas_p1, len(preguntas_p1))
        st.session_state.respuestas = [None] * len(st.session_state.preguntas)
        st.session_state.respondidas = [False] * len(st.session_state.preguntas)
        st.session_state.indice = 0
        st.session_state.estado = "quiz"
        st.rerun()
    
    if col2.button("📚 Parcial 2", use_container_width=True, key="btn_p2"):
        st.session_state.preguntas = random.sample(preguntas_p2, len(preguntas_p2))
        st.session_state.respuestas = [None] * len(st.session_state.preguntas)
        st.session_state.respondidas = [False] * len(st.session_state.preguntas)
        st.session_state.indice = 0
        st.session_state.estado = "quiz"
        st.rerun()
    
    if col1.button("🎯 Ambos Parciales", use_container_width=True, key="btn_ambos"):
        todas = random.sample(preguntas_p1 + preguntas_p2, len(preguntas_p1) + len(preguntas_p2))
        st.session_state.preguntas = todas
        st.session_state.respuestas = [None] * len(todas)
        st.session_state.respondidas = [False] * len(todas)
        st.session_state.indice = 0
        st.session_state.estado = "quiz"
        st.rerun()

# Pantalla Quiz
elif st.session_state.estado == "quiz":
    preguntas = st.session_state.preguntas
    indice = st.session_state.indice
    total = len(preguntas)
    correctas = sum(1 for i, (p, r) in enumerate(preguntas) if st.session_state.respuestas[i] == r)
    
    # Header
    col1, col2, col3 = st.columns(3)
    col1.metric("Pregunta", f"{indice + 1}/{total}")
    col2.metric("Correctas", correctas)
    col3.metric("Progreso", f"{int((indice+1)/total*100)}%")
    
    st.divider()
    
    # Pregunta
    pregunta, respuesta_correcta = preguntas[indice]
    st.markdown(f"<h3 style='color: #4296F5;'>{pregunta}</h3>", unsafe_allow_html=True)
    
    st.write("")
    
    # Botones de respuesta
    col1, col2 = st.columns(2)
    
    if not st.session_state.respondidas[indice]:
        if col1.button("✓ Verdadero", use_container_width=True, key=f"v_{indice}"):
            st.session_state.respuestas[indice] = "V"
            st.session_state.respondidas[indice] = True
            st.rerun()
        
        if col2.button("✗ Falso", use_container_width=True, key=f"f_{indice}"):
            st.session_state.respuestas[indice] = "F"
            st.session_state.respondidas[indice] = True
            st.rerun()
    else:
        respuesta_usuario = st.session_state.respuestas[indice]
        es_correcta = respuesta_usuario == respuesta_correcta
        
        color = "🟢" if es_correcta else "🔴"
        mensaje = "¡Correcto!" if es_correcta else f"Incorrecto. La respuesta es: {respuesta_correcta}"
        
        st.markdown(f"<h4 style='color: #{'76AF50' if es_correcta else 'F44336'};'>{color} {mensaje}</h4>", unsafe_allow_html=True)
    
    st.divider()
    
    # Navegación
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("← Anterior", use_container_width=True):
        if indice > 0:
            st.session_state.indice -= 1
            st.rerun()
    
    if col2.button("Siguiente →", use_container_width=True):
        if indice < total - 1:
            st.session_state.indice += 1
            st.rerun()
        elif all(st.session_state.respondidas):
            st.session_state.estado = "resultado"
            st.rerun()
    
    if col3.button("📋 Menú", use_container_width=True):
        st.session_state.estado = "menu"
        st.rerun()
    
    if col4.button("❌ Salir", use_container_width=True):
        st.stop()

# Pantalla Resultado
elif st.session_state.estado == "resultado":
    preguntas = st.session_state.preguntas
    correctas = sum(1 for i, (p, r) in enumerate(preguntas) if st.session_state.respuestas[i] == r)
    incorrectas = len(preguntas) - correctas
    porcentaje = int((correctas / len(preguntas)) * 100)
    
    st.markdown("<h1 style='text-align: center; color: #4296F5;'>✓ Resultado Final</h1>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("✓ Correctas", correctas, f"{porcentaje}%")
    col2.metric("✗ Incorrectas", incorrectas)
    col3.metric("Total", len(preguntas))
    
    st.divider()
    
    # Emoji según resultado
    if porcentaje >= 80:
        emoji = "🏆"
        msg = "¡Excelente!"
    elif porcentaje >= 60:
        emoji = "👍"
        msg = "¡Muy bien!"
    else:
        emoji = "📚"
        msg = "Sigue estudiando"
    
    st.markdown(f"<h2 style='text-align: center; color: #4296F5;'>{emoji} {msg}</h2>", unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🔄 Volver al Menú", use_container_width=True):
        st.session_state.estado = "menu"
        st.rerun()
