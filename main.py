import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import mpld3
import streamlit.components.v1 as components
import datetime
from streamlit_option_menu import option_menu
import date_manage as dm
import custom_components_css as ccs
import plotly.express as px
import json
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):

    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottiefile(filepath: str):
    with open(filepath, 'r') as f:
        return json.load(f)

# lottie_url = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_xo8yHWrXSL.json")

# ---------------------------------------------- Configuration du site -------------------------------------------
# https://www.webfx.com/tools/emoji-cheat-sheet/

hexa_color_site = {'data_header_bg': "#174f8a",
                   'data_header_font_color': 'white',
                   'sidebar_color_bg': "#9bc2eb",
                   'metric_color': '#f2f2f0'}

st.set_page_config(page_icon=':bar_chart:', page_title='Stock Viz', layout='wide')
ccs.CustomComponents.sidebar_color(hexa_color_site['sidebar_color_bg'])
ccs.CustomComponents.hide_generator_streamlit()

st.title(':bar_chart: Stock Viz')

st.markdown('---')

# ----------------------------------------------- Gestion des données --------------------------------------------

data = pd.read_csv(r"C:\Users\Antoine\Desktop\antoine_29_07_2021\Data Science\Dataset\Regression\stock10yrs.csv", index_col='date', parse_dates=True)
data.drop('Unnamed: 12', axis=1, inplace=True)
data['b_mkt'] = data['b_mkt'].replace('AAPL44547', 0)
data['b_mkt'] = data['b_mkt'].astype(float)
data.fillna(value={'b_mkt': data['b_mkt'].mean(),
                   'b_smb': data['b_smb'].mean(),
                   'b_hml': data['b_hml'].mean(),
                   'BID': data['BID'].mean(),
                   'ASK': data['ASK'].mean()}, inplace=True)
data.rename(columns={'PRC': 'Close'}, inplace=True)

df = data
columns_keep = ['AAPL', 'JPM', 'XOM', 'AMZN']
df = df[df.TICKER.isin(columns_keep)]
data_graph = df.drop('uniqueval', axis=1)

# ---------------------------------------------- Menu des entreprises --------------------------------------------

st.subheader('Entreprise à analyser')

translate_company_name = {'EXXON MOBIL': 'XOM',
                          'APPLE': 'AAPL',
                          'JP MORGAN': 'JPM',
                          'AMAZON': 'AMZN'}

