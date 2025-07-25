import streamlit as st
import pandas as pd
from api import BackendClient

st.set_page_config(page_title="Proyecto IA", layout="wide")
client = BackendClient()

st.title("📊 Sistema Inteligente - Proyecto Final")

tab1, tab2, tab3 = st.tabs(["🏁 Entrenamiento", "📈 Predicción", "🛠 Información"])

with tab1:
    st.subheader("Entrenar modelo")

    file = st.file_uploader("📁 Sube tu dataset CSV", type=["csv"])
    model = st.selectbox("📌 Modelo", ["logreg", "svc", "rf"])
    test_size = st.slider("📉 Porcentaje de test", 0.1, 0.5, 0.2, 0.05)
    random_state = st.number_input("🎲 Semilla", value=42)

    params = {}
    if model == "rf":
        params["n_estimators"] = st.slider("🌲 Árboles (n_estimators)", 10, 1000, 200)
        params["max_depth"] = st.slider("🔍 Profundidad máxima", 1, 50, 10)

    if st.button("🚀 Entrenar modelo"):
        if file is None:
            st.warning("Debes subir un archivo.")
        else:
            with st.spinner("Entrenando..."):
                res = client.train_model(file, {
                    "test_size": test_size,
                    "random_state": random_state,
                    "model_type": model,
                    "model_params": str(params)
                })
            st.success("Modelo entrenado correctamente ✅")
            st.json(res)

with tab2:
    st.subheader("Realizar predicción")
    texto = st.text_area("📝 Ingresa el texto a predecir (una línea por muestra)")
    if st.button("🔮 Predecir"):
        entradas = [line.strip() for line in texto.splitlines() if line.strip()]
        result = client.predict_text(entradas)
        df = pd.DataFrame({
            "Texto": entradas,
            "Predicción": result["labels"],
            "Confianza": result["probabilities"]
        })
        st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("🔧 Información del sistema")
    try:
        status = client.ping()
        st.success(f"Backend conectado ✅: {status}")
    except:
        st.error("❌ No se pudo conectar al backend")
