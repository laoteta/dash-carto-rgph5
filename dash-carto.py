import pandas as pd
#import plotly
import plotly.express as px
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

""""
from dash.development.base_component import Component
from dash_core_components.Dropdown import Dropdown
from pandas.core.frame import DataFrame

"""

app = dash.Dash(__name__)
server = app.server



# Exploration des données avec pandas
#-----------------------------------------

df = pd.read_excel("dagl.xlsx")
#print(df)


dff = df.groupby("CHEF D'EQUIPE",as_index=False)[
    [
        "POPULATION",
        "NOMBRE CONCESSIONS",
        "NOMBRE INFRASTRUCTURES",
        "CONCESSIONS AVEC OCCUPANTS PRESENTS",
        "CONCESSIONS AVEC OCCUPANTS ABSENTS",
        "CONCESSIONS INOCCUPEES",
        "CONCESSIONS EN CONSTRUCTION",
        "CONCESSIONS AVEC REFUS",
        "CONCESSIONS ABRITANT INFRASTRUCTURE"
    ]
].sum()
print(dff[:5])


app.layout = html.Div([
        #html.H1("Population estimée par Chef d'equipe et par Quartier / Canton"),
        html.Div([
            dash_table.DataTable(
                id='datatable_id',
                data=dff.to_dict('records'),
                columns=[
                    {
                        "name": i,
                        "id": i,
                        "deletable": False, #suppression de la colonne
                        "selectable": False,#selection des colonnes
                        "hideable": False,#cache la colonne
                    }
                    for i in dff.columns
                ],
                editable=False, # permettre la modification des données à l'intérieur de toutes les cellules
                filter_action="native", # autoriser le filtrage des données par utilisateur
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",# single ou multi
                row_selectable="multi", # mode de selection des lignes
                row_deletable=False,
                selected_rows=[],
                selected_columns=[],
                page_action="native",
                page_current=0,
                page_size=6,

                # page_action="none",
                style_cell={
                     'whiteSpace':'normal'
                },
                # fixed_rows={'headers':True, 'data':0},
                # virtualization=False,

                style_data_conditional=[
                    {'if':{'column_id':"CHEF D'EQUIPE"},'width':'20%','textAlign':'left'},
                    #{'if':{'column_id':"POPULATION"},'width':'5%','textAlign':'right'},
                    #{'if':{'column_id':"NOMBRE CONCESSIONS"},'width':'5%','textAlign':'right'},
                    #{'if':{'column_id':"NOMBRE INFRASTRUCTURES"},'width':'5%','textAlign':'right'},
                ],

            ),
        ],className='row'),


        html.Div([

            html.Div([
                 dcc.Dropdown(id='linedropdown',
                    options=[
                        #{'label': 'Population', 'value': "POPULATION"}
                        #{'label': 'Nb Concessions', 'value': "NOMBRE CONCESSIONS"},
                        #{'label': 'NB Infrastrures', 'value': "NOMBRE INFRASTRUCTURES"}
                        ],
                        value='POPULATION',
                        multi=False,
                        clearable=False
                        ),
                      ],className='six columns'),

            html.Div([
                 dcc.Dropdown(id='piedropdpwn',
                    options=[

                            #{'label': 'Population', 'value': "POPULATION"},
                            #{'label': 'Nb Concessions', 'value': "NOMBRE CONCESSIONS"},
                            #{'label': 'NB Infrastrures', 'value': "NOMBRE INFRASTRUCTURES"}
                             ],
                                value='NOMBRE CONCESSIONS',
                                multi=False,
                                clearable=False
                              ),
                          ], className='six columns'),

],className='row'),



    html.Div([
        html.Div([
            dcc.Graph(id='linechart'),
            ], className='six columns'),

        html.Div([
            dcc.Graph(id='piechart'),
            ], className='six columns'),
    ],className='row'),

])


#------------------------------------------------------------------

@app.callback(
    [Output('linechart', 'figure'),
     Output('piechart', 'figure')
     ],
     [Input('datatable_id', 'selected_rows'),
      #Input('piedropdpwn', 'value'),
      #Input('piedropdpwn1', 'value'),
      Input('linedropdown', 'value')
      ])


#def update_data(chosen_rows,piedropval,linedropval):
def update_data(chosen_rows,linedropval):
    global pie_chart, line_chart
    if len(chosen_rows)==0:
        #df_filterd = dff[dff["CHEF D'EQUIPE"].isin(["TCHALLA Kodjo","ATABA Ahoumodom Wilfred","ZOGBEDJI Uwulowudu","ABOUDOU Julien Komivi Sodjinè","OLANLO Tini Kodjo"])]
        df_filterd = dff[dff["CHEF D'EQUIPE"].isin([""])]
    else:
        #print(chosen_rows)
        df_filterd = dff[dff.index.isin(chosen_rows)]




    list_chosen_countries = df_filterd["CHEF D'EQUIPE"].tolist()
    df_line = df[df["CHEF D'EQUIPE"].isin(list_chosen_countries)]
    #print(df_line[:])
    line_chart = px.bar(
            data_frame=df_line,
            x="CANTON",
            y=linedropval,
            color="CANTON",
            labels={"CANTON": "CANTON"},
             )
    #line_chart.update_layout(uirevision='foo')

    #print(linedropval)
    #dff0 = df[df["CHEF D'EQUIPE"] == linedropval]
    dff0 = df_line
    fig = px.histogram(
        data_frame=dff0,
        x="CANTON",
        y="POPULATION",
        title="Population estimée",
    )

    return (fig,line_chart)


if __name__== "__main__":
    app.run_server(debug=True)

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




app.layout=html.Div([
    html.H1("Population estimée par Chef d'equipe et par Quartier / Canton"),


    #dcc.Graph(
   # id = 'pie',
   # figure = fig_bar
 # ),

    dcc.Dropdown(id='genre-choice',
                 options=[{'label':x, 'value':x}
                 for x in sorted(df["CHEF D'EQUIPE"].unique())],
                 value='ABOUDOU Julien Komivi Sodjinè'#Choix par défaut
                 ),
    html.H1("Canton"),
    dcc.Dropdown(id='canton',
                 options=[{'label':x, 'value':x}
                 for x in sorted(df["CANTON"].unique())],
                 value=''#Choix par défaut
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
    fig = px.histogram(data_frame=dff, x="CANTON",y="POPULATION",title="Population estimée")
    return fig

 if __name__== '__main__':
    app.run_server(debug=True)   

"""

