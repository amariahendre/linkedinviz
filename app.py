import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Sidebar Instructions for LinkedIn Data Download
st.sidebar.title("How to Download Data from LinkedIn")
st.sidebar.markdown(
    """
    1. Click on your **Me** drop-down on the LinkedIn homepage.
    2. Head over to **Settings & Privacy**.
    3. Click on **Data Privacy**.
    4. Click on **Get a copy of your data**.
    5. Check **Connections** only, and hit **Request archive**.
    6. After a few minutes, you should get the archive file in your email.
    """
)

# Title for the app
st.title('Linkedin Data Visualization App')

# Function to convert DataFrame to Excel
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# File upload widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Read the uploaded file into a DataFrame, skipping the first two rows
    df = pd.read_csv(uploaded_file, skiprows=2)
    
    # Display the DataFrame in the app
    # st.dataframe(df)
    
    # Subtitle for the download button
    st.subheader('Download the Data as Excel')

    # Allow user to download the DataFrame as an Excel file
    # st.download_button(label='📥 Download Excel', 
    #                    data=to_excel(df),
    #                    file_name='linkedin_connections.xlsx',
    #                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    flnme = 'linkedin_connections.xlsx'
    if flnme:
        if not flnme.endswith(".xlsx"):  # add file extension if it is forgotten
            flnme = flnme + ".xlsx"

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Report')
        
        st.download_button(label='📥 Download Excel', data=buffer.getvalue(), file_name=flnme, mime="application/vnd.ms-excel")

    # Ensure the necessary columns exist
    if all(column in df.columns for column in ['Company', 'Position', 'Connected On']):
        # Company value counts bar chart
        st.subheader('Top 10 Companies')
        company_counts = df['Company'].value_counts().head(10)
        fig = px.bar(company_counts, orientation='h', labels={'value':'Count', 'index':'Company'})
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Position value counts bar chart
        st.subheader('Top 10 Positions')
        position_counts = df['Position'].value_counts().head(10)
        fig = px.bar(position_counts, orientation='h', labels={'value':'Count', 'index':'Position'})
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Connected On histogram
        st.subheader('Connections Over Time')
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        fig = px.histogram(df, x='Connected On', nbins=15, labels={'Connected On':'Connected On'})
        fig.update_xaxes(title='Connected On')
        fig.update_yaxes(title='Count')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error('Uploaded file does not contain the required columns: Company, Position, Connected On.')
