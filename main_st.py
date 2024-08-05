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
        uploaded_file = file_uploader()

        if uploaded_file:
            display_excel_content(uploaded_file)
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
            gdf = kml_to_geojson(kml_data)

                
    
            except Exception as e:
                st.error(f"Error processing the KML file: {e}")
    
    

if __name__ == "__main__":
    main()
