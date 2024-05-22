# -*- coding: utf-8 -*-
"""
Created on May 21.04.2024

@author: Saskia Bilang, Aline Bühler, Emma Krames, Pia Obenauf
"""

import streamlit as st
import pandas as pd
import pickle
import altair as alt
import plotly.express as px
#import geopandas as gpd
#import json

# Setze die Seitenkonfiguration
st.set_page_config(
    page_title="Renovierungsapp", 
    page_icon="🏡", 
    layout="wide"
)

##### Lade das trainierte Modell
#########################################################


@st.cache_data
def load_data():
    data = pd.read_csv("./data/Modernization_compass_train.csv")
    return(data.dropna())

#kein cache möglich
def load_model():
    loaded_model = pickle.load(open("./data/finalized_modernization_model.sav", "rb"))
    return(loaded_model)

# =============================================================================
#  
# @st.cache_data
# def load_data1():
#   with open("./data/1_sehr_hoch.json") as f:
#     json_data = json.load(f)
#     gpd_data = gpd.GeoDataFrame.from_features(json_data["features"]).set_index("name")
#     return gpd_data
# data1 = load_data1()
#     
# =============================================================================
model = load_model()
data = load_data()


###### Laden der Excel files
#########################################################
gas_data = pd.read_excel("./data/Gasprice.xlsx")
kosten_data = pd.read_excel("./data/Kosten_Renovierung.xlsx")
umsatzpotentzial  =pd.read_excel("./data/umsatzpotentzial.xlsx")





##### Navigationsfunktionen
#########################################################
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
    
def go_to_welcome():
    st.session_state.page = 'welcome'

def go_to_home():
    st.session_state.page = 'home'

def go_to_data_input():
    st.session_state.page = 'data_input'

def go_to_analysis():
    st.session_state.page = 'analysis'

def go_to_dashboard():
    st.session_state.page = 'dashboard'





#### Seite 1: Welcome_Page 
#########################################################
def welcome_page():
    st.title(":blue[Fensterfix - Renovierungsapp]")
    st.write("")
    st.write("")
    st.write("Herzlich willkommen! Bitte wählen Sie, ob Sie zum Modernisierungskompass oder dem Sales-Dashboard wollen!")
    st.write("Klicken Sie auf einen der untenstehenden Buttons.")
    st.write("")
    st.write("")
    col1, col2, col3, col4= st.columns([1, 1, 1, 2])  
    
    with col1:
        st.button('**Modernisierungskompass**', on_click=go_to_home)
    with col2:
       st.button('**Sales-Dashboard**', on_click=go_to_dashboard)
        
    st.sidebar.subheader("About")
    st.sidebar.write('Diese Renovierungsapp soll den Verkäufern von Fensterfix den Alltag erleichtern. Auf der einen Seite können sie das kundenorientierte und benutzerfreundliche Verkaufstool, den "Modernisierungskompass", verwenden, um ihren Kunden das Einparpotential ihrer Immobilie aufzuzeigen. Auf der anderen Seite können sie im Sales-Dashboard einen Überblick über den Renovierungsmarkt in Deutschland erhalten und unerschöpfte Potentiale ansteuern. ')





#### Seite 2: Modernisierungskompass 
#########################################################
def home_page():
    st.title(":orange[Willkommen zum Modernisierungskompass]")
    
    col1, col2= st.columns([1, 1])  
    
    with col1:
        st.write("Liebe*r* Hausbesitzer*in*, 🏡 "
               "\n\nDiese App hilft Ihnen, die Einsparpotenziale Ihrer Gebäuderenovierungen zu berechnen. "
               "\n\nUnd stellt Ihnen passende Berater an die Seite!"
               "\n\nFinden Sie jetzt heraus wie viel Sie sparen könnnen! Klicken Sie auf den untenstehenden Button und starten Sie die Analyse")
               
        placeholder = st.empty()
        placeholder.text("                      ")
   
    with col2:
        st.image('vierfachverglasung.jpg', caption='Fensterfix-Fenster')
    
    st.button('**Dateneingabe!**', on_click=go_to_data_input, type="primary")
    st.button('Startseite', on_click=go_to_welcome)
        



