import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px

def create_web_app():
    # Connect to the database
    st.write("Connecting to the database...")
    engine = create_engine('mysql+pymysql://rootremote2:GW#$ETfdsfWSF@54.247.47.50/cars_data')

    # Read in data
    st.write("Reading data from the database...")
    df = pd.read_sql("""
        SELECT zone, time_start, time_end, time_end - time_start as time_spent
        FROM data
        WHERE time_start > DATE_SUB(NOW(), INTERVAL 1 WEEK);
        """, engine)

    st.write("Converting time_start to datetime...")
    #Convert time_start to datetime
    df['time_start'] = pd.to_datetime(df['time_start'], unit='s')

    # filter out the rows which does not contain the delimiter ">"
    df = df[df.zone.str.contains(">")]

    # Splitting the 'zone' column into two columns, location1, location2
    df['location1'] = df.zone.str.split(">").str.get(0)
    df['location2'] = df.zone.str.split(">").str.get(1)

    #Combining location 1 and 2 if the names are the same
    df = df.groupby(['location1','location2'], as_index=False)['time_spent'].sum()

    # data visualization
    st.write("Time spent in each location: ")
    st.bar_chart(df)

if __name__=="__main__":
    create_web_app()
