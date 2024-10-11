import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Mapa de Calor de Emisiones de Metano por Estado')

# Paso 1: Cargar el archivo Excel
file_path = st.file_uploader("Sube el archivo Excel con los datos", type="xlsx")

@st.cache_data
def cargar_datos(file):
    # Leer el archivo desde el binario
    emissions_df = pd.read_excel(file, sheet_name='ef_w_emissions_source_ghg', 
                                 usecols=['facility_id', 'reporting_year', 'total_reported_ch4_emissions', 'reporting_category'])
    facilities_df = pd.read_excel(file, sheet_name='rlps_ghg_emitter_facilities', usecols=['facility_id', 'state'])
    # Devolver la fusión de ambos DataFrames
    return pd.merge(emissions_df, facilities_df, on='facility_id', how='inner')

if file_path is not None:
    try:
        # Obtener los nombres de las hojas del archivo cargado
        sheet_names = pd.ExcelFile(file_path).sheet_names
        if 'ef_w_emissions_source_ghg' not in sheet_names or 'rlps_ghg_emitter_facilities' not in sheet_names:
            st.error("El archivo Excel no contiene las hojas requeridas.")
        else:
            # Usar la función cacheada
            merged_df = cargar_datos(file_path)

            # Filtrar las columnas relevantes
            filtered_df = merged_df[['reporting_year', 'total_reported_ch4_emissions', 'reporting_category', 'state']]

            # Asegurarse de que los años sean numéricos para evitar problemas en los filtros
            filtered_df['reporting_year'] = pd.to_numeric(filtered_df['reporting_year'], errors='coerce')

            # Obtener el rango de años y categorías de emisión únicas
            min_year = int(filtered_df['reporting_year'].min())
            max_year = int(filtered_df['reporting_year'].max())
            unique_categories = filtered_df['reporting_category'].unique().tolist()

            # Agregar la opción "Seleccionar todas las fuentes"
            unique_categories.insert(0, "Seleccionar todas las fuentes")

            # Paso 2: Mostrar los filtros
            st.write("### Filtros para los datos")

            # Selectbox para seleccionar el año
            year_selected = st.selectbox("Selecciona el año", sorted(filtered_df['reporting_year'].unique(), reverse=True))

            # Multiselect para seleccionar las fuentes de emisión
            categories = st.multiselect('Selecciona las fuentes de emisión', options=unique_categories, default="Seleccionar todas las fuentes")

            # Si el usuario selecciona "Seleccionar todas las fuentes", se seleccionan todas las categorías
            if "Seleccionar todas las fuentes" in categories:
                categories = filtered_df['reporting_category'].unique()

            # Botón para aplicar los filtros
            if st.button("Aplicar filtros y mostrar gráfico"):
                # Filtrar los datos según el año y las categorías seleccionadas
                filtered_df = filtered_df[(filtered_df['reporting_year'] == year_selected) & 
                                          (filtered_df['reporting_category'].isin(categories))]

                if not filtered_df.empty:
                    # Crear una tabla dinámica para el mapa de calor
                    pivot_table = filtered_df.pivot_table(index='state', values='total_reported_ch4_emissions', aggfunc='sum')

                    if not pivot_table.empty:
                        # Crear el mapa de calor con Plotly
                        fig = px.choropleth(pivot_table,
                                            locations=pivot_table.index,
                                            locationmode="USA-states",
                                            color='total_reported_ch4_emissions',
                                            color_continuous_scale="Viridis",
                                            scope="usa",
                                            labels={'total_reported_ch4_emissions':'Emisiones CH4 (toneladas)'},
                                            title='Emisiones de Metano por Estado en {} (Filtrado por Fuentes)'.format(year_selected))

                        # Personalización de detalles para un estilo profesional
                        fig.update_layout(
                            geo=dict(
                                showcoastlines=True,
                                coastlinecolor="Black",
                                showland=True,
                                landcolor="white",
                                projection_type='albers usa'
                            ),
                            title_font_size=20,
                            title_x=0.5,
                            margin={"r":0,"t":40,"l":0,"b":0}
                        )

                        # Mostrar el gráfico interactivo en Streamlit
                        st.plotly_chart(fig)
                else:
                    st.warning("No hay datos para los filtros seleccionados.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")
