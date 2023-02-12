!git clone https://github.com/PhonePe/pulse.git
  
  #Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="/content/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

column={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}
for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)    
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)        
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              column['Transacion_type'].append(Name)
              column['Transacion_count'].append(count)
              column['Transacion_amount'].append(amount)
              column['State'].append(i)
              column['Year'].append(j)
              column['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
pd.DataFrame(column)



# insert the dataframe into a sqlite database

import sqlite3
conn = sqlite3.connect('pulse.db')
c = conn.cursor()


#create a table in the database
c.execute('''CREATE TABLE IF NOT EXISTS transaction_data(
            State TEXT,
            Year TEXT,
            Quater TEXT,
            Transacion_type TEXT,
            Transacion_count TEXT,
            Transacion_amount TEXT
            )''')

#insert the All data into the table
c.executemany('INSERT INTO transaction_data VALUES(?,?,?,?,?,?)', zip(column['State'], column['Year'], column['Quater'], column['Transacion_type'], column['Transacion_count'], column['Transacion_amount']))


#fetch the data from the table where the state is Maharashtra and year is 2018 and quater is 1 and transaction type is Recharge and bill payments

d=c.execute("SELECT * FROM transaction_data WHERE State='maharashtra' AND Year='2018' AND Quater='1' AND Transacion_type='Recharge & bill payments' AND Transacion_amount>0")
d=c.fetchall()
for row in d:
  print(row)

  #data/map/user
path_mapuser="/content/pulse/data/map/user/hover/country/india/state/"
map_userstate_list=os.listdir(path_mapuser)
map_user={'State':[], 'Year':[],'quarter':[],'district':[], 'registeredUsers':[], 'appOpens':[]}

for i in map_userstate_list:
    p_i=path_mapuser+i+"/"
    map_yr=os.listdir(p_i)    
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)        
        for k in map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            d=D['data']['hoverData']
            for dis, val in d.items():
              map_user["district"].append(dis)
              map_user["registeredUsers"].append(val["registeredUsers"])
              map_user["appOpens"].append(val["appOpens"])
              map_user["State"].append(i)
              map_user["Year"].append(j)
              map_user["quarter"].append(int(k.strip('.json')))
dfmap=pd.DataFrame(map_user)
dfmap['State']=dfmap['State'].str.replace('&',' ')    
dfmap['State']=dfmap['State'].str.replace('-',' ')  
dfmap['State']=dfmap['State'].str.title() 
dfmap


dfd=dfmap.groupby("State").sum().iloc[ : ,1: ]
dfd

%%writefile app.py
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import os
from PIL import Image
from dataret import dfaggusr,dfaggstate,dfmapstate,dfmapuser,dftopstate,dftopusr,dfmapuserdeo

#cleaning the data
def cleanstate(df):
  df['State']=df['State'].str.replace('&',' ')    
  df['State']=df['State'].str.replace('-',' ')  
  df['State']=df['State'].str.title() 
  return df

#importing dataframes 
df1=cleanstate(dfaggusr)
df2=cleanstate(dfaggstate)
df3=cleanstate(dfmapstate)
df4=cleanstate(dfmapuser)
df5=cleanstate(dftopstate)
df6=cleanstate(dftopusr)
dfgeo=cleanstate(dfmapuserdeo)

if 'dfagguser' not in st.session_state:
    st.session_state['dfagguser'] = df1
if 'dfagstate' not in st.session_state:
    st.session_state['dfagstate'] = df2	
if 'dfmapstat' not in st.session_state:
    st.session_state['dfmapstat'] = df3
if 'dfmapusr' not in st.session_state:
    st.session_state['dfmapusr'] = df4
if 'dftopstat' not in st.session_state:
    st.session_state['dftopstat'] = df5
if 'dftopuser' not in st.session_state:
    st.session_state['dftopuser'] = df6	
		
#st.session_state

df7=dfgeo.groupby("State").sum().iloc[ : ,1: ]

figgeo = px.choropleth(
    df7,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations=df7.index,
    color= "registeredUsers",
    color_continuous_scale='Reds',
    hover_name = df7.index,
    hover_data = df7.columns,
)

