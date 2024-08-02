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
        render_analysis_options(proxies)

if __name__ == "__main__":
    main()
