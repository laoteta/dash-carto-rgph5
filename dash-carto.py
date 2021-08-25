import dash
from dash.development.base_component import Component
from dash_core_components.Dropdown import Dropdown
from pandas.core.frame import DataFrame
import plotly.express as px
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

# Exploration des données avec pandas
#-----------------------------------------

df = pd.read_excel("dagl.xlsx")
#print(df)

"""
#print(df[:5]) # Affiche les 5 premières lignes
#print(df.iloc[:5,[0,3]])  # Affiche les 5 premières lignes des colonnes 0 et 3

#print(df.loc[:5,["Population estimée"]]) # Affiche les 5 premières lignes de la colonne "Population estimée"
#print(df.Région.nunique())
#print(df.Région.unique())
#print(df.POPULATION.nunique())
#print(sorted(df.POPULATION.unique()))

# Analyse de données
#print(df.head())# affiche les 5 premières lignes
#print(df.tail())# affiche les 5 dernières lignes
print(df.shape)# affiche le nombre de lignes et de colonne
print(df.columns)# affiche les informations sur les colonnes
print(df.columns.tolist())# transforme en liste python les informations sur les colonnes
print(df.index)#affiche les informations sur l'index
#df.set_index("email", implace)# change l'index avec 
#df = df.set_index("email")# change l'index avec 

# selection des elements
#print(df["PREFECTURE"].head())
print(type(df))
print(df.PREFECTURE.head())
print(type(df.PREFECTURE))

"""

# Visualisation des données avec plotly
#-----------------------------------------
fig_pie = px.pie(data_frame=df, names="CHEF D'EQUIPE",values='POPULATION')
#fig_pie = px.pie(data_frame=df, names="CHEF D'EQUIPE",values='CONCESSIONS AVEC REFUS')
#fig_pie.show()


# bar
fig_bar = px.bar(data_frame=df, x="CHEF D'EQUIPE",y="POPULATION")
#fig_bar.show()

# histogramme
fig_his = px.histogram(data_frame=df, x="CHEF D'EQUIPE",y="POPULATION")
#fig_his.show()

#Graphique Interactive avec Dash
app = dash.Dash(__name__)
server = app.server

app.layout=html.Div([
    html.H1("Population estimée par Chef d'equipe et par Quartier / Canton"),
    dcc.Dropdown(id='genre-choice',
                 options=[{'label':x, 'value':x}
                 for x in sorted(df["CHEF D'EQUIPE"].unique())],
                 value='ABOUDOU Julien Komivi Sodjinè'#Choix par défaut
                 ),
    dcc.Graph(id='my-graph', figure={})
])

@app.callback(
    Output('my-graph', 'figure'),
     Input('genre-choice', 'value')
)
def interactive_graphing(value_genre):
    print(value_genre)
    dff = df[df["CHEF D'EQUIPE"]==value_genre]
    fig = px.histogram(data_frame=dff, x="CANTON",y="POPULATION",title="Population estiméeeee")
    return fig

if __name__=='__main__':
    app.run_server()
