import streamlit as st
from useful_functions_st import *

def main():

    proxies = None
    
    """Fonction principale pour exécuter l'application."""
    st.title("Backtesting tempêtes tropicales")

    # Affichage des options dans la barre latérale
    option = render_sidebar()
       

    if option == 'Charger les données':

        template_path = "template.xlsx"  # Remplacez par le chemin réel de votre fichier template
        download_template(template_path)
        
        st.subheader("Charger un fichier Excel")

        # Télécharger le fichier
        uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])
        
        # Vérifiez si un fichier a été téléchargé
        if uploaded_file is not None:
            # Lisez le fichier Excel dans un DataFrame
            df_client_sites = pd.read_excel(uploaded_file)
            
            # Affichez le DataFrame
            st.write(df_client_sites)
        else:
            st.write("Veuillez télécharger un fichier Excel.")

        if uploaded_file:
            display_excel_content(df_client_sites)
        else:
            st.warning("Veuillez télécharger un fichier Excel pour continuer.")

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
            df_compar_expositions = points_in_polygons_(df_client_sites, gdf)

    

if __name__ == "__main__":
    main()