#### Seite 3: Dateneingabe 
#########################################################
def data_input_page(): 
    st.title(":orange[Modernisierungskompass]")
    
    st.divider() 
    
    st.title('Um die Einsparungen zu berechnen, geben Sie bitte folgende Informationen ein:')
    
    features = list(data.columns)
    features.remove('verbkw')  
   
    
    ###CSS, um die Buttons zu designen
    st.markdown("""
        <style>
        .button-container {
            background-color: #f0f0f5;
            border: 2px solid #ccc;
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            text-align: center;
            width: 100%;
            height: 110px;  /* Ensuring equal height for buttons */
            white-space: pre-wrap;  /* Allowing line breaks within the button text */
            cursor: pointer;
            position: relative;
        }
        .button-container.selected {
            background-color: #ffe5b4;
            border: 2px solid orange;
            color: black;
        }
        .icon-title {
            display: inline-block;
        }
        .title {
            font-size: 20px;
            font-weight: bold;
            margin-left: 5px;  /* Adding a small margin between the icon and the title */
        }
        .explanation {
            font-size: 14px;
            color: #555;
            margin-top: 0;  /* Reduced margin */
        }
        .checkbox {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 24px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Funktion, um die Buttonclicks zu generieren und im Status "ausgewählt" zu lassen 
    def toggle_checkbox(option):
        if st.session_state.selected_option == option:
            st.session_state.selected_option = None  
        else:
            st.session_state.selected_option = option
    
    # Initialsieren der session state, wenn nicht bereits gemacht
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
        
    # Initialsieren der user input, wenn nicht bereits gemacht
    if 'user_input' not in st.session_state:
        st.session_state.user_input = {}
    
          
    ## Feature: Region 
    region_options = {
         0: "Sachsen",  
         2: 'Hamburg und Schleswig-Holstein und Bremen ', 
         3: 'Niedersachsen und Sachsen-Anhalt', 
         4: 'Nordrhein-Westfalen (süd)', 
         5: 'Nordrhein-Westfalen (nord)', 
         6: 'Hessen und Rheinland Pfalz und Saarland', 
         7: 'Baden-Württemberg', 
         8: 'Süd-Bayern', 
         9: 'Nord-Bayern und Thüringen', 
         1: "Berlin, Brandenburg und Mecklenburg-Vorpommern"
         }
    
    selected_region = st.selectbox('Region', list(region_options.values()))
    region_index = list(region_options.values()).index(selected_region)
    
    region_keys = ['Region_0', 'Region_1', 'Region_2', 'Region_3', 'Region_4', 'Region_5', 'Region_6', 'Region_7', 'Region_8', 'Region_9']
    for key in region_keys:
        st.session_state.user_input[key] = 0
    st.session_state.user_input[f'Region_{region_index}'] = 1
    
    
    
    ## Feature: Gebäudetyp    
    options = {
        1: ('<span class="icon">🏠</span>', "<span class='title'>Freistehend</span>", 'Ein- und Zweifamilienhäuser, Reihen-Einfamilienhäuser'), 
        2: ('<span class="icon">🏢</span>', "<span class='title'>Angebaut</span>", 'Mehrfamilienhäuser, Alterssiedlungen und -wohnungen, Mehrfamilien-Ferienhäuser, Heime')
    }
    
    # Funktion, um die selektionierte Option bestehen zu lassen
    def set_selected_option(option):
        st.session_state.selected_option = option
        st.experimental_rerun()  
    
    htype_keys = ['htyp_1', 'htyp_2']
    for key in htype_keys:
        st.session_state.user_input[key] = 0
    if st.session_state.selected_option is not None:
        st.session_state.user_input[f'htyp_{st.session_state.selected_option}'] = 1
    
    # Aufbauen der Gliederung der Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("", key='button1'):
            set_selected_option(1)
        checkbox = '<span class="checkbox">&#10003;</span>' if st.session_state.selected_option == 1 else '<span class="checkbox"></span>'
        st.markdown(f'<div class="button-container {"selected" if st.session_state.selected_option == 1 else ""}">{checkbox}<span class="icon-title">{options[1][0]}{options[1][1]}</span><br><span class="explanation">{options[1][2]}</span></div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("", key='button2'):
            set_selected_option(2)
        checkbox = '<span class="checkbox">&#10003;</span>' if st.session_state.selected_option == 2 else '<span class="checkbox"></span>'
        st.markdown(f'<div class="button-container {"selected" if st.session_state.selected_option == 2 else ""}">{checkbox}<span class="icon-title">{options[2][0]}{options[2][1]}</span><br><span class="explanation">{options[2][2]}</span></div>', unsafe_allow_html=True)
    

    ## Feature: Wohnflaeche
    def custom_slider(label, min_value, max_value, step_small, step_large):
        initial_value = min_value
        steps = list(range(min_value, 1000, step_small)) + list(range(800, max_value + 1, step_large))
        value = st.select_slider(label, options=steps, value=initial_value)
        return value
    
    # Anwendung des benutzerdefinierten Sliders
    wohnflaeche = custom_slider('Wohnfläche (m²)', min_value=0, max_value=3000, step_small=10, step_large=100)
    
    ## Feature: Baujahr
    user_input = {}
    baujahr_options = {
        1: 'bis 1918',
        2: '1919 - 1948',
        3: '1949 - 1957',
        4: '1958 - 1968',
        5: '1969 - 1978',
        6: '1979 - 1983',
        7: '1984 - 1994',
        8: '1995 - 2018',
    }
    
    def determine_baujahr_class(year):
        if year <= 1918:
            return 1
        elif year <= 1948:
            return 2
        elif year <= 1957:
            return 3
        elif year <= 1968:
            return 4
        elif year <= 1978:
            return 5
        elif year <= 1983:
            return 6
        elif year <= 1994:
            return 7
        elif year <= 2018:
            return 8
        else:
            return None
    
        
    baujahr = st.number_input('Baujahr des Hauses', min_value=0, max_value=2024, step=1)
    baujahr_index = determine_baujahr_class(baujahr)
    
    baujahr_keys = [f'baukl_{i}' for i in range(1, 9)]
    for key in baujahr_keys:
        st.session_state.user_input[key] = 0
    
    if baujahr_index is not None:
        st.session_state.user_input[f'baukl_{baujahr_index}'] = 1
        selected_baujahr = baujahr_options[baujahr_index]
    else:
        selected_baujahr = "Unknown"
    
    

    ## Feature: Verglasung
    verglasung_options = {
        1: 'Einfachverglasung', 
        2: 'Zweifachverglasung', 
        3: 'Zweifach Isolierglas', 
        4: 'Dreifachverglasung', 
        }
    selected_verglasung = st.selectbox('Verglasung', list(verglasung_options.values()))
    verglasung_index = list(verglasung_options.values()).index(selected_verglasung) + 1
    
    verglasung_keys = ['vergl_1', 'vergl_2', 'vergl_3', 'vergl_4']
    for key in verglasung_keys:
        st.session_state.user_input[key] = 0
    st.session_state.user_input[f'vergl_{verglasung_index}'] = 1
    
    
    ## Feature: Rahmen
    rah_options = {
        1: 'Holz', 
        2: 'Kunststoff', 
        3: 'Aluminium', 
        }
     
    selected_rah = st.selectbox('Fensterrahmen', list(rah_options.values()))
    rah_index = list(rah_options.values()).index(selected_rah) + 1
    
    rah_keys = ['rah_1', 'rah_2', "rah_3"]
    for key in rah_keys:
        st.session_state.user_input[key] = 0
    st.session_state.user_input[f'rah_{rah_index}'] = 1
    

    ## Feature: Art der Kellerfenster
    kellerfensterart_options = {
        1: 'Metall', 
        2: 'Kunststoff', 
        3: 'Holz', 
        }
     
    selected_kellerfensterart = st.selectbox('Art der Kellerfenster', list(kellerfensterart_options.values()))
    kellerfensterart_index = list(kellerfensterart_options.values()).index(selected_kellerfensterart) + 1
    
    kellerfensterart_keys = ['kefe_1', 'kefe_2', 'kefe_3', 'kefe_4']
    for key in kellerfensterart_keys:
        st.session_state.user_input[key] = 0
    st.session_state.user_input[f'kefe_{kellerfensterart_index}'] = 1
    
    
    ## Feature: Fensterbaujahr
    febj_config = {'type': 'number_input', 'default': 0, 'display_name': 'Baujahr der Fenster'}
    
    if febj_config['type'] == 'number_input':
        st.session_state.user_input['febj'] = st.number_input(febj_config['display_name'], value=febj_config['default'])
    
    
    ## Feature: Dicke der Tragwand
    awdi_config = {'type': 'slider', 'options': range(0, 50), 'display_name': 'Dicke der Tragwand (cm)'}
    
    if awdi_config['type'] == 'slider':
        st.session_state.user_input['awdi'] = st.slider(awdi_config['display_name'], min_value=min(awdi_config['options']), max_value=max(awdi_config['options']), value=20)  
        
    
    ## Erstellen eines neuen Dictionaries, welche nur die Features enthält, welche für das Modell genutzt werden
    def filter_dictionary(input_dict, keys_to_remove):
        """
        Entfernt die angegebenen Keys und ihre zugehörigen Values aus dem Dictionary.
    
        :param input_dict: Das ursprüngliche Dictionary.
        :param keys_to_remove: Eine Liste von Keys, die entfernt werden sollen.
        :return: Ein neues Dictionary ohne die unerwünschten Keys und Values.
        """
        return {key: value for key, value in input_dict.items() if key not in keys_to_remove}


    # Liste der zu entfernenden Keys und erstellen des neuen Dictionaries
    keys_to_remove = ["Region_1", "baukl_1", "vergl_2", "htyp_1", "kefe_1", "rah_1"]

    st.session_state.filtered_user_input = filter_dictionary(st.session_state.user_input, keys_to_remove)
    
    # Prüfen, ob die wohnflaeche eingegeben wurde
    if wohnflaeche == 0:
        st.error('Bitte geben Sie eine Wohnfläche ein!', icon="🚨")
    st.write("")
    
    # Buttons, um zu anderen Seiten zu navigieren 
    if st.button("Zu Analyse"):
        st.session_state.inputs = st.session_state.filtered_user_input
        st.session_state.wohnflaeche = wohnflaeche  # Wohnfläche speichern 
        st.session_state.baujahr = baujahr
        #st.session_state.region = region
        st.session_state.page = "analysis"
        st.experimental_rerun()
        
    st.button('Zurück zur Startseite', on_click=go_to_home) 
    
    
    
    # =============================================================================
    #     st.write("User Input Visualization:")
    #     st.dataframe(st.session_state.user_input)
    #     
    #     st.write("User Input Visualization:")
    #     st.dataframe(st.session_state.filtered_user_input)
    # =============================================================================



#### Seite 4: Analyse/ Output 
#########################################################
def analysis_page():
    st.title(":orange[Modernisierungskompass]")
    
    st.divider() 
    
    #st.subheader('Ihre Analyse für: ')
    st.title('Analyseergebnisse')
    
    
    input_df = pd.DataFrame([st.session_state.inputs])
    original_prediction = model.predict(input_df)
    
    
# =============================================================================
#     # Display original input data
#     st.subheader("Input Features for the Real Model:")
#     st.write(input_df)
# =============================================================================
    
    # Make prediction using the original input data
    original_prediction = model.predict(input_df)
    #st.write(f"Original Prediction: {original_prediction}")
    
    # Set all vergl_ columns to 0 except for vergl_4 which is set to 1
    features = list(data.columns)
    vergl_features = [f for f in features if f.startswith('vergl_')]
    for vf in vergl_features:
        input_df[vf] = 0
    if 'vergl_4' in vergl_features:  # Check if vergl_4 exists
        input_df['vergl_4'] = 1
    
# =============================================================================
#     # Display modified input data
#     st.subheader("Input Features for the Modified Model:")
#     st.write(input_df)
# =============================================================================
    
    # Make prediction using the modified input data
    modified_prediction = model.predict(input_df)
    #st.write(f"Modified Prediction: {modified_prediction}")
    
    # Calculate and display the difference
    difference = original_prediction[0]- modified_prediction[0]
    #st.write(f"Difference: {difference}")
    
# =============================================================================
#     # Display original input data
#     st.subheader("Input Features for the Real Model:")
#     st.write(input_df)
# =============================================================================
    
 
# =============================================================================
#     # Display modified input data
#     st.subheader("Input Features for the Modified Model:")
#     st.write(input_df)
#     
    
    
    #####Große if-else Schleife 
    ########################################################
    if  difference > 30000:
        st.error("Ihre Immobilie hat ein sehr hohes Einsparpotential! 🪟")
        
        st.divider()
        
        # Add more space before the button
        st.write("")
           
                
        # Predict button
        if st.button('Analyse anzeigen!'):
        
             
            st.write("")
            st.subheader('Ergebnisse: ')
            st.write("")
            st.write("")
            st.write("")
        
            # Erstellen einer Spalte für jede Karte
            col1, col2, col3 = st.columns(3)
            
            # Box für Energiekosten pro Jahr
            with col1:
                proqm = original_prediction[0]/ st.session_state.wohnflaeche
                durschnitt = ((proqm)/ 130) *100
                st.metric(label="Ihre verbrauchten Kilowattstunden pro Jahr betragen",
                          value=f"{original_prediction[0]:.2f} kWh", 
                          delta=f"Das sind {proqm:.2f} kWh pro Quadratmeter. Und {durschnitt:.2f}% mehr als der Durchschnitt.",
                          delta_color="inverse")
                st.markdown('               ')
                st.markdown('               ')
            
            # Box für Energiebedarf pro Jahr
            with col2:
                st.metric(label="Ihr Sparpotenzial in Kilowattstunden pro Jahr beträgt",
                          value=(f"{difference:.2f} kWh" ),
                          delta="1 kWh entspricht 50h Laptop-Arbeit",
                          delta_color="inverse")
                st.markdown('               ')
                st.markdown('               ')
            
            # Box für CO2-Emissionen pro Jahr
            with col3:
                 value = (original_prediction[0] * 450) / 1000  # Calculate the current CO2 
                 value2 = ((modified_prediction[0] * 450) / 1000 - value)
                 st.metric(label="Ihr CO2- Ausstoß beträgt aktuell",
                           value=f"{value:.2f} kg",
                           delta=f"Durch eine Renovierung reduzieren Sie ihren CO2 Ausstoß um {value2:.2f} kg.",
                           delta_color="inverse")
                 st.markdown('               ')
                 st.markdown('               ')
                        
            st.write("")
            st.write("") 
        
                          
            kosten_renovierung = kosten_data.loc[kosten_data['Wohnfläche'] == st.session_state.wohnflaeche, 'Preis der Erneuerung'].values[0]
        
            gas_data["Energieverbrauch_aktuell"] = original_prediction[0]
            gas_data["Energieverbrauch_nR"] = modified_prediction[0]
            gas_data["Einsparung"] = gas_data["Energieverbrauch_aktuell"] - gas_data["Energieverbrauch_nR"]
            gas_data["Kosteneinsparung"] = gas_data["Einsparung"] * gas_data["Preis"]
            gas_data["Kosteneinsparung_kumuliert"] = gas_data["Kosteneinsparung"].cumsum()
            gas_data["Preis_Renovierung"] = kosten_renovierung
                      
         
            # Vorberietung der Daten für Altair
            plot_data = gas_data[['Jahr', 'Kosteneinsparung_kumuliert', 'Preis_Renovierung']].melt('Jahr', var_name='Type', value_name='Preis')
            
            # Erstelles des des Altair chart
            line_chart = alt.Chart(plot_data).mark_line().encode(
                x=alt.X('Jahr:O', axis=alt.Axis(tickMinStep=1)),
                y='Preis:Q',
                color='Type:N'
            ).properties(
                width=600,
                height=400,
                title='Wann hat sich die Investition ausgezahlt?'
            )
        
        
            # Abbildung Linechart
            final_chart = (line_chart).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            )
        
            st.altair_chart(final_chart, use_container_width=True)
            
        
        
            st.write("")
            # Find the intersection point
            intersection_point = gas_data[gas_data["Kosteneinsparung_kumuliert"] >= kosten_renovierung]
            if not intersection_point.empty:
                 intersection_year = intersection_point.iloc[0]["Jahr"]
                 years_until_amortization = intersection_year - 2024
                 st.write(f"In {years_until_amortization:.0f} Jahren hat sich Ihre Investition in neue Fenster amortisiert!")
            else:
                 st.write("Die Renovierungskosten werden nicht innerhalb des abgebildeten Zeitrahmens gedeckt.")
            st.write("") 
            
            st.write("**Wir beraten und begleiten Sie gerne auf Ihrem Weg der Fensterrenovierung!**")
            st.write("") 
            st.write("") 
            st.divider()
            st.write("")
            #Es ist nicht möglich eine checkbox unter einem buttom einzufügen daher wird der Dataframe permanent gezeigt 
            st.write("Für unsere App-Entwickler werden hier die Daten nocheinmal in Tabellenform ausgegeben. ")
            #Den Dataframe auf dem der Graph basiert in Streamlit ausgeben
            st.dataframe(gas_data) 
            
            
            #Weitere Informationen oder Beschreibungen
            st.info("Diese Daten basieren auf prognostizierten Gaspreisen und gängigen Fensterrenovierungskosten in Deutschland.")   
        
            st.write("")
            st.write("")
            st.write("")
            st.write("") 
        
    elif 0 <= difference <= 30000:
           st.error("Ihre Immobilie hat ein hohes Einsparpotential! 🪟 ")
           
           st.divider()
           
           # Add more space before the button
           st.write("")
              
           
           # Predict button
           if st.button('Analyse anzeigen!'):
           
                
               st.write("")
               st.subheader('Ergebnisse: ')
               st.write("")
               st.write("")
               st.write("")
           
               # Erstellen einer Spalte für jede Karte
               col1, col2, col3 = st.columns(3)
               
               # Box für Energiekosten pro Jahr
               with col1:
                   proqm = original_prediction[0]/ st.session_state.wohnflaeche
                   durschnitt = ((proqm)/ 130) *100
                   st.metric(label="Ihre verbrauchten Kilowattstunden pro Jahr betragen",
                             value=f"{original_prediction[0]:.2f} kWh", 
                             delta=f"Das sind {proqm:.2f} kWh pro Quadratmeter. Und {durschnitt:.2f}% mehr als der Durchschnitt.",
                             delta_color="inverse")
                   st.markdown('               ')
                   st.markdown('               ')
               
               # Box für Energiebedarf pro Jahr
               with col2:
                   st.metric(label="Ihr Sparpotenzial in Kilowattstunden pro Jahr beträgt",
                             value=(f"{difference:.2f} kWh" ),
                             delta="1 kWh entspricht 50h Laptop-Arbeit",
                             delta_color="inverse")
                   st.markdown('               ')
                   st.markdown('               ')
               
               # Box für CO2-Emissionen pro Jahr
               with col3:
                    value = (original_prediction[0] * 450) / 1000  # Calculate the current CO2 
                    value2 = ((modified_prediction[0] * 450) / 1000 - value)
                    st.metric(label="Ihr CO2- Ausstoß beträgt aktuell",
                              value=f"{value:.2f} kg",
                              delta=f"Durch eine Renovierung reduzieren Sie ihren CO2 Ausstoß um {value2:.2f} kg.",
                              delta_color="inverse")
                    st.markdown('               ')
                    st.markdown('               ')
                           
               st.write("")
               st.write("") 
           
                             
               kosten_renovierung = kosten_data.loc[kosten_data['Wohnfläche'] == st.session_state.wohnflaeche, 'Preis der Erneuerung'].values[0]
        
               gas_data["Energieverbrauch_aktuell"] = original_prediction[0]
               gas_data["Energieverbrauch_nR"] = modified_prediction[0]
               gas_data["Einsparung"] = gas_data["Energieverbrauch_aktuell"] - gas_data["Energieverbrauch_nR"]
               gas_data["Kosteneinsparung"] = gas_data["Einsparung"] * gas_data["Preis"]
               gas_data["Kosteneinsparung_kumuliert"] = gas_data["Kosteneinsparung"].cumsum()
               gas_data["Preis_Renovierung"] = kosten_renovierung
                         
            
               # Vorberietung der Daten für Altair
               plot_data = gas_data[['Jahr', 'Kosteneinsparung_kumuliert', 'Preis_Renovierung']].melt('Jahr', var_name='Type', value_name='Preis')
               
               # Erstelles des des Altair chart
               line_chart = alt.Chart(plot_data).mark_line().encode(
                   x=alt.X('Jahr:O', axis=alt.Axis(tickMinStep=1)),
                   y='Preis:Q',
                   color='Type:N'
               ).properties(
                   width=600,
                   height=400,
                   title='Wann hat sich die Investition ausgezahlt?'
               )


               # Abbildung Linechart
               final_chart = (line_chart).configure_axis(
                   labelFontSize=12,
                   titleFontSize=14
               )

               st.altair_chart(final_chart, use_container_width=True)
               
         

               st.write("")
               # Find the intersection point
               intersection_point = gas_data[gas_data["Kosteneinsparung_kumuliert"] >= kosten_renovierung]
               if not intersection_point.empty:
                    intersection_year = intersection_point.iloc[0]["Jahr"]
                    years_until_amortization = intersection_year - 2024
                    st.write(f"In {years_until_amortization:.0f} Jahren hat sich Ihre Investition in neue Fenster amortisiert!")
               else:
                    st.write("Die Renovierungskosten werden nicht innerhalb des abgebildeten Zeitrahmens gedeckt.")
               st.write("") 
               
               st.write("**Wir beraten und begleiten Sie gerne auf Ihrem Weg der Fensterrenovierung!**")
               st.write("") 
               st.write("") 
               st.divider()
               st.write("")
               #Es ist nicht möglich eine checkbox unter einem buttom einzufügen daher wird der Dataframe permanent gezeigt 
               st.write("Für unsere App-Entwickler werden hier die Daten nocheinmal in Tabellenform ausgegeben. ")
               #Den Dataframe auf dem der Graph basiert in Streamlit ausgeben
               st.dataframe(gas_data) 
               
               
               #Weitere Informationen oder Beschreibungen
               st.info("Diese Daten basieren auf prognostizierten Gaspreisen und gängigen Fensterrenovierungskosten in Deutschland.")   

               st.write("")
               st.write("")
               st.write("")
               st.write("") 
               
               
    elif difference <= 0:
          st.success("Ihre Immobilie ist in einem sehr guten Zustand. 🎉  Hier kommen Sie zu unserer Fensterreinigungsseite.")
    

    st.button('Zurück', on_click=go_to_data_input)
    st.button('Modernisierungskompass', on_click=go_to_home)
    st.button('Startseite', on_click=go_to_welcome)
    

    





#### Seite 5: Dashboard
#########################################################
def dashboard_page():
    st.title('Sales-Dashboard')
    
    st.write("Wie sieht der aktuelle Renovierungsmarkt in Deutschland aus? ") 
    st.write("") 
    
    ################# Graph 1
    # Prepare data for Altair
    plot_data = umsatzpotentzial[['Land name', 'Umsatzpotential (Milionen) Deutschland']].melt('Land name', var_name='Type', value_name='Umsatz')
    
    bar_chart = alt.Chart(plot_data).mark_bar(color='orange').encode(
        x=alt.X('Land name:O', axis=alt.Axis(tickMinStep=1)),
        y='Umsatz:Q',
        color='Type:N'
    ).properties(
        width=600,
        height=400,
        title='Wie viele Umsatzpotential gibt es in den einzelnen Bundesländern?'
    )
        
    # Add text labels to the bars
    text = bar_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Adjust this value to place the text properly
    ).encode(
        text='Umsatz:Q'
    )
    
    # Combine the bar chart with the text labels
    final_chart = (bar_chart + text).configure_axis(
         labelFontSize=12,
         titleFontSize=14
     )

    st.altair_chart(final_chart, use_container_width=True)
    
    ################# Graph 2
    # Prepare data for Altair
    plot_data = umsatzpotentzial[['Land name', 'Anzahl Häuser Deutschland']].melt('Land name', var_name='Type', value_name='Anzahl')
    
    bar_chart = alt.Chart(plot_data).mark_bar(color='blue').encode(
        x=alt.X('Land name:O', axis=alt.Axis(tickMinStep=1)),
        y='Anzahl:Q',
        color='Type:N'
    ).properties(
        width=600,
        height=400,
        title='Wie viele zu renovierende Immobilien befinden sich in den einzelnen Bundesländern?'
    )
        
    # Add text labels to the bars
    text = bar_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10  # Adjust this value to place the text properly
    ).encode(
        text='Anzahl:Q'
    )
    
    # Combine the bar chart with the text labels
    final_chart = (bar_chart + text).configure_axis(
         labelFontSize=12,
         titleFontSize=14
     )

    st.altair_chart(final_chart, use_container_width=True)
    
# =============================================================================
#     #### Hauptanwendung ####
#     st.title("Deutschlandkarte mit Umsatzpotenzialen pro Bundesland")
#     
#     min_value = data1['Umsatzpotential'].min()
#     max_value = data1['Umsatzpotential'].max()
#     mid_value = data1['Umsatzpotential'].median()  # Or you can choose a different value
# 
#     
#     
#     fig = px.choropleth_mapbox(data1,
#                           geojson=data1.geometry,
#                           locations=data1.index,
#                           color=(data1.Umsatzpotential),
#                           center={"lat": 51.1657, "lon": 10.4515},
#                           mapbox_style="open-street-map",
#                           zoom=7,
#                           color_continuous_scale=px.colors.sequential.YlGnBu,
#                           range_color=(min_value, max_value),  # Set the range for color scale
#                           color_continuous_midpoint=mid_value,
#                           opacity=0.5,width=1600, height=800)
# 
#     st.plotly_chart(fig)
# =============================================================================
    

   
    st.button('Startseite', on_click=go_to_welcome)
    

    
# Entscheide, welche Seite basierend auf dem Zustand angezeigt wird
if st.session_state.page == 'welcome':
    welcome_page()
elif st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'data_input':
    data_input_page()
    pass
elif st.session_state.page == 'analysis':
    analysis_page()
    pass
elif st.session_state.page == 'dashboard':
    dashboard_page()
    
    