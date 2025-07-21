# 🧠 Modelo de IA para Clasificación de Ofertas de Teclados Gaming

Este proyecto implementa un **modelo de inteligencia artificial supervisado multiclase** que analiza el precio de un teclado gaming y lo clasifica automáticamente en categorías como:

- 🟢 **Ofertón**
- 🟩 **Excelente Oferta**
- 🟨 **Buen Precio**
- ⚪ **Normal**
- 🟧 **Mala Compra**
- 🟥 **Pésima Compra**
- ❌ **Estafa**

> La predicción se basa en el precio ingresado por el usuario, el precio real del producto, y otras características como switches, tipo, conexión, calificación y número de tiendas.

---

## 🧩 ¿Cómo funciona?

El modelo fue entrenado con un dataset de más de 3,000 teclados gaming. Para cada uno se simularon **50 precios distintos** (desde 60% hasta 150% del precio real), y cada uno fue etiquetado automáticamente con una categoría según el siguiente criterio:

| Categoría         | Condición del precio simulado                             |
|-------------------|-----------------------------------------------------------|
| Ofertón           | ≤ 60% del precio real                                     |
| Excelente Oferta  | ≤ 75% del precio real                                     |
| Buen Precio       | ≤ 90% del precio real                                     |
| Normal            | entre 95% y 105% del precio real                          |
| Mala Compra       | ≥ 110% del precio real                                    |
| Pésima Compra     | ≥ 125% del precio real                                    |
| Estafa            | ≥ 140% del precio real                                    |
| (entre otras)     | Clasificado como **Normal** si está entre otras bandas    |

Se utilizó un `RandomForestClassifier` con 10,000 árboles, y luego optimizado a 3,000 árboles para reducir tiempos de inferencia manteniendo una **precisión del 93%**.

---

## ⚙️ Requisitos

- Python ≥ 3.10
- pandas
- numpy
- scikit-learn
- joblib

---

## 🧪 ¿Cómo usarlo?

### 1. Ejecutar una predicción de ejemplo

En `test/test_model.py`:

```python
resultado = predecir_categoria("Logitech G915 TKL (GL Clicky)", 129.99)
```

Esto imprimirá:

```
🧾 Resultado de la evaluación:

🖥️  Teclado            : Logitech G915 TKL (GL Clicky)
💵 Precio ingresado   : $129.99
🏷️  Precio real        : $229.0
📈 Porcentaje del real: 56.76%
📊 Categoría           : Ofertón

📦 Resultado en formato JSON:

{
    "Teclado": "Logitech G915 TKL (GL Clicky)",
    "Precio ingresado": 129.99,
    "Precio real": 229.0,
    "Porcentaje del real": 56.76,
    "Categoría": "Oferton"
}
```

---

### 2. Usarlo en tu backend o frontend

Puedes importar la función `predecir_categoria` desde `test_model.py` o desde el archivo donde la tengas definida:

```python
from test_model import predecir_categoria

resultado = predecir_categoria("Corsair K63", 150.00)
```

El resultado es un `dict` (JSON) que puedes enviar como respuesta desde una API.

---

## 📂 Estructura del Proyecto

```
Proyecto_IA_Modelo/
├── data/
│   ├── teclados_limpio.csv
│   └── train_dataset.csv
├── model/
│   ├── modelo_multiclase_v2.pkl
│   ├── scaler_full.pkl
│   ├── encoder_categoricos.pkl
│   └── encoder_etiquetas.pkl
├── notebooks/
│   ├── entrenamiento.ipynb
│   └── modelo_final.ipynb
├── test/
│   └── test_model.py
├── preprocessor/
│   └── preprocesar.py
└── README.md
```

---

## 📈 Resultados

**Precisión final del modelo:** `93%`  
**F1-Score promedio:** `0.90`  
**Muestras simuladas por teclado:** `50`  
**Teclados de membrana:** ❌ Excluidos para mayor precisión

---

## 👨‍💻 Autores y Créditos

- Desarrollador: Luis Adrian Ramos Guzman.
- Tecnología utilizada: Python + Scikit-learn
- Proyecto de tesis de grado: *Modelo de IA para clasificación y recomendación de teclados gaming*

---

## 📬 Contacto

¿Tienes dudas o sugerencias?  
📧 Escríbeme a `luchoramos042004@gmail.com` o abre un issue en este repositorio.