figgeo.update_geos(fitbounds="locations", visible=False)

figgeo.update_layout(
    title=dict(
            text="No of RegisteredUsers in each State ",
            xanchor='left',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b':10}),
            margin={'r':0,'t':30,'l':0,'b':0},
            height=550,
            width=1000
      )


#funtion to update year
def update_year(value):
	df_p1=df1
	df_p2=df2
	df_p3=df3
	df_p4=df4
	df_p5=df5
	df_p6=df6
	if value == "All":
		st.session_state['dfagguser'] = df_p1
		st.session_state['dfagstate'] = df_p2	
		st.session_state['dfmapstat'] = df_p3
		st.session_state['dfmapusr'] = df_p4
		st.session_state['dftopstat'] = df_p5
		st.session_state['dftopuser'] = df_p6
	else:
		st.session_state['dfagguser']=df_p1[df_p1["Year"]==value]
		st.session_state['dfagstate']=df_p2[df_p2["year"]==value]
		st.session_state['dfmapstat'] =df_p3[df_p3["Year"]==value]
		st.session_state['dfmapusr'] =df_p4[df_p4["Year"]==value]
		st.session_state['dftopstat'] = df_p5[df_p5["Year"]==value]
		st.session_state['dftopuser'] = df_p6[df_p6["Year"]==value]

#funtion to update state in figures
def update_dashboard(value):
	dfp1=st.session_state['dfagguser']
	dfp2=st.session_state['dfagstate']
	dfp3=st.session_state['dfmapstat']
	dfp4=st.session_state['dfmapusr']
	dfp5=st.session_state['dftopstat']
	dfp6=st.session_state['dftopuser']

	dfstate=dfp1[dfp1["State"]==value]
	dfstate2=dfp2[dfp2["State"]==value]
	dfmap1=dfp3[dfp3['State']==value]
	dfmap2=dfp4[dfp4['State']==value]
	dftop1=dfp5[dfp5['State']==value]
	dftop2=dfp6[dfp6['State']==value]
	#d1=dftop1.groupby("District")['Transacion_count'].mean()
	fig=px.bar(dfstate,x="brand",y="count",title="Brand vs User count")
	fig2=px.area(dfstate2,x="Transacion_type",y="Transacion_amount",title="Transacion type vs Transacion amount")
	fig3=px.bar(dfmap1,x='District',y='Transacion_count',title="District vs Transacion_count")
	fig4=px.area(dfmap2,x="District",y="registeredUsers",title="District vs RegisteredUsers")
	fig5=px.pie(dftop1,names='District',values="Transacion_count",title="Transacion_count in each District")
	fig6=px.pie(dftop2,names='District',values="registeredUsers",title="RegisteredUsers in each District")

	st.plotly_chart(fig)
	st.plotly_chart(fig2)
	st.plotly_chart(fig3)
	st.plotly_chart(fig4)
	st.plotly_chart(fig5)
	st.plotly_chart(fig6)
	
#main function
def main():

	image = Image.open('/content/phonepe-logo-icon.png')
	col1, col2, col3 = st.columns(3)
	with col1:
		st.write('     ')
	with col2:
		st.image(image,width=200)
	with col3:
		st.write(' ')
	st.markdown("<h1 style='text-align: center; color: blue;'>PhonePe</h1>", unsafe_allow_html=True)
	
	
	st.plotly_chart(figgeo)
	#st.dataframe(dfgeo)
	#st.dataframe(df7)


	options2 = df1["Year"].unique()
	options2=np.append(["All"],options2)
	selected_year = st.selectbox('Select a Year:', options2)
	update_year(selected_year)

	options = df1["State"].unique()
	selected_option = st.selectbox('Select a State:', options)
	update_dashboard(selected_option)
	#st.dataframe(df2)

if __name__ == '__main__':
	main()
  
  !pip install pyngrok==4.1.1
  
  !ngrok authtoken 2KmLhi9o9rhTfgnwUY03qPNSw2p_3nUjkV6j5CBE73Xz2rWy3
  
  !streamlit run --server.port 80 app.py &>/dev/null&
from pyngrok import ngrok 
public_url = ngrok.connect(port='80')
public_url
