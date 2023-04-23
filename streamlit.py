import streamlit as st
from github import Github
import pandas as pd

# Replace with your GitHub access token
ACCESS_TOKEN = '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'

# Authenticate with the GitHub API
g = Github(ACCESS_TOKEN)

# Get the repository
repo = g.get_repo('streamlit/streamlit')

# Create a form to enter data for the new issue
with st.form(key='new_issue_form'):
    title = st.text_input(label='Title')
    body = st.text_area(label='Body')
    submit_button = st.form_submit_button(label='Create Issue')

# Create a new issue and store the data in a CSV file when the form is submitted
if submit_button:
    # Create a new issue
    issue = repo.create_issue(
        title=title,
        body=body
    )
    st.write(f'Issue #{issue.number} created!')
    
    # Create a DataFrame with the data
    df = pd.DataFrame({'Issue Number': [issue.number], 'Title': [title], 'Body': [body]})
    
    # Append the data to the CSV file
    df.to_csv('issues.csv', mode='a', header=False, index=False)