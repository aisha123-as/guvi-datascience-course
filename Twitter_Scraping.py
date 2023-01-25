!pip install snscrape
!pip install langcodes[data]
!pip install streamlit -q
!pip install pyngrok



from langcodes import * #for finding the language name from language codes
import pandas as pd #for creating the dataframe
import datetime #for finding the current timestamp
import pytz
import snscrape.modules.twitter as sntwitter #scrapping the twitter data


%%writefile function_file2.py
#!pip install snscrape
#!pip install langcodes[data]
#!pip install streamlit -q
#!pip install pyngrok


from langcodes import * 
import pandas as pd 
import datetime 
from datetime import timedelta
import snscrape.modules.twitter as sntwitter
import json

def scrap_datas(tag, from_date, to_date, lim):
  query = f"{tag} since:{from_date} until:{to_date}"
  limit = lim
  d_tweets = []
  scraper = sntwitter.TwitterSearchScraper(query)
  for tweet in scraper.get_items():
    if len(d_tweets) == lim:
      break
    else:
      d_tweets.append([tweet.id,tweet.url,tweet.date,tweet.user.username,tweet.content,tweet.replyCount,tweet.retweetCount,tweet.lang,tweet.source, tweet.likeCount])

  language_dict = {"Unknown language [qst]" : "Tweets with short text",
                   "Unknown language [qme]" : "Tweets with media link",
                   "Unknown language [qam]" : "Tewwts with mentions only", 
                   "Unknown language [qct]" : "Tweets with cashtags", 
                   "Unknown language [qht]" : "Tweets with hashtags",
                   "Unknown language" : "Undefined language"}

  for i in d_tweets:
    i[7] = Language.make(language=i[7]).display_name()

  for i in d_tweets:
    if i[7] in language_dict.keys():
      i[7] = language_dict[i[7]]
    else:
      i[7] = i[7]

  da = pd.DataFrame(d_tweets, columns = ["Id", "URL", "Date posted", "User Name", "Content", "Reply count", "Retweet count", "Language", "Source" , "Like count"])
  da["Source"] = da["Source"].apply(lambda x:x.split("=")[1].strip("rel"))
  da["Id"] = da["Id"].astype("str")
  return da

def update_data(tag, df_name):
  df_name["Date posted"] = df_name["Date posted"].apply(lambda x:(str(x)).split("+")[0])
  #Creating document of the fetched data
  data_list = []
  for i in range(df_name.shape[0]):
    x = pd.DataFrame.to_json(df_name.iloc[i, :])
    data_list.append(json.loads(x))

  #connecting to the server
  import pymongo
  client = pymongo.MongoClient("mongodb+srv://<UserName>:<Password>@cluster0.juglogj.mongodb.net/?retryWrites=true&w=majority")
  db = client.Twitter_data
  records = db.Twitter
  #inserting document into the database
  x = datetime.datetime.now()+timedelta(minutes = 330)
  cur_tsr = str(x).split(".")[0]
  htag = tag+"_"+cur_tsr
  daata = {htag : data_list}
  info = records.insert_one(daata)
  if info != 0:
    return "Inserted succcessfully"
  elif info == 0:
    return "Something went wrong please try again"
  
  
  
  
  GUI APP CREATION
  !pip install pyngrok==4.1.1
  
  
  !ngrok authtoken 2Kjk1sNkgtHmhrvADxwoX7sWOtY_87unGjkb4XkX7h8bLv2fs
  
  
  !wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
!unzip -qq ngrok-stable-linux-amd64.zip



%%writefile streamlit_app.py
import json
from function_file2 import  scrap_datas, update_data
import streamlit as st


st.markdown("TWEET SCRAPER", unsafe_allow_html=True)
hashtag = st.text_input('Enter your hashtag for search', '#')
f_date = st.date_input('Enter your Start Date')
from_date = str(f_date).replace("/", "-")
t_date = st.date_input('Enter your End Date')
to_date = str(t_date).replace("/", "-")
limit = st.number_input('Set Limit', 10)
if st.button("Display Data"):
  df = scrap_datas(hashtag, from_date, to_date, limit)
  st.table(df)
if st.button("Download Data"):
  df = scrap_datas(hashtag, from_date, to_date, limit)
  df_c = df.copy()
  df_c["Id"] = df_c["Id"].astype("str")
  df_csv = df_c.to_csv()
  st.download_button("Download as CSV",data = df_csv,file_name = f"{hashtag}.csv",mime='text/csv')
  st.balloons()
  df_json = df.to_json()
  st.download_button("Download as JSON", data = df_json, file_name = f"{hashtag}.json", mime="application/json")
  st.balloons()

if st.button("Upload data to the database"):
  df = scrap_datas(hashtag, from_date, to_date, limit)
  message = update_data(hashtag, df)
  st.write(message)
  st.balloons()
  
 #After running the streamlit app file run the below cell for creating the external link

 #For altering the file or re executing the streamlit app file this cell should be run for 2 times .Ignore the first result and use the link created by the second execution
  
  
  
  get_ipython().system_raw('./ngrok http 8501 &')
! curl -s http://localhost:4040/api/tunnels | python3 -c \
    "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
    
    
    
  #This cell is to be executed after the external link generation . After execution this cell will generate 2 local links. Dont use the local links. Use the above link after executing this cell
 
    !streamlit run /content/streamlit_app.py
  
  #After clicking the link from the 2nd last cell, you will land on a page where you can find a redirectiong button Visit site click that button to enter into the GUI italicized text
