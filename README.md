

# NYTimes Article Word Visualization Generator


## Overview

Utilizing the NYTimes API, this app creates word visualizations based on articles of a 
user's selected topic.
## About

- Pulls top articles from NYTimes and generates graphics based on most 
    frequently appearing words from said articles.
    - Visualizations come in the forms of a word frequency distribution line graph
        and a wordcloud, which is an image composed of words, in which 
        the size of each word indicates its frequency.
- Wordclouds can be generated based on top stories from a given topic, or from the most 
    emailed, seen, or shared articles.
- Amount of time to consider articles from is customizable as well, from the choices of
    1, 7, and 30 days.

- ```Streamlit run main.py``` command must be issued in terminal to run application properly

## To do
- Reorganize code into separate files and classes.
  - Add proper encapsulation between said newly-created files.
- Create a more robust front-end as to improve user experience.
