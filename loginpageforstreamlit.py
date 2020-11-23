import streamlit as st
import datetime
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

import sqlite3
#sqlite3 stuff to store users info
conn = sqlite3.connect('data.db')
c = conn.cursor()

#traffics database
conn1 = sqlite3.connect('traffic.db')
c1 = conn1.cursor()

def create_todaytraffic():
    c1.execute('CREATE TABLE IF NOT EXISTS todaytraffic(id INT PRIMARY KEY AUTOINCREMENT,borough TEXT NOT NULL,on_street_name TEXT NOT NULL,type TEXT NOT NULL)')

def add_trafficdata(borough,on_street_name,type):
    c1.execute('INSERT INTO todaytraffic(borough,on_street_name,type) VALUES (?,?,?)',(borough,on_street_name,type))
    conn1.commit()
def deleteNull():
    c1.execute('DELETE FROM todaytraffic ')
    conn1.commit()

def view_all_info():
    c1.execute('SELECT DISTINCT * FROM todaytraffic')
    data = c1.fetchall()
    return data





#function for database connectivity and user validation
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS usertable(username TEXT,password TEXT)')

def add_userdata(username,password):
    c.execute('INSERT INTO usertable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usertable WHERE username=? AND password=?',(username,password))
    data=c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data


def deleteUserNull():
    c.execute('DELETE FROM usertable')
    conn.commit()




#background image improvisation

