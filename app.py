import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import folium
from streamlit_folium import folium_static

# Background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
                                            background-color: #ed9fa6 !important;
                                            }}
[data-testid="stHeader"] {{
                        background: rgba(0,0,0,0);
                        }}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)



def main():
    # User's input, there are 6 information needed to be filled by user
    st.title(":blue[_Ride to the World_] 🌏🚎💨")

    st.header(":blue[Your budget Your trip 🗽]", divider=True)
    st.subheader("***In this application, we will propose you the destinations designed for you by your wishes and budget.***")

    col1, col2 = st.columns(2, gap="small")
    with col1:
        ### input1: month
        month = st.selectbox(
                                ":blue[***In which month would you like to travel?***]",
                                ("January", "February",
                                        "March", "April",
                                        "May", "June",
                                        "July", "August",
                                        "September", "October",
                                        "November", "December")
                                )
        st.write("You selected:", month)

        if month == "January":
            month_code = 1
        elif month == "February":
            month_code = 2
        elif month == "March":
            month_code = 3
        elif month == "April":
            month_code = 4
        elif month == "May":
            month_code = 5
        elif month == "June":
            month_code = 6
        elif month == "July":
            month_code = 7
        elif month == "August":
            month_code = 8
        elif month == "September":
            month_code = 9
        elif month == "October":
            month_code = 10
        elif month == "November":
            month_code = 11
        else:
            month_code = 12

    with col2:

        ### input3: Air auality
        air_qual = st.selectbox(
                                ":blue[***Which level of air quality do you expect?***]",
                                ("Very Bad", "Bad", "Not Good", "Moderate","Good")
                                )
        st.write("You selected:", air_qual)
    

        if air_qual == "Very Bad":
            air_qual_code = 0
        elif air_qual == "Bad":
            air_qual_code = 1
        elif air_qual == "Not Good":
            air_qual_code = 2
        elif air_qual == "Moderate":
            air_qual_code = 3
        else:
            air_qual_code = 4

    col1, col2 = st.columns(2, gap="small")
    with col1:

        ### input2: avgTemperature

        temp = st.text_input(":blue[***What is your average Temperature that you expect?***]", "20")
        temp = int(temp)
        st.write("You inputted", temp, "°C")  

        ### input4: budget hotel

        hotel = st.text_input(":blue[***What is your average budget for hotel per day?***]", "50")
        hotel = int(hotel)
        st.write("You inputted", hotel, "USD")

    with col2:

     ### input5: budget food

        food = st.text_input(":blue[***What is your average budget for food per day?***]", "50")
        food = int(food)
        st.write("You inputted", food, "USD")

        ### input5: budget transport

        transport = st.text_input(":blue[***What is your average budget for transport per day?***]", "10")
        transport = int(transport)
        st.write("You inputted", transport, "USD")





    # Importing datasets
    df_main = pd.read_csv(r"dashboard.csv")
    
    df_user = [[month_code, temp, air_qual_code, hotel, food, transport]]

    ### Traite df for model
    df = df_main[['Month', 'AvgTemperature', 'air_quality_label', 'hotel_price_avg', 'budget_food_avg',
       'budget_transport_avg', 'City']].copy()
    
    dico_air = {'Very Bad': 0, 'Bad': 1, 'Not Good': 2, 'Moderate': 3,'Good':4}
    df['air_quality_label'] = df['air_quality_label'].replace(dico_air)

    ### Train model
    # Initialize variable X
    X = df[['Month', 'AvgTemperature', 'air_quality_label', 'hotel_price_avg', 'budget_food_avg','budget_transport_avg']]
    y = df['City']

    # Standardize features of X
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)

    #Create a function to return recommendated city
    # Scale searching value
    input_scaled = scaler.transform(df_user)
 
    # Fit model
    modelKNN = NearestNeighbors(n_neighbors=5)
    modelKNN.fit(X_scaled)

    # Identify distance and indeices of similar cities
    neigh_dist, neigh_cities = modelKNN.kneighbors(input_scaled, n_neighbors=11)
    cities_proposed = neigh_cities[0][0:]
    

    st.markdown(" ")
    st.header(":blue[We would like to recommend you destinations below. Hope you will like them!]😎", divider='blue')
    

    # Change Month into text
    dico_month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'Jun',
                  7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    df_main['Month_text'] = df_main['Month'].replace(dico_month)

    recom = df_main.iloc[cities_proposed]
    #df_main['coordonates'] = df_main['coordonates'].apply(lambda x: list(x))
    #df_main['coordonates_country'] = df_main['coordonates_country'].apply(lambda x: list(x))
    # Loop to return each city with photo

    for i, row in recom.iterrows():
        if row["Month"] == month_code:

            photo_city = row["City"]
            st.image(r"photo/" + photo_city + ".png")
            st.markdown(" ")
            col1, col2 = st.columns(2, gap='small')
            with col1:
                st.write("Region:", str(row["Region"]))
                st.write("Country:", str(row["Country"]))
                st.write("City:", str(row["City"]))
                st.write("Average Temperature in ", str(row["Month_text"]), " : ", str(row["AvgTemperature"]), "°C")
                st.write("Air Quality Index: ", row["Air_Quality_Index"], "which means ", str(row["air_quality_label"]))
                st.write("Healthcare Index: ", row["Healthcare_Index"], "which means ", str(row["healthcare_label"]))
                st.write("Decibel Level: ", row["Decibel_Level"], "which means ", str(row["decibel_label"]))
                st.write("Happiness score of the city:", row["Happiness_Score"])
            with col2:
                st.write("Cost of Living Index:", row["Cost_of_Living_Index"])
                st.write("Average Hotel Cost:", row["hotel_price_avg"], "USD")
                st.write("Average Food Cost:", round(row["budget_food_avg"], 2), "USD")
                st.write("Average Transport Cost:", round(row["budget_transport_avg"], 2), "USD")
                st.write("Price for one combe in McDonal:", row["combo_meal_mcdo"], "USD")
                st.write("Price for one meal in Cheap Restaurant:", row["meal_inexpensive_res"], "USD")
                st.write("Price for one full menu in a Mid-range Restaurant:", row["Res_3course1P"], "USD")

            st.markdown(" ")
           
            ###Folium

            m = folium.Map(location=row['coordonates'].strip('][').split(', '), zoom_start=5)
            folium.Marker(
                location=row['coordonates'].strip('][').split(', '),
                popup= row['City'],
                icon=folium.Icon(color='purple', icon='fa fa-flag', prefix='fa')).add_to(m)
            
            folium_static(m, height=500, width=700)
            
            st.header(" ", divider='blue')
    


            
        else:
            pass

    st.header(":blue[_Voilà, Let's goooo_]📢💥🚀")
            




main()