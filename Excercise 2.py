import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Título de la aplicación
st.title('Visualización de Emisiones de Metano por Empresa')

# Paso 1: Cargar el archivo Excel
file_path = st.file_uploader("Sube el archivo Excel con los datos", type="xlsx")

@st.cache_data
def cargar_datos(file):
    emissions_df = pd.read_excel(file, sheet_name='ef_w_emissions_source_ghg', 
                                 usecols=['facility_id', 'reporting_year', 'total_reported_ch4_emissions', 'reporting_category', 'basin_associated_with_facility'])
    facilities_df = pd.read_excel(file, sheet_name='rlps_ghg_emitter_facilities', usecols=['facility_id', 'parent_company'])
    return pd.merge(emissions_df, facilities_df, on='facility_id', how='inner')

if file_path is not None:
    try:
        sheet_names = pd.ExcelFile(file_path).sheet_names
        if 'ef_w_emissions_source_ghg' not in sheet_names or 'rlps_ghg_emitter_facilities' not in sheet_names:
            st.error("El archivo Excel no contiene las hojas requeridas.")
        else:
            merged_df = cargar_datos(file_path)

            # Filtrar las columnas relevantes
            filtered_df = merged_df[['reporting_year', 'total_reported_ch4_emissions', 'parent_company', 'reporting_category', 'basin_associated_with_facility']]
            filtered_df['reporting_year'] = pd.to_numeric(filtered_df['reporting_year'], errors='coerce')

            # Obtener el rango de años y los basins únicos
            min_year = int(filtered_df['reporting_year'].min())
            max_year = int(filtered_df['reporting_year'].max())
            unique_basins = filtered_df['basin_associated_with_facility'].unique().tolist()

            # Agregar la opción "Seleccionar todas las fuentes"
            unique_basins.insert(0, "Seleccionar todas las cuencas")

            # Paso 2: Mostrar los filtros
            st.write("### Filtros para los datos")

            # Slider para seleccionar el año
            year_selected = st.selectbox("Selecciona el año", sorted(filtered_df['reporting_year'].unique(), reverse=True))

            # Multiselect para seleccionar las cuencas
            basins = st.multiselect('Selecciona las cuencas', options=unique_basins, default="Seleccionar todas las cuencas")

            # Si el usuario selecciona "Seleccionar todas las cuencas", se seleccionan todas las categorías
            if "Seleccionar todas las cuencas" in basins:
                basins = filtered_df['basin_associated_with_facility'].unique()

            # Botón para aplicar los filtros
            if st.button("Aplicar filtros y mostrar gráfico"):
                filtered_df = filtered_df[(filtered_df['reporting_year'] == year_selected) & 
                                          (filtered_df['basin_associated_with_facility'].isin(basins))]

                if not filtered_df.empty:
                    # Crear una tabla dinámica para el gráfico
                    pivot_table = filtered_df.pivot_table(index='parent_company', columns='reporting_category', 
                                                          values='total_reported_ch4_emissions', aggfunc='sum')

                    # Ordenar por emisiones totales y mostrar solo las top 10 empresas con más emisiones
                    pivot_table['Total Emissions'] = pivot_table.sum(axis=1)
                    pivot_table = pivot_table.sort_values(by='Total Emissions', ascending=False).head(10)
                    pivot_table = pivot_table.drop(columns=['Total Emissions'])  # Quitar la columna auxiliar

                    if not pivot_table.empty:
                        # Ajustar los colores según el número de categorías
                        colors = sns.color_palette('Set2', n_colors=min(len(pivot_table.columns), 8))
                        
                        # Cambiar el gráfico a barras horizontales apiladas
                        fig, ax = plt.subplots(figsize=(10, 6 + 0.5 * len(pivot_table)))  # Ajustar el tamaño dinámicamente
                        pivot_table.plot(kind='barh', stacked=True, ax=ax, color=colors)

                        ax.set(title='Top 10 Empresas con más Emisiones de Metano',
                               xlabel='Emisiones Totales de CH4 (toneladas)',
                               ylabel='Empresa')
                        ax.legend(title='Fuente de Emisión', bbox_to_anchor=(1.05, 1), loc='upper left')

                        # Añadir cuadrícula
                        ax.grid(True, which='both', axis='x', linestyle='--', linewidth=0.7, alpha=0.7)

                        # Mostrar el gráfico en Streamlit
                        st.pyplot(fig)
                else:
                    st.warning("No hay datos para los filtros seleccionados.")
    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {str(e)}")