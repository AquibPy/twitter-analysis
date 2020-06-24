import streamlit as st
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import webbrowser


consumerKey = 'E39cshUel1sCtP6rb0E4hsaeZ'
consumerSecret = 'rmuQx9317MT8NOeXbHHKGxugoDjIR1w2TE9sv0UkB72I6sYqMx'

accessToken = '2924217373-rv18gyiUyKgfl233kzsWopJlaiH74njT9BscU5i'

accessTokenSecret ='P16R5y5q686jjo1Jq0k1FSVMmFcY1axTIVj4lt4udSvO2'


# Create an Authentication Object
authenticate = tweepy.OAuthHandler(consumerKey,consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken,accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate,wait_on_rate_limit=True)



def main_tweet():
    st.title("Tweet Analyzer 🐦")
    from PIL import Image
    image = Image.open('logo.jpeg')
    st.sidebar.image(image,use_column_width=True)
    activities = ['Tweet Analyzer','Generate Tweet Data','About Us']
    choice = st.sidebar.selectbox("Select Your Activity",activities)


    if choice == "Tweet Analyzer":
        st.subheader('Analyze the tweets of your favourite Personalities')
        st.subheader('This Tool will performs the following tasks:')
        st.write('1. Fetchs the 5 most recents tweets from the given twitter handle')
        st.write('2. Generates a Word Cloud')
        st.write('3. Performs Sentiments Analysis and Display it in a form of Bar Graph')


        raw_text = st.text_area('Enter the exact twitter handle of the Personality (without @)')

        analysis = st.selectbox("Select the Activities",["Show the Recent Tweets","Generate the WordCloud","Visualize the Sentiment Analysis"])

        if st.button("Analyze"):
            if analysis == "Show the Recent Tweets":
                st.success("Fetching last 5 Tweets")
                def Show_Recent_Tweets(raw_text):
                    posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")
                    def get_tweets():
                        l=[]
                        i=1
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i= i+1
                        return l
                    recent_tweets=get_tweets()
                    return recent_tweets
                recent_tweets= Show_Recent_Tweets(raw_text)
                st.write(recent_tweets)
            elif analysis == "Generate the WordCloud":
                st.success("Generating Word Cloud")
                def gen_wordcloud():
                    posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")
					# Create a dataframe with a column called Tweets
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
					# word cloud visualization
                    allWords = ' '.join([twts for twts in df['Tweets']])
                    wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
                    plt.imshow(wordCloud, interpolation="bilinear")
                    plt.axis('off')
                    plt.savefig('WC.jpg')
                    img= Image.open("WC.jpg")
                    return img
                img=gen_wordcloud()
                st.image(img)
            else:
                def Plot_Analysis():
                    st.success("Generating Visualisation for Sentiment Analysis")
                    posts = api.user_timeline(screen_name=raw_text, count = 100, lang ="en", tweet_mode="extended")
                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
					# Create a function to clean the tweets
                    def cleanTxt(text):
                        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
                        text = re.sub('#', '', text) # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text) # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
                        return text
					# Clean the tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)
                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity
					# Create a function to get the polarity
                    def getPolarity(text):
                        return  TextBlob(text).sentiment.polarity


					# Create two new columns 'Subjectivity' & 'Polarity'
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)
                    def getAnalysis(score):
                        if score < 0:
                            return 'Negative'
                        elif score == 0:
                            return 'Neutral'
                        else:
                            return 'Positive'  
                    df['Analysis'] = df['Polarity'].apply(getAnalysis)
                    return df

                df= Plot_Analysis()
                st.write(sns.countplot(x=df["Analysis"],data=df))
                st.pyplot(use_container_width=True)
    elif choice == "Generate Tweet Data":
        st.subheader("This tool fetches the last 100 tweets from the twitter handel & Performs the following tasks")
        st.write("1. Converts it into a DataFrame")
        st.write("2. Cleans the text")
        st.write("3. Analyzes Subjectivity of tweets and adds an additional column for it")
        st.write("4. Analyzes Polarity of tweets and adds an additional column for it")
        st.write("5. Analyzes Sentiments of tweets and adds an additional column for it")

        user_name = st.text_area("Enter the exact twitter handle of the Personality (without @)*")
        def get_data(user_name):
            post = api.user_timeline(screen_name=user_name, count = 100, lang ="en", tweet_mode="extended")
            df = pd.DataFrame([tweet.full_text for tweet in post], columns=['Tweets'])
            def cleanTxt(text):
                text = re.sub('@[A-Za-z0–9]+', '', text)
                text = re.sub('#', '', text)
                text = re.sub('RT[\s]+', '', text) # Removing RT
                text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
                return text
            df["Tweets"] = df["Tweets"].apply(cleanTxt)

            def getSubjectivity(text):
                return TextBlob(text).sentiment.subjectivity

            # Create a function to get the polarity
            def getPolarity(text):
                return TextBlob(text).sentiment.polarity

            # Create two new columns 'Subjectivity' & 'Polarity'
            df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
            df['Polarity'] = df['Tweets'].apply(getPolarity)

            def getAnalysis(score):
                if score < 0:
                    return 'Negative'
                elif score == 0:
                    return 'Neutral'
                else:
                    return 'Positive'
            
            df['Analysis'] = df['Polarity'].apply(getAnalysis)
            return df
        if st.button('Show Data'):
            st.success('Fetching Last 100 Tweets')
            df = get_data(user_name)
            st.write(df)
    else:
        st.header("SCRIPTHON")

        st.write("""SCRIPTHON is a coding community founded by students of MCA, Aligarh Muslim University.
        We are a group of talented and enthusiastic students who have experienced in a certain area like ML/AI, Web Development, Android Development, Ethical Hacking & many more.
        All are willing to help each other to grow simultaneously and share their knowledge because Richard Feynman said "THE ULTIMATE TEST OF YOUR KNOWLEDGE IS YOUR CAPACITY TO CONVEY IT TO ANOTHER". 
        We've made many interesting projects which you can see on our website and currently we've community of five members, if you want to join our community then let us know.""")

        st.subheader('Our Team Members')
        st.subheader("1. Mohd Aquib")
        st.subheader("2. Nikhil Upadhyay")
        st.subheader("3. Mahiya Khan")
        st.subheader("4. Mohd Maaz Azhar")
        st.subheader("5. Dilanshi Varshney")



        st.subheader("Made with ❤️ by Mohd Aquib.")

        github = "https://github.com/AquibPy"
        linkedIn = "https://www.linkedin.com/in/aquib-mohd-182b2a71/"

        if st.button('Github'):
            webbrowser.open_new_tab(github)
        if st.button('LinkedIn'):
            webbrowser.open_new_tab(linkedIn)


if __name__ == "__main__":
	main_tweet()
