import pandas as pd
import streamlit as st
from datetime import date
from io import BytesIO
import zipfile
import requests
import os
from functions_backtest import *

def dezip_kmz(response):
    try:
        kmz = zipfile.ZipFile(BytesIO(response.content))
        kml_filename = None
        for filename in kmz.namelist():
            if filename.lower().endswith('.kml'):
                kml_filename = filename
                name_kml = re.findall(r"(.*).kml",kml_filename)[0]
                break
        if kml_filename is None:
            raise Exception('KML file not found in KMZ archive')
    except Exception as e:
        print("Erreur dans la fonction v1_13_dezipp_kmz: impossible de dezipper le kmz en kml")
        print(e)
    
    try:
        kml_content = kmz.read(kml_filename).decode('utf-8')
    except Exception as e:  
        kml_content = "NA"

    return kml_content

def format_datetime(selected_date, selected_hour):
    """Formater la date et l'heure en format AAAAMMJJHH."""
    hour_map = {"00h": "00", "06h": "06", "12h": "12", "18h": "18"}
    date_str = selected_date.strftime("%Y%m%d")
    hour_str = hour_map[selected_hour]
    return f"{date_str}{hour_str}"

def file_uploader():
    """Fonction pour créer un widget de téléchargement de fichier."""
    return st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

def display_excel_content(uploaded_file):
    """Fonction pour lire et afficher le contenu du fichier Excel."""
    try:
        # Lire le fichier Excel avec pandas
        df = pd.read_excel(uploaded_file)
        st.success("Fichier chargé avec succès!")
        st.write("Voici les premières lignes du fichier :")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")

def download_template(file_path):
    
    """Fonction pour télécharger un fichier template."""
    with open(file_path, "rb") as file:
        btn = st.download_button(
            label="Télécharger le template",
            data=file,
            file_name="template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    return btn

def render_sidebar():
    """Fonction pour afficher les options dans la barre latérale."""
    st.sidebar.title("Options")
    option = st.sidebar.radio(
        "Naviguer vers",
        ('Charger les données','Choix de la tempête')
    )
    return option

def download_kmz_file(date_str,proxies):
    """Télécharge le fichier KMZ correspondant à la date donnée, le dézippe, et l'enregistre dans le cache."""
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Remplacez l'URL par l'URL correcte du site
    base_url = "https://www.nhc.noaa.gov/gis/forecast/archive"
    if date_str==None:
        kmz_url = f"{base_url}/latest_wsp64knt120hr_5km.kmz"
        file_path = os.path.join(cache_dir, f"latest.kml")
    else:
        kmz_url = f"{base_url}/{date_str}_wsp64knt120hr_5km.kmz"
        file_path = os.path.join(cache_dir, f"{date_str}.kml")

    response = requests.get(kmz_url,proxies=proxies,verify=False)
    response.raise_for_status()
    kmz_content = BytesIO(response.content)
    kml_content = dezip_kmz(response)
    # Stocker le fichier dans le cache de Streamlit
    with open(file_path, 'wb') as f:
        f.write(kml_content.encode('utf-8'))
        
def render_analysis_options(proxies):
    """Fonction pour afficher les options d'analyse dans la barre latérale."""
    analysis_option = st.radio(
        "Choisissez l'option d'analyse",
        ('Temps réel', 'Vision à une date précise', 'Sélection d\'un intervalle de dates', 'Choix d\'une tempête')
    )
    if analysis_option == 'Temps réel':
        try:
            download_kmz_file(None,proxies)
            datetime=None
            st.success(f"Fichier KML a téléchargé avec succès et stocké dans le cache.")
        except Exception as e:
            st.error(f"Erreur lors du téléchargement du fichier d'informations de la tempête. Merci de réessayer ultérieurement\n{e}.")
    
    elif analysis_option == 'Vision à une date précise':
        date_selected = st.date_input("Choisissez une date", value=date.today())
        hour_selected = st.selectbox("Choisissez une heure", ["00h", "06h", "12h", "18h"])
        datetime=format_datetime(date_selected,hour_selected)
        try:
            download_kmz_file(datetime,proxies)
            st.success(f"Fichier KML pour {datetime} téléchargé avec succès et stocké dans le cache.")
        except Exception as e:
            st.error(f"Erreur lors du téléchargement du fichier d'informations de la tempête. Merci de réessayer\n{e}.")
        st.write(f"Date sélectionnée : {date_selected}, {hour_selected}")

    elif analysis_option == 'Sélection d\'un intervalle de dates':
        start_date = st.date_input("Date de début", value=date.today())
        start_hour = st.selectbox("Heure de début", ["00h", "06h", "12h", "18h"], key="start_hour")
        end_date = st.date_input("Date de fin", value=date.today())
        end_hour = st.selectbox("Heure de fin", ["00h", "06h", "12h", "18h"], key="end_hour")
    
        st.write(f"Intervalle sélectionné : de {start_date} {start_hour} à {end_date} {end_hour}")

    elif analysis_option == 'Choix d\'une tempête':
        storm_selected = st.selectbox("Choisissez une tempête", ['IRMA', 'MARIA', 'HARVEY', 'BERYL'])
        st.write(f"Tempête sélectionnée: {storm_selected}")

    return analysis_option,datetime
