# Build a streamlit app to display Github Repos

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import base64
import datetime
import time
import altair as alt
from PIL import Image

# Set page title
st.title('Github Repo Search')

# Set page icon
image = Image.open('github.jpg')
st.image(image, width=100)

# Set page subtitle
st.write("""
### Search for Github Repos
""")
st.write('---')

# Set sidebar
st.sidebar.header('Search Parameters')

# Create function to get user input
def get_user_input():
    query = st.sidebar.text_input('Query', 'openai')
    # stars = st.sidebar.slider('Stars', 0, 100000, 1000)
    # a list of languages
    languages = ['python', 'javascript', 'ruby', 'java', 'php', 'c++', 'c#', 'go', 'typescript', 'shell', 'swift', 'scala', 'kotlin', 'rust', 'r', 'dart', 'haskell', 'julia', 'elixir', 'clojure', 'groovy', 'lua', 'matlab', 'perl', 'powershell', 'racket', 'sas', 'sql', 'tcl', 'visual basic']
    # a dropdown select box for languages
    language = st.sidebar.selectbox('Languages', languages)

    return query, language

# Create function to get repo data
def get_repo_data(query, language):
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': '%s+language:%s' % (query, language)
    }
    r = requests.get(url, params=params)
    data = r.json()
    return data

# Create function to get repo info
def get_repo_info(data):
    repo_dict = {
        'name': [],
        'user': [],
        'stars': [],
        'forks': [],
        'date': [],
        'url': []
    }
    for i in range(len(data['items'])):
        repo_dict['name'].append(data['items'][i]['name'])
        repo_dict['user'].append(data['items'][i]['owner']['login'])
        repo_dict['stars'].append(data['items'][i]['stargazers_count'])
        repo_dict['forks'].append(data['items'][i]['forks_count'])
        repo_dict['date'].append(data['items'][i]['created_at'])
        repo_dict['url'].append(data['items'][i]['html_url'])
    repo_df = pd.DataFrame.from_dict(repo_dict)
    return repo_df

# Create function to plot repo info
def plot_repo_info(repo_df):
    c = alt.Chart(repo_df).mark_circle().encode(
        x='stars',
        y='forks',
        size='stars',
        color='user',
        tooltip=['name', 'user', 'stars', 'forks', 'date', 'url']
    ).interactive()
    return c

# Create function to display repo info
def display_repo_info(repo_df):
    st.write('### Top Repos')
    st.write(repo_df.sort_values('stars', ascending=False).head(10))
    st.write('---')
    st.write('### Plot of Top Repos')
    st.write(plot_repo_info(repo_df))

# get user input
query, language = get_user_input()

# get repo data
data = get_repo_data(query, language)

# get repo info
repo_df = get_repo_info(data)

# display repo info
display_repo_info(repo_df)

# Set page footer
st.write('---')
st.write('Powered by Github Copilot')
