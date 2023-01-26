!pip install easy-exchange-rates
!pip install jupyter_dash
!pip install geopandas
!pip install dash_bootstrap_components
     
  
  
import pandas as pd
from easy_exchange_rates import API
from datetime import date
import dash
from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import dash_table as dt


#Country code 
Country_code = pd.read_csv('https://raw.githubusercontent.com/Aravindan79/data/main/Country-Code.csv')

#Zomato DataSet
Zomato = pd.read_csv('https://raw.githubusercontent.com/Aravindan79/data/main/Zomato.csv')

# INR exchange rate for other Currencies
Curr_code = list(Country_code['Currency_code'])
Exchange_Rate = []

api = API()
for i in range (0, len(Curr_code)):
  time_series = api.get_exchange_rates(
  base_currency=Curr_code[i], 
  start_date=str(date.today()), 
  end_date=str(date.today()), 
  targets=['INR']
  )
  Exchange_Rate.append((time_series[str(date.today())])['INR'])

Country_code['Exchange_rate'] = Exchange_Rate

#Merging two Zomato Data Set

Zomato = pd.merge(Zomato,Country_code)

#Currency Converstion to INR 

ex_rate = list(Zomato['Exchange_rate'])
rate_conversion = list(Zomato['Average_Cost_for_two'])

Price_in_INR = []

for i in range (0,len(rate_conversion)):
  Price_in_INR.append(ex_rate[i]*rate_conversion[i])

Zomato['Indian_Rupee']=Price_in_INR

#Creating new DF for Country ploting
#calculation of average money spent by each country,dine in, delivery,costlier cusine, most popular cusine...

s = list(dict(Zomato.groupby("Country")['Indian_Rupee'].mean()))
s1 = list(Zomato.groupby("Country")['Indian_Rupee'].mean())
df4 = pd.DataFrame(s,columns=['Country'])
df4['Average_Money_Spent']=s1
Country_list = list(df4['Country'])
length = len(Country_list)
dine = []
delivery = []
Costlier_Cusine = []
Popular_Cusine = []
max_spent_city = []
min_spent_city = []
min_spent_amount = []
a1 = ''

for i in range(0,length):
#countrywise dataFrame
  specific_country=(Zomato[ Zomato['Country']==Country_list[i]])
# to get dine-in and delivery count of each country
  dine.append(len(list(specific_country[specific_country['Has_Table_booking']=='Yes'].index.values)))
  delivery.append(len(list(specific_country[specific_country['Has_Online_delivery']=='Yes'].index.values)))
#most Costlier cusine
  max_spent = specific_country.Indian_Rupee.max()
  index = list(specific_country[specific_country['Indian_Rupee']==max_spent].index.values)
  Costlier_Cusine.append(specific_country.loc[int(index[0]),'Cuisines'])
#Most popular Cusine
  popular_vote = specific_country.Aggregate_rating.max()
  li = {}
  index = (specific_country[specific_country['Aggregate_rating']==popular_vote].index.values)
  for i in range(0,len(index)):
    b = (list(specific_country.loc[int(index[i]),['Votes']]))
    a = str(list(specific_country.loc[int(index[i]),['Cuisines']])).replace('[','').replace(']','').replace("'",'')
    li[a] = b[0]
  value = dict(li)
  Popular_Cusine.append(max(zip(value.values(), value.keys()))[1])
#Highest Spending City 
  city = specific_country.City.unique()
  city_wise_cost = (dict(specific_country.groupby("City")['Indian_Rupee'].sum()))
  max_spent_city.append(max(zip(city_wise_cost.values(), city_wise_cost.keys()))[1])
#Min Spending City
  min_spent_city.append(min(zip(city_wise_cost.values(), city_wise_cost.keys()))[1])
#Votes and Aggregate rating
vote = list(Zomato.groupby("Country")['Votes'].sum())
avg_rating = list(Zomato.groupby("Country")['Aggregate_rating'].mean())
# Appending the data to Df4

df4['Dine-In'] = dine
df4['Online_Delivery'] = delivery
df4['Popular_Cusine'] = Popular_Cusine
df4['Costlier_Cusine'] = Costlier_Cusine
df4['Max_spent_city'] = max_spent_city
df4['Min_spent_city'] = min_spent_city
df4['Votes'] = vote
df4['Aggregate_rating'] = avg_rating

df4 = pd.merge(df4,Country_code)

#DASH BOARD -CODE


app = JupyterDash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
#Dropdown Options 
OPTIONS = ['Average_Money_Spent','Aggregate_rating','Votes','Dine-In','Online_Delivery']
packages = ['Choropleth', 'Scatter']