company = option_menu(None, ['EXXON MOBIL', 'APPLE', 'JP MORGAN', 'AMAZON'],
                      icons=['droplet', 'phone', 'building', 'mailbox'],
                      menu_icon="cast",
                      default_index=0,
                      orientation="horizontal",
                      styles={
                        "container": {"padding": "0!important", "background-color": "#fafafa"},
                        "icon": {"color": "orange", "font-size": "25px"},
                        "nav-link": {"font-size": "25px", "text-align": "right", "margin": "0px", "--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "#3b598a"},
                        })

# Altération des données

df = df.loc[df['TICKER'] == translate_company_name[company]]

# ----------------------------------------- Période ---------------------------------------------------------------'''

st.sidebar.title(f"Période actualisable")
st.sidebar.markdown(f"<h4>{str(df.index.min())[:10]} - {str(df.index.max())[:10]}</h4>", unsafe_allow_html=True)

first_date = st.sidebar.date_input('Du', value=df.index.max() - datetime.timedelta(60))
end_date = st.sidebar.date_input('Au', value=df.index.max())

st.sidebar.markdown('---')

boolean_date = first_date > end_date

if boolean_date:
    st.error(f":warning: Vous ne pouvez pas sélectionner une date de fin supérieure à la date de début de période")
    lottie_download = load_lottiefile("C:/Users/Antoine/PycharmProjects/StockAnalysis/template/error.json")
    st_lottie(lottie_download, height=600)

else:

    # ---------------------------------------- Fin de période ---------------------------------------------------------'''

    # Récupération de la date pour le beta ------------------------------------------------------------------------------

    looking_first_date = dm.date_search(df, first_date)
    date_return_start = str(looking_first_date.return_date_exist())[:10]

    looking_end_date_for_beta = dm.date_search(df, end_date)
    date_return_end = str(looking_end_date_for_beta.return_date_exist())[:10]

    # Format str to date

    date_return_start_date_format = datetime.datetime.strptime(date_return_start, '%Y-%m-%d').date()
    date_return_end_date_format = datetime.datetime.strptime(date_return_end, '%Y-%m-%d').date()


    # Condition ---------------------------------------------------------------------------------------------------------

    if looking_end_date_for_beta.statut:
        st.warning(f":warning: La date {end_date} n'est pas répertoriée, veuillez saisir une date entre la période du {df.index.min().date()} au {df.index.max().date()}")
        lottie_download = load_lottiefile("C:/Users/Antoine/PycharmProjects/StockAnalysis/template/warning.json")
        st_lottie(lottie_download, height=600)

    else:
        market_beta_asset = float(round(df.loc[date_return_end]['b_mkt'], 2))
        market_beta_size = float(round(df.loc[date_return_end]['b_smb'], 2))
        market_beta_value = float(round(df.loc[date_return_end]['b_hml'], 2))

        # "b_smb" : représente le coefficient de sensibilité d'un actif aux variations du facteur "Size" (taille) qui mesure
        #          la performance des entreprises en fonction de leur capitalisation boursière. Un coefficient positif
        #          indique que l'actif est plus sensible aux mouvements du facteur "Size", ce qui signifie qu'il a tendance
        #          à mieux performer dans un environnement où les petites entreprises sont en hausse.

        # "b_hml" : représente le coefficient de sensibilité d'un actif aux variations du facteur "Value" (valeur) qui
        #           mesure la performance des entreprises en fonction de leur ratio valeur/bénéfice. Un coefficient positif indique
        #           que l'actif est plus sensible aux mouvements du facteur "Value", ce qui signifie qu'il a tendance à mieux performer
        #           dans un environnement où les entreprises "value" sont en hausse.

        st.markdown('')
        st.markdown(f"<h6>Fama-French Three-Factor Model | coefficient du {date_return_end}</h6>", unsafe_allow_html=True)

        metric_side_left, metric_side_mid, metric_side_right = st.columns(3)

        def get_icon(value):
            if value < 0:
                return ":exclamation:"
            else:
                return ":chart:"

        with metric_side_left:
            st.subheader("B_MKT")
            if market_beta_asset < 0:
                ccs.CustomComponents.style_markdown(market_beta_asset, balise='header', bgcolor='#f5959a', radius='8px', padding='8px')
            else:
                ccs.CustomComponents.style_markdown(market_beta_asset, balise='header', bgcolor="#b0d4b4", radius='8px', padding='8px')

        with metric_side_mid:
            st.subheader("B_SMB")
            if market_beta_size < 0:
                ccs.CustomComponents.style_markdown(market_beta_size, balise='header', bgcolor='#f5959a', radius='8px', padding='8px')
            else:
                ccs.CustomComponents.style_markdown(market_beta_size, balise='header', bgcolor="#b0d4b4", radius='8px', padding='8px')

        with metric_side_right:
            st.subheader("B_HML")
            if market_beta_value < 0:
                ccs.CustomComponents.style_markdown(market_beta_value, balise='header', bgcolor='#f5959a', radius='8px',
                                                    padding='8px')
            else:
                ccs.CustomComponents.style_markdown(market_beta_value, balise='header', bgcolor="#b0d4b4", radius='8px',
                                                    padding='8px')

        # Slicing chart function ---------------------------------------------------------------------------------------

        def relative_date(date, delta: int):
            delta_date = date - datetime.timedelta(delta)
            return delta_date

        def get_x(data_graph):
            x = np.array(range(data_graph.index.size))
            x = x.reshape(x.shape[0], 1)
            return x

        def return_line_mark():
            return st.markdown('---')

        def return_blank_mark():
            return st.markdown('')

        def return_export_button(data):
            return data.to_csv('données.xlsx', encoding='utf-8')

        def r2_score(ypred, y):
            numerator = np.sum((y - ypred)**2)
            denumerator = np.sum((y - np.mean(y))**2)
            return round(1 - (numerator / denumerator), 2)


        # Chart --------------------------------------------------------------------------------------------------------

        st.markdown('')

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()

        tabs = ['Période', 'Année', 'Mois', 'Semaine']

        selection, year, month, week = st.tabs(tabs)
        ccs.CustomComponents.style_tabs()

        metric_mean = None


        # Période ----------------------------------------------------------------------------------------------------------

        with selection:
            data_graph = data_graph.loc[data_graph['TICKER'] == translate_company_name[company]][
                         date_return_start_date_format:date_return_end_date_format].sort_index()

            x, y = get_x(data_graph), data_graph['Close']
            model.fit(x, y)

            data_graph['Régression linéaire'] = model.predict(x)
            data_graph['Moyenne 5 jours'] = data_graph['Close'].rolling(window=5).mean()

            metric_mean = round(data_graph['Moyenne 5 jours'].mean(), 1)

            fig = px.line(data_graph,
                          y=['Close', 'Régression linéaire', 'Moyenne 5 jours'],
                          title=f"Cours boursier de {company} du {first_date} au {end_date}")

            st.plotly_chart(fig, use_container_width=True)

            # Data ---------------------------------------

            return_blank_mark()

            reg_coef, mean_coef, r2_score_metric = st.columns(3)

            with reg_coef:
                st.subheader('Pente de régression')
                ccs.CustomComponents.style_markdown(text=round(float(model.coef_), 2),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with mean_coef:
                st.subheader('Moyenne du cours')
                ccs.CustomComponents.style_markdown(text=metric_mean,
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with r2_score_metric:
                st.subheader('R2')
                ccs.CustomComponents.style_markdown(text=r2_score(data_graph['Régression linéaire'], data_graph['Close']),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            st.markdown('---')

            ccs.CustomComponents.style_markdown(
                text=f"Données de {company} du {first_date} au {end_date}",
                balise='subheader',
                bgcolor=hexa_color_site['data_header_bg'],
                radius='8px',
                padding='14px',
                fontcolor=hexa_color_site['data_header_font_color'])

            return_blank_mark()

            st.dataframe(data_graph, use_container_width=True)
            export_button_period = st.button('Exportez les données sur Excel | Période sélectionné')

            if export_button_period:
                return_export_button(data_graph)

        # Année ------------------------------------------------------------------------------------------------------------

        with year:
            year_delta = relative_date(end_date, 365)

            data_graph = data_graph.loc[data_graph['TICKER'] == translate_company_name[company]][
                             year_delta:date_return_end_date_format].sort_index()

            x, y = get_x(data_graph), data_graph['Close']
            model.fit(x, y)

            data_graph['Régression linéaire'] = model.predict(x)
            data_graph['Moyenne 5 jours'] = data_graph['Close'].rolling(window=5).mean()

            metric_mean = round(data_graph['Moyenne 5 jours'].mean(), 1)

            fig = px.line(data_graph,
                              y=['Close', 'Régression linéaire', 'Moyenne 5 jours'],
                              title=f"Cours boursier de {company} du {year_delta} au {date_return_end_date_format}")

            st.plotly_chart(fig, use_container_width=800)

            return_blank_mark()

            reg_coef, mean_coef, r2_score_metric = st.columns(3)

            with reg_coef:
                st.subheader('Pente de régression')
                ccs.CustomComponents.style_markdown(text=round(float(model.coef_), 2),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with mean_coef:
                st.subheader('Moyenne du cours')
                ccs.CustomComponents.style_markdown(text=metric_mean,
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with r2_score_metric:
                st.subheader('R2')
                ccs.CustomComponents.style_markdown(text=r2_score(data_graph['Régression linéaire'], data_graph['Close']),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            st.markdown('---')

            ccs.CustomComponents.style_markdown(
                text=f"Données de {company} du {year_delta} au {date_return_end_date_format}",
                balise='subheader',
                bgcolor=hexa_color_site['data_header_bg'],
                radius='8px',
                padding='14px',
                fontcolor=hexa_color_site['data_header_font_color'])

            return_blank_mark()

            st.dataframe(data_graph, use_container_width=True)
            export_button_year = st.button("Exportez les données sur Excel | Année")

            if export_button_year:
                return_export_button(data_graph)


        # MOIS -------------------------------------------------------------------------------------------------------------

        with month:
            year_delta = relative_date(end_date, 30)

            data_graph = data_graph.loc[data_graph['TICKER'] == translate_company_name[company]][
                             year_delta:date_return_end_date_format].sort_index()

            x, y = get_x(data_graph), data_graph['Close']
            model.fit(x, y)

            data_graph['Régression linéaire'] = model.predict(x)
            data_graph['Moyenne 5 jours'] = data_graph['Close'].rolling(window=5).mean()

            metric_mean = round(data_graph['Moyenne 5 jours'].mean(), 1)

            fig = px.line(data_graph,
                              y=['Close', 'Régression linéaire', 'Moyenne 5 jours'],
                              title=f"Cours boursier de {company} du {year_delta} au {date_return_end_date_format}")

            st.plotly_chart(fig, use_container_width=800)

            return_blank_mark()

            reg_coef, mean_coef, r2_score_metric = st.columns(3)

            with reg_coef:
                st.subheader('Pente de régression')
                ccs.CustomComponents.style_markdown(text=round(float(model.coef_), 2),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with mean_coef:
                st.subheader('Moyenne du cours')
                ccs.CustomComponents.style_markdown(text=metric_mean,
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with r2_score_metric:
                st.subheader('R2')
                ccs.CustomComponents.style_markdown(text=r2_score(data_graph['Régression linéaire'], data_graph['Close']),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            st.markdown('---')

            ccs.CustomComponents.style_markdown(
                text=f"Données de {company} du {year_delta} au {date_return_end_date_format}",
                balise='subheader',
                bgcolor=hexa_color_site['data_header_bg'],
                radius='8px',
                padding='14px',
                fontcolor=hexa_color_site['data_header_font_color'])

            return_blank_mark()

            st.dataframe(data_graph, use_container_width=True)
            export_button_month = st.button('Exportez les données sur Excel | Mois')

            if export_button_month:
                return_export_button(data_graph)



        # Semaine ----------------------------------------------------------------------------------------------------------

        with week:
            year_delta = relative_date(end_date, 7)

            data_graph = data_graph.loc[data_graph['TICKER'] == translate_company_name[company]][
                             year_delta:date_return_end_date_format].sort_index()

            x, y = get_x(data_graph), data_graph['Close']
            model.fit(x, y)

            data_graph['Régression linéaire'] = model.predict(x)
            data_graph['Moyenne 2 jours'] = data_graph['Close'].rolling(window=2).mean()

            metric_mean = round(data_graph['Moyenne 2 jours'].mean(), 1)

            fig = px.line(data_graph,
                              y=['Close', 'Régression linéaire', 'Moyenne 5 jours'],
                              title=f"Cours boursier de {company} du {year_delta} au {date_return_end_date_format}")

            st.plotly_chart(fig, use_container_width=800)

            return_blank_mark()

            reg_coef, mean_coef, r2_score_metric = st.columns(3)

            with reg_coef:
                st.subheader('Pente de régression')
                ccs.CustomComponents.style_markdown(text=round(float(model.coef_), 2),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with mean_coef:
                st.subheader('Moyenne du cours')
                ccs.CustomComponents.style_markdown(text=metric_mean,
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')

            with r2_score_metric:
                st.subheader('R2')
                ccs.CustomComponents.style_markdown(text=r2_score(data_graph['Régression linéaire'], data_graph['Close']),
                                                    balise='text',
                                                    bgcolor=hexa_color_site['metric_color'],
                                                    radius='8px',
                                                    padding='10px')


            st.markdown('---')

            ccs.CustomComponents.style_markdown(text=f"Données de {company} du {year_delta} au {date_return_end_date_format}",
                                                balise='subheader',
                                                bgcolor=hexa_color_site['data_header_bg'],
                                                radius='8px',
                                                padding='14px',
                                                fontcolor=hexa_color_site['data_header_font_color'])

            return_blank_mark()

            st.dataframe(data_graph, use_container_width=True)
            export_button_week = st.button('Exportez les données sur Excel | Semaine')

            if export_button_week:
                return_export_button(data_graph)


        # st.sidebar.metric('r2', value=r2_score(data_graph['Régression linéaire'], data_graph['Close']))
    st.markdown("<style>.reportview-container {background-color:red;}</style>", unsafe_allow_html=True)