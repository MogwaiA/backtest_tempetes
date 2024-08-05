import streamlit as st
from useful_functions_st import *

def main():

    proxies = None
    
    """Fonction principale pour exécuter l'application."""
    st.title("Backtesting tempêtes tropicales")

    # Affichage des options dans la barre latérale
    option = render_sidebar()
       

    if option == 'Charger les données':
        if "df_client_sites" not in st.session_state:
            st.session_state.df_client_sites = None
            
        template_path = "template.xlsx"  # Remplacez par le chemin réel de votre fichier template
        download_template(template_path)
        
        st.subheader("Charger un fichier Excel")

        # Fonction pour uploader le fichier
        file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])
        
        if file is not None:
            # Charger les données dans un DataFrame et le mettre en cache
            st.session_state.df_client_sites = load_data(file)

        else:
            st.warning("Veuillez télécharger un fichier Excel pour continuer.")
        
        # Si le DataFrame est chargé, l'afficher
        if st.session_state.df_client_sites is not None:
            st.dataframe(st.session_state.df_client_sites)

    elif option == 'Choix de la tempête':
        st.subheader("Options d'analyse")
        option=render_analysis_options(proxies)
        choice=option[0]
        date_str=option[1]

        cache_dir="cache"
        if choice=='Vision à une date précise':
            file_path = os.path.join(cache_dir, f"{date_str}.kml")
            with open(file_path, "r", encoding="utf-8") as f:
                    kml_data = f.read()
            gdf = kml_to_geojson(file_path)
            #df_compar_expositions = points_in_polygons_(st.session_state.df_client_sites, gdf)

            points_in_polygons = []
            geometry_points = [Point(xy) for xy in zip(st.session_state.df_client_sites['LON'], st.session_state.df_client_sites['LAT'])]
            gdf_points = gpd.GeoDataFrame(st.session_state.df_client_sites, geometry=geometry_points)
            for point in gdf_points.iterrows():
                for poly in gdf.iterrows():
                    if point[1]['geometry'].within(poly[1]['Geometry']):
                        point_data = point[1].copy()  # Copier les données du point
                        point_data['POLYGON_AREA'] = poly[1]['Name']  # Ajouter la valeur 'Name' du polygone
                        point_data['LEVEL']=poly[1]['level']
                        points_in_polygons.append(point_data)
        
            result_df = gpd.GeoDataFrame(points_in_polygons)
            st.dataframe(result_df)
    
            

    

if __name__ == "__main__":
    main()
