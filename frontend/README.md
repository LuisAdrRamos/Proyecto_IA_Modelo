
# Frontend – Proyecto IA de Teclados Gaming 🎮🔍

Este frontend proporciona una interfaz visual para interactuar con un modelo de inteligencia artificial que clasifica ofertas de teclados gaming según su precio y características. Permite a los usuarios ingresar datos manualmente o subir archivos CSV para realizar predicciones.

## 🚀 Tecnologías utilizadas

- **Python 3.12+**
- **Flask** como framework principal
- **HTML + Jinja2** para las vistas
- **Tailwind CSS** (a través de clases en `styles.css`) para estilos modernos
- **JavaScript** para interacción dinámica
- **Chart.js** para visualización gráfica de precios (integrado en `main.js`)

## 📁 Estructura del frontend

```
frontend/
│
├── app.py                       # Punto de entrada principal de la app Flask
├── config.py                   # Configuraciones globales (paths, API)
├── requirements.txt            # Dependencias del frontend (Flask, etc.)
│
├── jobs/
│   └── watcher.py              # Módulo para monitorear subidas de archivos
│
├── services/
│   └── api.py                  # Lógica para consumir el backend y el modelo
│
├── static/
│   ├── main.js                 # Lógica para gráficas y validaciones
│   ├── styles.css              # Estilos visuales personalizados
│   ├── bg-cyberpunk.jpg        # Imagen de fondo de la web
│   └── aaa.webp                # Imagen decorativa
│
├── templates/
│   ├── base.html               # Plantilla base de layout (con navbar y estilos)
│   ├── index.html              # Página principal de bienvenida
│   ├── predict.html            # Formulario para predicción individual
│   ├── result.html             # Vista con la predicción del modelo
│   ├── upload.html             # Subida de archivos CSV para predicciones múltiples
│   └── partials/
│       └── predict_result.html# Subcomponente reutilizable para predicciones
│
├── uploads/
│   ├── all_keyboards.csv       # Archivos cargados por el usuario
│   └── *.csv                   # Dataset cargado para predicción masiva
```

## ⚙️ Instalación

1. **Clona el repositorio y entra al frontend:**

```bash
git clone https://github.com/tuusuario/Proyecto_IA_Modelo.git
cd Proyecto_IA_Modelo/frontend
```

2. **Crea un entorno virtual (opcional pero recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Una vez instaladas las dependencias, inicia la aplicación con:

```bash
python app.py
```

Por defecto estará disponible en: [http://localhost:5000](http://localhost:5000)

## ✨ Funcionalidades

- **🏠 Inicio (`/`)**
  - Página de bienvenida con imagen de fondo y diseño moderno.

- **🔮 Predicción personalizada (`/predict`)**
  - Formulario donde se ingresan manualmente los datos del teclado.
  - Muestra el resultado de la predicción del modelo con visualización del precio vs precio real.

- **📂 Subir CSV (`/upload`)**
  - Permite cargar un archivo `.csv` con varios teclados.
  - Se procesan en segundo plano y se muestran los resultados en tabla.

- **📊 Resultados**
  - Categorías como `Ofertón`, `Mala compra`, `Estafa`, etc.
  - Visualización del precio real y el precio ingresado en gráficas.

## 📌 Recomendaciones

- Asegúrate de que el backend esté corriendo y accesible desde `localhost:8000` o ajusta el archivo `config.py`.
- Los archivos `.csv` deben tener las columnas requeridas: `Nombre`, `Precio`, `Tipo`, `Conexión`, `Switches`, etc.
- Si modificas la estructura del modelo o los campos de entrada, asegúrate de actualizar `predict.html` y `api.py`.

## 📷 Capturas

> Agrega aquí imágenes de `predict.html`, `upload.html` y `result.html` si las tienes listas para mostrar.

## 📦 Dependencias

Listado en `requirements.txt`:
```
flask
requests
pandas
joblib
```

## 🧠 Autores

Este frontend fue desarrollado como parte del proyecto de Inteligencia Artificial para evaluar precios de teclados gaming.