def homepagebck():
    page_bg_img = '''
            <style>
            body {
            background-image: url("https://images.pexels.com/photos/399161/pexels-photo-399161.jpeg?cs=srgb&dl=pexels-lumn-399161.jpg&fm=jpg");
            background-size: cover;
            }
            </style>
            '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def loginpagebck():
    page_bg_img = '''
            <style>
            body {
            background-image: url("https://images.pexels.com/photos/1323550/pexels-photo-1323550.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500");
            background-size: cover;
            }
            </style>
            '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def signuppagebck():
    page_bg_img = '''
            <style>
            body {
            background-image: url("https://images.pexels.com/photos/4197563/pexels-photo-4197563.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940");
            background-size: cover;
            }
            </style>
            '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

#function of load_data
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['crash_date', 'crash_time']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data



#main function
def main():
    menu=['Home','Login','Signup']
    st.sidebar.title("MENU")
    choice = st.sidebar.selectbox("Menu",menu)
    st.markdown(
        """
    <style>
    .sidebar .sidebar-content {
        background: url(https://images.pexels.com/photos/1111316/pexels-photo-1111316.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500);
        color: white;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    #st.sidebar.button("GOKU")

    if( choice =="Home"):
        st.title("Welcome To the HomePage")
        homepagebck()

        #[[thisisanimagelink](upload://7FxfXwDqJIZdYJ2QYADywvNRjB.png)](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data)
        st.subheader("Latest Traffic updates")
        date=datetime.datetime.now()
        st.subheader(date)
        query_view = view_all_info()
        clean_db = pd.DataFrame(query_view, columns=["LOCATION", "STREET NAME", "TYPE OF TRAFFIC"])
        st.dataframe(clean_db)
        #show data and ...
        #st.write("https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data")





    elif( choice=="Login"):
        st.header("Login Section")

        # if (st.sidebar.button("veronica")):
        #     deleteUserNull()
        loginpagebck()


        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password",type='password')
        if(st.sidebar.checkbox("Login")):

            create_usertable()
            result = login_user(username,password)
            if(result):

                st.success("Logged in as {}".format(username))

                task = st.selectbox("Task",["UPDATE","Data Set","Visualise",])
#update column of login page
                if(task=="UPDATE"):
                    st.subheader("Add current traffic update here and see that table")

                    create_todaytraffic()

                    borough = st.text_input("enter the borough")
                    on_street_name = st.text_input("enter the on_street_name")
                    type = st.text_input("enter the type")
                    #update button in updateLoginpage
                    if (st.button("UPDATE")):
                        add_trafficdata(borough, on_street_name, type)
                        query_view = view_all_info()
                        clean_db = pd.DataFrame(query_view, columns=["LOCATION", "STREET NAME", "TYPE OF TRAFFIC"])
                        st.dataframe(clean_db)
                    if(st.button("Drop all from today")):
                        deleteNull()
                        query_view = view_all_info()
                        clean_db = pd.DataFrame(query_view, columns=["LOCATION", "STREET NAME", "TYPE OF TRAFFIC"])
                        st.dataframe(clean_db)



                elif(task=="Data Set"):
                    st.subheader("Data Set from Uber about Newyork City")
                    #add set here

                    DATA_URL = (
                        " https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data "
                    )

                    st.markdown("This application is a streamlit dashboared that can "
                                "be used to analyse motor vhicle collision in nyc")


                    data = load_data(100000)
                    if (st.checkbox("data head", False)):
                        st.write(data.head())
                        st.info("Successfully Loaded Data Frame Head")
                    if st.checkbox("Show Raw Data", False):
                        st.subheader('Raw data')
                        st.info("Note That The Dataset is very large")
                        st.write(data)
                    # if(st.button("Visit Column Name")):
                    #     for col in data.columns:
                    #         st.write(col)




                elif(task=="Visualise"):
                    #st.subheader("Edith")

                    #add plots here
                    DATA_URL = (
                        " https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data "
                    )

                    st.markdown("This application is a streamlit dashboared that can "
                                "be used to analyse motor vhicle collision in nyc")


                    data = load_data(100000)
                    original_data=data
                    if (st.checkbox("data head", False)):
                        st.write(data.head())
                        st.info("Successfully Loaded Data Frame Head")
                    if st.checkbox("Show Raw Data", False):
                        st.subheader('Raw data')
                        st.info("Note That The Dataset is very large")
                        st.write(data)
                    st.header("Where are he most people injured in NYC?")
                    injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
                    st.map(
                        data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))


                    st.header("How many collisions occured during a given time of day?")
                    hour = st.slider("Hour to look at", 0, 23)
                    data = data[data['crash_date_crash_time'].dt.hour == hour]

                    st.markdown("Vehicle Collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))

                    midpoint = (np.average(data['latitude']), np.average(data['longitude']))

                    st.write(pdk.Deck(
                        map_style="mapbox://styles/mapbox/light-v9",
                        initial_view_state={
                            "latitude": midpoint[0],
                            "longitude": midpoint[1],
                            "zoom": 11,
                            "pitch": 50,

                        },
                        layers=[
                            pdk.Layer(
                                "HexagonLayer",
                                data=data[['crash_date_crash_time', 'latitude', 'longitude']],
                                get_position=['longitude', 'latitude'],
                                radius=100,
                                extruded=True,
                                pickable=True,
                                elevation_range=[0, 1000],
                            ),
                        ],

                    ))

                    st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
                    filtered = data[
                        (data['crash_date_crash_time'].dt.hour >= hour) & (
                                    data['crash_date_crash_time'].dt.hour < (hour + 1))
                        ]
                    hist = np.histogram(filtered['crash_date_crash_time'].dt.minute, bins=60, range=(0, 60))[0]
                    chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
                    fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
                    st.write(fig)

                    st.header("Top 5 dangerous streets by affected type")
                    st.markdown("based on visualisation and data interpretation")
                    select = st.selectbox('Affected type of people', ['Pedestrians', 'Cyclists', 'Motorists'])

                    if (select == 'Pedestrians'):
                        st.write(original_data.query("injured_pedestrians >= 1")[
                                     ["on_street_name", "injured_pedestrians"]].sort_values(by=['injured_pedestrians'],
                                                                                            ascending=False).dropna(
                            how="any")[:5])



                    elif (select == 'Cyclists'):
                        st.write(original_data.query("injured_cyclists >= 1")[
                                     ["on_street_name", "injured_cyclists"]].sort_values(by=['injured_cyclists'],
                                                                                         ascending=False).dropna(
                            how="any")[:5])

                    else:
                        st.write(original_data.query("injured_motorists >= 1")[
                                     ["on_street_name", "injured_motorists"]].sort_values(by=['injured_motorists'],
                                                                                          ascending=False).dropna(
                            how="any")[:5])





            else:
                st.warning("Incorrect Username/Password")
                st.markdown("Enter correct Username/Password and try again")
                st.info("Go in sidebar to Signup for free")







    elif( choice=="Signup"):
        signuppagebck()
        # background for signup pages
        #https://images.pexels.com/photos/399161/pexels-photo-399161.jpeg?cs=srgb&dl=pexels-lumn-399161.jpg&fm=jpg
        st.subheader("Create New Account")
        new_user= st.text_input("Username")
        new_password = st.text_input("Password",type="password")

        if(st.button("Signup")):
            create_usertable()
            add_userdata(new_user,new_password)
            st.success("You Have Succesfully Created a Valid Account")
            st.info("Go in to Login Menu to login ")




hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




if __name__=='__main__':
    main()

