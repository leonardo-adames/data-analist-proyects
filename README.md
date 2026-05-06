# 🛒 Retail Sales Intelligence — Análisis de Ventas 2023–2024

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.x-F7931E?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Completo-success)

## 📌 Descripción del Problema

Las cadenas retail enfrentan un problema crítico: **toman decisiones comerciales sin entender sus datos**. No saben qué categorías les generan más margen real, qué tiendas tienen potencial oculto, ni qué clientes están a punto de abandonarlos.

Este proyecto analiza **15,000 transacciones** de una cadena de 5 tiendas durante 2 años para responder preguntas reales de negocio.

---

## 🎯 Preguntas de Negocio Respondidas

| # | Pregunta | Técnica Utilizada |
|---|----------|-------------------|
| 1 | ¿Cuál es la tendencia de revenue y crece comparado al año anterior? | Series de tiempo, YoY |
| 2 | ¿Qué categorías generan más margen real, no solo más ventas? | Análisis de rentabilidad |
| 3 | ¿Qué tiendas son las más eficientes por ticket y margen? | Benchmark comparativo |
| 4 | ¿Cuándo se concentran las ventas en el año? | Heatmap estacional |
| 5 | ¿Qué clientes son los más valiosos y cuáles están en riesgo? | Segmentación RFM |
| 6 | ¿Los descuentos realmente aumentan las ventas o destruyen margen? | Análisis de impacto |

---

## 📊 Hallazgos Clave

```
Revenue 2023:      RD$ 121,451,121
Revenue 2024:      RD$ 218,053,132
Crecimiento YoY:            +79.5%

Mejor categoría:     Computadoras (mayor revenue)
Mejor margen:        Accesorios (45% margen prom.)
Tasa de devolución:          3.0%
Clientes Champions:         1,885
```

### 🔑 Insights accionables

1. **Accesorios** tiene el margen más alto (45%) pero bajo volumen — oportunidad de cross-selling con Celulares y Computadoras
2. **Diciembre** concentra el pico máximo de ventas — requiere planificación de inventario anticipada
3. **1,885 clientes Champions** representan el núcleo del negocio — programa de fidelización prioritario
4. **359 clientes Perdidos** — campaña de reactivación con descuento puede recuperar revenue significativo
5. Los descuentos del **25%** no mejoran el margen proporcional — política de descuentos ineficiente

---

## 🗂️ Estructura del Proyecto

```
retail-sales-analysis/
│
├── 📁 data/
│   └── ventas_retail.csv          # Dataset sintético (15,000 filas)
│
├── 📁 notebooks/
│   └── 01_analisis_ventas_retail.py   # Análisis completo ejecutable
│
├── 📁 src/
│   └── generate_data.py           # Generador del dataset sintético
│
├── 📁 outputs/
│   ├── 01_revenue_mensual.png
│   ├── 02_analisis_categorias.png
│   ├── 03_desempeno_tiendas.png
│   ├── 04_estacionalidad.png
│   ├── 05_segmentacion_rfm.png
│   └── 06_analisis_descuentos.png
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación y Uso

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/retail-sales-analysis.git
cd retail-sales-analysis

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar el dataset
python src/generate_data.py

# 4. Ejecutar el análisis completo
python notebooks/01_analisis_ventas_retail.py

# O convertir a Jupyter Notebook:
pip install jupytext
jupytext --to notebook notebooks/01_analisis_ventas_retail.py
jupyter notebook notebooks/01_analisis_ventas_retail.ipynb
```

---

## 🛠️ Stack Tecnológico

| Librería | Uso |
|----------|-----|
| **Pandas** | Manipulación y transformación de datos |
| **NumPy** | Cálculos numéricos y generación de datos |
| **Matplotlib** | Visualizaciones personalizadas |
| **Seaborn** | Heatmaps y gráficos estadísticos |
| **Scikit-learn** | Segmentación RFM (KMeans base) |

---

## 📈 Visualizaciones Generadas

1. **Revenue mensual 2023 vs 2024** — tendencia y comparativa YoY
2. **Análisis de categorías** — revenue, margen y bubble chart
3. **Desempeño por tienda** — benchmark y eficiencia
4. **Heatmap estacional** — patrones por día/mes
5. **Segmentación RFM** — Champions, Leales, En Riesgo, Perdidos
6. **Análisis de descuentos** — impacto real en margen

---

## 👤 Autor

**Leonardo (Aizen)**  
BI Analyst en formación | Bootcamp Business Intelligence  
📺 YouTube: [Bootcamp Business Intelligence](#)  
💼 Notion Portfolio: [Ver portfolio](#)

---

*Proyecto desarrollado como parte del Bootcamp Business Intelligence — 120 días, 120 videos.*
