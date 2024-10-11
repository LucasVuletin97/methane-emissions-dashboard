<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
</head>
<body>

<h1>Methane Emissions Dashboard</h1>

<h2>Descripción</h2>
<p>Este proyecto es una visualización interactiva de las emisiones de metano utilizando <strong>Streamlit</strong>. 
El dashboard permite analizar las emisiones a través de varios filtros e incluye gráficos detallados que muestran las emisiones por año, empresa y un mapa de calor por estado.</p>

<h3>Características:</h3>
<ul>
    <li><strong>Gráfico de Emisiones vs. Año</strong>: Muestra las emisiones de metano agrupadas por segmento industrial y permite seleccionar un rango de años y cuencas.</li>
    <li><strong>Gráfico de Emisiones vs. Empresa</strong>: Visualiza las emisiones agrupadas por fuente de emisión, filtradas por año y cuenca.</li>
    <li><strong>Mapa de Calor por Estado</strong>: Muestra las emisiones de metano por estado de los EE. UU. en un mapa interactivo, filtrado por año y categoría de emisión.</li>
</ul>

<h2>Estructura del Proyecto</h2>

<pre>
Methane-emissions-dashboard/
│
├── Excercise.py
├── requirements.txt        
├── README.md               
└── data/
        Data - Junior Data Visualization Analyst.xlsx
</pre>

<h2>Requisitos</h2>
<p><strong>Python 3.x</strong> (recomendado 3.8 o superior)</p>
<p>Las dependencias se pueden instalar utilizando el archivo <code>requirements.txt</code>.</p>

<h2>Instalación</h2>
<p>Sigue los siguientes pasos para configurar el entorno y ejecutar la aplicación:</p>

<ol>
    <li>Clonar este repositorio:</li>
    <pre><code>git clone https://github.com/LucasVuletin97/methane-emissions-dashboard.git
cd methane-emissions-dashboard</code></pre>

<li> Crear un entorno virtual: </li>
    <pre><code>python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate</code></pre>

<li>Instalar las dependencias:</li>
    <pre><code>pip install -r requirements.txt</code></pre>

<li>Ejecutar la aplicación:</li>
    <pre><code>streamlit run Excercise1.py
streamlit run Excercise2.py
streamlit run Excercise3.py
    </code></pre>
</ol>

<h2>Uso</h2>
<p>Al iniciar la aplicación, podrás cargar un archivo <strong>Excel</strong> que contiene los datos de emisiones de metano. La aplicación mostrará diferentes gráficos interactivos, donde podrás aplicar filtros por:</p>

<ul>
    <li><strong>Año</strong>: Seleccionar un rango o año específico para el análisis.</li>
    <li><strong>Cuenca</strong>: Filtrar por cuenca de emisión.</li>
    <li><strong>Estado</strong>: Visualizar las emisiones por estado (opcional: elegir todos los estados).</li>
    <li><strong>Fuente de Emisión</strong>: Filtrar por categoría de emisión.</li>
</ul>

<h2>Archivos</h2>
<ul>
    <li><strong>Excercise.py</strong>: Este archivo contiene el código de la aplicación Streamlit, que genera gráficos interactivos y permite filtrar los datos cargados.</li>
    <li><strong>requirements.txt</strong>: Archivo que lista todas las dependencias necesarias para que el código funcione.</li>
    <li><strong>README.md</strong>: Este archivo de documentación, con instrucciones detalladas para ejecutar el proyecto.</li>
</ul>

<h2>Visualizaciones</h2>

<h3>1. Emisiones de Metano vs. Año (Apilado por Segmento Industrial)</h3>
<p>Este gráfico muestra las emisiones de metano a lo largo de los años, agrupado por segmento industrial, y permite filtrar por año y cuenca.</p>

<h3>2. Emisiones de Metano vs. Empresa (Apilado por Fuente de Emisión)</h3>
<p>Muestra las emisiones de metano por empresa, apilado por la fuente de emisión. El gráfico permite filtrar por año y cuenca.</p>

<h3>3. Mapa de Calor de Emisiones por Estado</h3>
<p>Un mapa interactivo de las emisiones de metano por estado, con la posibilidad de filtrar por año y fuente de emisión.</p>

</body>
</html>