Cities_on_Country = dict(Zomato.groupby('Country')['City'].unique())
names = list(Cities_on_Country.keys())
nestedOptions = Cities_on_Country[names[0]]
# Sidebar stlying
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#a1becf",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Zomato Data Analysis", className="display-4"),
        html.Hr(),
        html.P(
            "Filter based on Country and Cities", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Country Wise Analysis", href="/", active="exact"),
                dbc.NavLink("City Wise Analysis", href="/page-1", active="exact"),
                dbc.NavLink("Worldwide Analysis", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
            
        ),
    ],
    style=SIDEBAR_STYLE,
)
#https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
#above link is to refer 
Drop_down = dcc.Dropdown(
        list(Zomato['Country'].unique()),
        'India',
        id="dropdown"
    )
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],suppress_callback_exceptions=True
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Country wise Analysis',
                        style={'textAlign':'center',
                               'fontWeight': 'bold',
                               'color': 'black',
                               }),
                html.Br(),
                html.Label('Country name: ',style = {'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",}),
                html.Br(),
                dcc.Dropdown(
                list(df4['Country'].unique()),
                'India',
                id="dropdown",
                style={"background-color": "#e8ebed",
                       'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",
                       'textAlign':'center'}
                ),
                html.Br(),
                
                dt.DataTable(id='data-table', columns=[
                            {'name': 'Popular_Cusine', 'id': 'Popular_Cusine'},
                            {'name': 'Costlier_Cusine', 'id': 'Costlier_Cusine'},
                            {'name': 'Max_spent_city', 'id': 'Max_spent_city'},
                            {'name': 'Min_spent_city', 'id': 'Min_spent_city'},
                            ],
                style_header={
                            'backgroundColor': '#8c9dc2',
                            'color': 'black',
                            'font_family':"Merriweather Sans",
                            'textAlign':'center'
                            },
                style_data={
                            'backgroundColor': '#8c9dc2',
                            'color': 'black',
                            'font_family':"Merriweather Sans",
                            'textAlign':'center'
                            }),
                html.Br(),
                dcc.Graph(id="graph")
    
                ]
    elif pathname == "/page-1":
        return [
        html.H1('Citywise Analysis',
                        style={'textAlign':'center'}),
        html.Label('Country name: ',style = {'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",}),
        html.Div([
        dcc.Dropdown(
            id='name-dropdown',
            options=[{'label':name, 'value':name} for name in names],
            value = list(Cities_on_Country.keys())[0]
            ),
            ],style={'width': '100%', 
                     "background-color": "#94abd4",
                       'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",
                       'textAlign':'center'}),
        html.Label('City name: ',style = {'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",}),
        html.Br(),
        html.Div([
        dcc.Dropdown(
            id='opt-dropdown',
            value = 'Penola',
            
            ),
            ],style={'width': '100%', 
            "background-color": "#94abd4",
                       'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",
                       'textAlign':'center'}
        ),
        html.Hr(),
        html.Br(),
        html.P(id='my-output1',
        style={
           'font_color':'#1c1b1b',
           'fontWeight': 'bold',
           'font_family':"Merriweather Sans",
           'textAlign':'center'
       }),
        html.P(id='my-output2',
        style={
           'font_color':'#1c1b1b',
           'fontWeight': 'bold',
           'font_family':"Merriweather Sans",
           'textAlign':'center'
       }),
        html.P(id='my-output3',
        style={
           'font_color':'#1c1b1b',
           'fontWeight': 'bold',
           'font_family':"Merriweather Sans",
           'textAlign':'center'
       }),
        html.P(id='my-output4',
        style={
           'font_color':'#1c1b1b',
           'fontWeight': 'bold',
           'font_family':"Merriweather Sans",
           'textAlign':'center'
       }),
        html.Br(),
        dcc.Graph(id="my-graph3")
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Worldwide Analysis',
                        style={'textAlign':'center'}),
                html.Label('Values: ',style = {'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",}),
                html.Br(),
                dcc.Dropdown(id='var_choice'  , value='Average_Money_Spent'  , options=[{'label': i, 'value': i} for i in  OPTIONS],
                             style={"background-color": "#e8ebed",
                                    'font_color':'black',
                                    'fontWeight': 'bold',
                                   
                                    # 'font_family':"Merriweather Sans",
                                    'textAlign':'left'}),
                html.Br(),
                html.Label('Map Types: ',style = {'font_color':'black',
                       'fontWeight': 'bold',
                      'font_family':"Merriweather Sans",}),
                html.Br(),
                dcc.Dropdown(id='pkg_choice'  , value='Choropleth'       , options=[{'label': i, 'value': i} for i in  packages],
                             style={"background-color": "#e8ebed",
                                    'font_color':'black',
                                    'fontWeight': 'bold',
                                    # 'font_family':"Merriweather Sans",
                                    'textAlign':'left'}),
   
                dcc.Graph(id='my-graph'),
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
@app.callback(
    [Output('data-table', 'data'),
    Output("graph", "figure")],   
    [Input("dropdown", "value")],suppress_callback_exceptions=True)

def update_bar_chart(value):
#getting the popular & costlier cusine,min and max spent city
    columns = []
    columns_index = (df4[df4['Country']==value].index.values)
    temp = ['Popular_Cusine','Costlier_Cusine','Max_spent_city','Min_spent_city']
    for i in range(0,len(temp)):
      columns.append(df4.iloc[columns_index[0]][temp[i]])
    dummy = pd.DataFrame([columns], columns = temp)
    data=dummy.to_dict('records')
#graph 
    fig = make_subplots(rows=1, cols=2,subplot_titles=('Average Money Spent',  'Dine-In VS Online Delivery'))

    avg_spent = int(df4.iloc[columns_index[0]]['Average_Money_Spent'])
    column_1 = []
    temp1 = ['Dine-In','Online_Delivery']
    for i in range(0,len(temp1)):
      column_1.append(df4.iloc[columns_index[0]][temp1[i]])

    fig.add_scatter(x =[f'{value}'],y=[avg_spent],
            marker=dict(color="black"),
            name="Indian Rupee ₹", row=1, col=1)

    fig.add_bar(x =['Dine-in','Online Delivery'],y= column_1,
            marker=dict(color="black"),
            name="Count", row=1, col=2)

    fig.update_layout(height=500, 
                      width= 1200,
                      showlegend=False,  plot_bgcolor='#faf5dc',
                      paper_bgcolor="#e8e8e8",
                      font_color='black',
                      font_family="Merriweather Sans")

    fig.update_traces(overwrite=True, marker={"opacity": 0.6})
    
    fig.data[0].marker.line.width = 4
    fig.data[0].marker.line.color = "black"

    fig.data[1].marker.line.width = 4
    fig.data[1].marker.line.color = "black"
    return data,fig

@app.callback(     Output('my-graph', 'figure'    ) ,
                   [Input('var_choice' , 'value'     ),
                   Input('pkg_choice' , 'value'     ),
                   ],suppress_callback_exceptions=True )
def update_figure(var_choice,pkg):

    if pkg=='Choropleth':
      df = df4
      fig = go.Figure(data=go.Choropleth(
      locations = df4['iso_alpha'],
      z = df4[var_choice],
      text = df4['Country'],
      colorscale = 'Inferno',
      autocolorscale=False,
      reversescale=True,
      marker_line_color='#1a1c1c',
      marker_line_width=1,
      colorbar_tickprefix = '$',
      colorbar_title = var_choice,
))

      fig.update_layout(
      title_text=var_choice,
      geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
 
)     
      fig.update_layout(
      autosize=False,
      width=1250,
      height = 600
      )

      return fig
    else:
      df = df4
    map = px.scatter_geo(df, locations = 'iso_alpha',
                     size= var_choice,
                     color="Country",
                     hover_name="Country"# size of markers, "pop" is one of the columns of gapminder
                     )
    map.update_layout(
    autosize=False,
    width=1250,
    height = 600
    )
    return map

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')],suppress_callback_exceptions=True
)
def update_date_dropdown(name):
     
    return [{'label': i, 'value': i} for i in Cities_on_Country[name]]

@app.callback(
    
    dash.dependencies.Output(component_id='my-output1', component_property='children'),
    dash.dependencies.Output(component_id='my-output2', component_property='children'),
    dash.dependencies.Output(component_id='my-output3', component_property='children'),
    dash.dependencies.Output(component_id='my-output4', component_property='children'),
    dash.dependencies.Output("my-graph3", "figure"),

    dash.dependencies.Input('opt-dropdown', 'value'),suppress_callback_exceptions=True)
def set_display_children(value):
    #getting the popular & costlier cusine,Highest and Lowest rating Res
    columns = [popularCusine(value),costlierCuisine(value),RatingCount_H(value),RatingCount_L(value)]

    a= f'Popular Cusine : {columns[0]}'
    b= f'Costlier Cusine : {columns[1]}'
    c= f'Highest Rating Restaurant : {columns[2]}'
    d= f'Lowest Rating Restaurant : {columns[3]}'
# graph 
    val,val1 = dine_Delivery(value)
    fig = make_subplots(rows=1, cols=2,subplot_titles=('YES - Dine in Vs Online Delivery',  'NO - Dine in Vs Online Delivery'))   
    fig.add_bar(x =['Dine-in','Online Delivery'],y=val,
            marker=dict(color="black"),
            name="Indian Rupee ₹", row=1, col=1)
    fig.add_bar(x =['Dine-in','Online Delivery'],y=val1,
            marker=dict(color="black"),
            name="Count", row=1, col=2)
    fig.update_layout(height=500, 
                      width= 1200,
                      showlegend=False,  plot_bgcolor='#faf5dc',
                      paper_bgcolor="#e8e8e8",
                      font_color='black',
                      font_family="Merriweather Sans")
    fig.update_traces(overwrite=True, marker={"opacity": 0.6})
    fig.data[0].marker.line.width = 4
    fig.data[0].marker.line.color = "black"
    fig.data[1].marker.line.width = 4
    fig.data[1].marker.line.color = "black"
    return a,b,c,d,fig

def popularCusine(a):
  l1 = list(Zomato['Country'].unique())
  specific_city=(Zomato[ Zomato['City']==a])
  Popular_Cusine = []
  popular_vote = specific_city.Aggregate_rating.max()
  li = {}
  index = (specific_city[specific_city['Aggregate_rating']==popular_vote].index.values)
  for i in range(0,len(index)):
    b = (list(specific_city.loc[int(index[i]),['Votes']]))
    a = str(list(specific_city.loc[int(index[i]),['Cuisines']])).replace('[','').replace(']','').replace("'",'')
    li[a] = b[0]
  value = dict(li)
  Popular_Cusine.append(max(zip(value.values(), value.keys()))[1])
  return Popular_Cusine[0]

def costlierCuisine(a):
  Costlier_Cusine = []
  l1 = list(Zomato['Country'].unique())
  specific_city=(Zomato[ Zomato['City']==a])
  max_spent = specific_city.Indian_Rupee.max()
  index = list(specific_city[specific_city['Indian_Rupee']==max_spent].index.values)
  Costlier_Cusine.append(specific_city.loc[int(index[0]),'Cuisines'])
  return Costlier_Cusine[0]

def RatingCount_H(a):
  l1 = list(Zomato['Country'].unique())
  specific_city=(Zomato[ Zomato['City']==a])
  Res_name = []
  popular_vote = specific_city.Aggregate_rating.max()
  li = {}
  index = (specific_city[specific_city['Aggregate_rating']==popular_vote].index.values)
  for i in range(0,len(index)):
    b = (list(specific_city.loc[int(index[i]),['Votes']]))
    a = str(list(specific_city.loc[int(index[i]),['Restaurant_Name']])).replace('[','').replace(']','').replace("'",'')
    li[a] = b[0]
  value = dict(li)
  Res_name.append(max(zip(value.values(), value.keys()))[1])
  return Res_name[0]

def RatingCount_L(a):
  l1 = list(Zomato['Country'].unique())
  specific_city=(Zomato[ Zomato['City']==a])
  Res_name = []
  popular_vote = specific_city.Aggregate_rating.min()
  li = {}
  index = (specific_city[specific_city['Aggregate_rating']==popular_vote].index.values)
  for i in range(0,len(index)):
    b = (list(specific_city.loc[int(index[i]),['Votes']]))
    a = str(list(specific_city.loc[int(index[i]),['Restaurant_Name']])).replace('[','').replace(']','').replace("'",'')
    li[a] = b[0]
  value = dict(li)
  Res_name.append(max(zip(value.values(), value.keys()))[1])
  return Res_name[0]

def dine_Delivery(a):
  count = []
  count1 = []
  l1 = list(Zomato['Country'].unique())
  specific_city=(Zomato[ Zomato['City']==a])
  count.append(len(list(specific_city[specific_city['Has_Table_booking']=='Yes'].index.values)))
  count.append(len(list(specific_city[specific_city['Has_Online_delivery']=='Yes'].index.values)))
  count1.append(len(list(specific_city[specific_city['Has_Table_booking']=='No'].index.values)))
  count1.append(len(list(specific_city[specific_city['Has_Online_delivery']=='No'].index.values)))
  return count,count1

if __name__=='__main__':
    app.run_server(debug=True)
