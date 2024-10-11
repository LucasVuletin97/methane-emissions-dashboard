import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título de la aplicación
st.title('Visualización de Emisiones de Metano')

# Paso 1: Cargar el archivo Excel
file_path = st.file_uploader("Sube el archivo Excel con los datos", type="xlsx")

@st.cache_data
def cargar_datos(file):
    # Leer el archivo desde el binario
    emissions_df = pd.read_excel(file, sheet_name='ef_w_emissions_source_ghg', 
                                 usecols=['facility_id', 'reporting_year', 'total_reported_ch4_emissions', 'industry_segment', 'basin_associated_with_facility'])
    facilities_df = pd.read_excel(file, sheet_name='rlps_ghg_emitter_facilities', usecols=['facility_id'])
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
            filtered_df = merged_df[['reporting_year', 'total_reported_ch4_emissions', 'industry_segment', 'basin_associated_with_facility']]

            # Asegurarse de que los años sean numéricos para evitar problemas en los filtros
            filtered_df['reporting_year'] = pd.to_numeric(filtered_df['reporting_year'], errors='coerce')

            # Obtener el rango de años y los basins únicos
            min_year = int(filtered_df['reporting_year'].min())
            max_year = int(filtered_df['reporting_year'].max())
            unique_basins = filtered_df['basin_associated_with_facility'].unique().tolist()

            # Agregar la opción "Seleccionar todas las fuentes"
            unique_basins.insert(0, "Seleccionar todas las cuencas")

            # Paso 2: Mostrar los filtros
            st.write("### Filtros para los datos")

            # Slider para seleccionar el rango de años
            years_option = st.selectbox('Selecciona una opción para los años', ['Elegir todos los años', 'Seleccionar un rango de años'])

            if years_option == 'Seleccionar un rango de años':
                years = st.slider('Selecciona el rango de años', 
                                  min_value=min_year, 
                                  max_value=max_year, 
                                  value=(min_year, max_year))
            else:
                years = (min_year, max_year)  # Por defecto, selecciona todos los años

            # Multiselect para seleccionar las cuencas
            basins = st.multiselect('Selecciona las cuencas', options=unique_basins, default="Seleccionar todas las cuencas")

            # Si el usuario selecciona "Seleccionar todas las cuencas", se seleccionan todas las categorías
            if "Seleccionar todas las cuencas" in basins:
                basins = filtered_df['basin_associated_with_facility'].unique()

            # Botón para aplicar los filtros
            if st.button("Aplicar filtros y mostrar gráfico"):
                # Filtrar los datos según los años y cuencas seleccionados
                filtered_df = filtered_df[(filtered_df['reporting_year'].between(years[0], years[1])) & 
                                          (filtered_df['basin_associated_with_facility'].isin(basins))]

                if not filtered_df.empty:
                    # Crear gráfico apilado
                    pivot_table = filtered_df.pivot_table(index='reporting_year', columns='industry_segment', 
                                                          values='total_reported_ch4_emissions', aggfunc='sum')

                    if not pivot_table.empty:
                        # Ajustar los colores según el número de segmentos industriales
                        colors = sns.color_palette('Set2', n_colors=min(len(pivot_table.columns), 8))
                        fig, ax = plt.subplots(figsize=(12, 8))
                        pivot_table.plot(kind='bar', stacked=True, ax=ax, color=colors)

                        ax.set(title='Emisiones de Metano por Año y Segmento Industrial',
                               xlabel='Año',
                               ylabel='Emisiones Totales de CH4 (toneladas)')
                        ax.legend(title='Segmento Industrial', bbox_to_anchor=(1.05, 1), loc='upper left')

                        # Añadir una cuadrícula suave
                        ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

                        # Mostrar el gráfico en Streamlit
                        st.pyplot(fig)
                else:
                    st.warning("No hay datos para los filtros seleccionados.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")
