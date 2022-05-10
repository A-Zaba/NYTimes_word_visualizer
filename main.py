import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud

import main_functions

# Known bugs:
# NYTimes API returns an error message JSON if too many requests are sent in a short span of time, this will cause
# the frequency distribution and wordclouds to generate an error on the page.
# Can make a method to handle wordcloud generation, as there is currently redundant code in the top stories and most
# popular articles sections

api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dict["api_key"]

st.title("Article Word Frequency Visualizer")
st.header("Word Map Generator")
st.subheader("Part A - The Stories API")
st.write("This app uses the Top Stories API to display the most common words used in the top current articles "
         "based on a specified topic selected by the user. The data is displayed as a line chart and as a wordcloud "
         "image.")
st.subheader("1 - Topic Selection")
user_name = st.text_input("Please enter your name", "")
# Catch user input on what topic articles they want to generate the frequency distribution and wordcloud for
option = st.selectbox(
    "Select a topic of your interest",
    ("Arts", "Automobiles", "Books", "Business", "Fashion", "Food", "Health", "Home", "Insider", "Magazine",
     "Movies", "NYRegion", "Obituaries", "Opinion", "Politics", "RealEstate", "Science", "Sports", "SundayReview",
     "Technology", "Theater", "T-Magazine", "Travel", "Upshot", "US", "World"), index=0)
# Use NYTimes Top Stories API to create json response containing articles of user's selected topic
stories_url = f"https://api.nytimes.com/svc/topstories/v2/{option.lower()}.json?api-key={api_key}"
stories_response = requests.get(stories_url).json()
main_functions.save_to_file(stories_response, "JSON_Files/response.json")

st.write("Hi %s, you have selected the %s topic." % (user_name, option))

st.subheader("2 - Frequency Distribution")
# Initialize empty string to append abstracts to
story_abstracts = ""
# Create a list of words to omit from counting, such as articles "the"," "and", etc.
stopwords = stopwords.words("english")
clean_words = []
fDistribution = st.checkbox("Click here to generate frequency distribution")
if fDistribution:

    articles = main_functions.read_from_file("JSON_Files/response.json")
    for i in articles["results"]:
        story_abstracts = story_abstracts + i["abstract"]
    words = word_tokenize(story_abstracts)
    # Process all words generated from story abstracts, and if the current word is not in our
    # list of omitted words, add it to the list which the frequency distribution will be based on.
    for w in words:
        if w.isalpha() and w.lower() not in stopwords:
            clean_words.append(w.lower())
    fDist = FreqDist(clean_words)
    common_words = {"List": fDist.most_common(10)}
    x_axis = [x[0] for x in common_words["List"]]
    y_axis = [y[1] for y in common_words["List"]]
    chart_data = pd.DataFrame({"Words": x_axis, "Occurrences": y_axis})
    chart_data = chart_data.rename(columns={"Words": "times"}).set_index("times")
    st.line_chart(chart_data)

# Generate WordCloud based on user's selected article topic category
st.subheader("3 - Wordcloud")
wordCloud = st.checkbox("Click here to generate wordcloud")
if wordCloud:
    articles = main_functions.read_from_file("JSON_Files/response.json")
    for i in articles["results"]:
        story_abstracts = story_abstracts + i["abstract"]
    wordcloud = WordCloud().generate(story_abstracts)
    plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(plt)
    st.write("Wordcloud generated for %s topic." % option)

# Generate wordcloud based on the most shared, emailed, or viewed articles in the last X days.
st.subheader("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed, or viewed articles.")
articleType = st.selectbox("Select your preferred set of articles", ("Shared", "Emailed", "Viewed"))
timePeriod = st.selectbox("Select the period of time (last days)", ("1", "7", "30"))

popular_url = f"https://api.nytimes.com/svc/mostpopular/v2/{articleType.lower()}/{timePeriod.lower()}.json?api-key={api_key}"
popular_response = requests.get(popular_url).json()

pop_abstracts = ""
pop_clean_words = []
articles = main_functions.read_from_file("JSON_Files/response2.json")
for i in articles["results"]:
    pop_abstracts = pop_abstracts + i["abstract"]

pop_wordcloud = WordCloud().generate(pop_abstracts)
plt.figure(figsize=(12, 12))
plt.imshow(pop_wordcloud)
plt.axis("off")
st.pyplot(plt)
