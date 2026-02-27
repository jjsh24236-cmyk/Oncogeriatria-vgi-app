import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# 🔐 Supabase configuration
SUPABASE_URL = "https://ccrhhdavgzfoshgcbels.supabase.co"
SUPABASE_KEY = "sb_publishable_TnXqTP9cfYSYeLlVdp4hzg_5osLIL5r"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="VGI Oncogeriatría", layout="wide")

st.title("Valoración Geriátrica Integral - Oncogeriatría")

# =========================
# DATOS GENERALES
# =========================

st.header("I. Datos Generales")

nombre = st.text_input("Nombre completo")
nss = st.text_input("Número de Seguridad Social")
edad = st.number_input("Edad", min_value=18, max_value=110)

# =========================
# G8
# =========================

st.header("II. G8")

peso = st.number_input("Peso (kg)", min_value=20.0, max_value=200.0)
talla = st.number_input("Talla (m)", min_value=1.0, max_value=2.5)

imc = None
if peso and talla:
    imc = peso / (talla ** 2)
    st.write(f"IMC calculado: {round(imc,2)}")

perdida_peso = st.selectbox(
    "¿Ha perdido peso en los últimos 3 meses?",
    [
        "No",
        "Sí, 1-3 kg",
        "Sí, >3 kg",
        "No sabe"
    ]
)

movilidad = st.selectbox(
    "Movilidad",
    [
        "Sale de casa",
        "Limitado",
        "En cama o silla"
    ]
)

neuro = st.selectbox(
    "Problemas neuropsicológicos",
    [
        "No",
        "Depresión leve",
        "Demencia"
    ]
)

medicamentos = st.number_input("Número de medicamentos diarios", 0, 20)

salud = st.selectbox(
    "Percepción de salud",
    [
        "Mejor",
        "Igual",
        "Peor"
    ]
)

# =========================
# FUNCIONALIDAD
# =========================

st.header("III. Funcionalidad")

barthel = st.number_input("Índice de Barthel (0-100)", 0, 100)
katz = st.selectbox(
    "Katz",
    [
        "A - Independiente",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G - Dependiente"
    ]
)

lawton = st.number_input("Lawton y Brody (0-8)", 0, 8)

# =========================
# COGNITIVA
# =========================

st.header("IV. Esfera Cognitiva")

mini_cog = st.number_input("Mini-Cog (0-5)", 0, 5)

imagen_reloj = st.file_uploader("Subir imagen del dibujo del reloj", type=["png","jpg","jpeg"])

# =========================
# NUTRICIÓN
# =========================

st.header("V. Nutrición")

mna = st.number_input("MNA-SF (0-14)", 0, 14)

# =========================
# EMOCIONAL
# =========================

st.header("VI. Esfera Emocional")

yesavage = st.number_input("Yesavage (0-15)", 0, 15)

# =========================
# SOCIAL
# =========================

st.header("VII. Esfera Social")

vive_solo = st.selectbox("¿Vive solo?", ["Sí", "No"])

# =========================
# CRASH / CARG
# =========================

st.header("VIII. Toxicidad Quimioterapia")

crash = st.text_input("Resultado CRASH (copiar desde MDCalc)")
carg = st.text_input("Resultado CARG-TT (copiar desde MDCalc)")

# =========================
# GUARDAR
# =========================

if st.button("Guardar Evaluación"):

    data = {
        "nombre": nombre,
        "nss": nss,
        "edad": edad,
        "peso": peso,
        "talla": talla,
        "imc": imc,
        "perdida_peso": perdida_peso,
        "movilidad": movilidad,
        "neuro": neuro,
        "medicamentos": medicamentos,
        "salud": salud,
        "barthel": barthel,
        "katz": katz,
        "lawton": lawton,
        "mini_cog": mini_cog,
        "mna": mna,
        "yesavage": yesavage,
        "vive_solo": vive_solo,
        "crash": crash,
        "carg": carg,
        "fecha": datetime.now().isoformat()
    }

    response = supabase.table("vgi_evaluaciones").insert(data).execute()

    st.success("Evaluación guardada correctamente en Supabase")

