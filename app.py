# streamlit run app.py
#conda activate base
#pip install -U streamlit
#pip install -U plotly
#streamlit run app.p


import streamlit as st
import pandas as pd
import numpy as np
import sklearn
import re
from datetime import time, datetime, timedelta
import pickle
from PIL import Image

# loading the model
model = pickle.load(open('model.pkl', 'rb'))

# setting an image and a title for the page
image = Image.open('i.jpg')
st.image(image,'')
st.title('Flight Price Prediction')

# The list that is going to be used to give the to the model 
input_data = []

# since the model uses one-hot-encoder as input data we need to create an encoder list of zeros that has the same size of the list -1 
#example --  ['Air India', 'AirAsia', 'GO FIRST', 'Indigo', 'SpiceJet', 'StarAir','Trujet', 'Vistara']  , encoded_air_line[0,0,0,0,0,0,0]
# since the one hot encoder uses the (or gate) there is only one data can be true 
#so based on this information we can make the encoded list less than the elements list
# by choosing one element that becomes true when all the elements in the encoded list is false (first element) in our model case:)


########    
def radio_creation(radio_list, radio_name):

    # A list of zeros that has the same size  of the list 
    encoded_list = np.zeros(len(radio_list), dtype=int)

    #Create a radion button and name it the given name and make the opitions the given list elements
    selected_radio = st.sidebar.radio(f':rainbow[{radio_name}]', radio_list, index=None)
    
    # if the user selected an element for the radio button 
    if  selected_radio:
        for i in range(len(radio_list)):
            # if the loop reached the element that have been choosen 
            if selected_radio == radio_list[i]:
                # change the value of the encoded element that has the same index as the element from the radio list that the user choosed  
                encoded_list[i] =1
   #delete the first element 
    encoded_list = encoded_list[1:]

    return encoded_list


### Airline
# radion button elements 
airline_list = ['Air India', 'AirAsia', 'GO FIRST', 'Indigo', 'SpiceJet', 'StarAir',
                'Trujet', 'Vistara']
encoded_airline_list = []
# create a radio button 
encoded_airline_list.extend(radio_creation(airline_list, "AirLine"))



# radion button elements
source_city_list = ['Bangalore', 'Chennai' ,'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
encoded_source_city_list = []
# create a radio button 
encoded_source_city_list.extend(radio_creation(source_city_list, "Source City"))




# radion button elements
destenation_city_list = ['Bangalore', 'Chennai' ,'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
encoded_destenation_city_list = []
# create a radio button
encoded_destenation_city_list.extend(radio_creation(destenation_city_list, "Destenation City"))





# 'departure_time_Early Morning', 'departure_time_Morning',
# 'departure_time_Afternoon', 'departure_time_Evening','departure_time_Night'
### departure_time & arrival_time

# CREATE A USER INPUT AND MAKE IT'S TITLE Departure Time AND GIVE MAKE THE TITLE HAVE RINBOW COLOR 
departure_time_str = st.sidebar.text_input(':rainbow[Departure Time (hh : mm)]', '05:00')

# USING THE REGULAR EXPRESSION LIBARY CREATE A TIME PATTREN WHICH GOING TO BE USED AS A MATCH FOR HH:MM
# (0 OR 1 WITH ANY NUMBER FROM 0-9)OR(2 WITH ANY NUMBER FROM 0-3)00 - 23
# : THE SAME GOES FOR THE PART AFTER : [0-5] CHECK IF THE FIRST DIGIT IS BETWEEN (0-5) AND THE SECOND DIGIT IS BETWEEN (0-9)
time_pattern = re.compile(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')

#IF THE ENTERED TIME BY THE USER DOESN'T MATCH THE REQUIREMENTS THEN STOP THE CODE AND GIVE THE USER AN ERROR MASSEGE
if not time_pattern.match(departure_time_str):
    st.sidebar.error('Please enter a valid time in the format (hh : mm)')
    st.stop()

#Split the departure time into 6 sections
departure_time = (pd.to_datetime(departure_time_str).hour % 24 + 4) // 4

# Split that data given by the user into hours and minutes(This part will be used in the calculating the duration of the flight)
depar_hours, depar_minutes = map(int, departure_time_str.split(':'))
selected_dep_time = time(depar_hours,depar_minutes)

# create a dictionary of 6 diffrent times of the day 
time_category_mapping = {1:'Late Night', 2:'Early Morning', 3:'Morning',
                         4:'Afternoon', 5:'Evening', 6:'Night'}

#Assign a time category based on departure_time, or 'Unknown' if not found.
result_departure_time = time_category_mapping.get(departure_time, 'Unknown')

# READ THE LAST PART OF THE  RADIO BUTTON FUNCTION TO UNDERSTAND THIS PART 
encoded_departure_time_list = [0, 0, 0, 0, 0, 0]
departure_time_list = ['Late Night', 'Early Morning', 'Morning',
                         'Afternoon', 'Evening', 'Night']
for i in range(len(departure_time_list)):
    if result_departure_time == departure_time_list[i]:
        encoded_departure_time_list[i] = 1

encoded_departure_time_list_1 = encoded_departure_time_list[1:]



#############################################################################
#Everything that happend in the departure part will reaplly in this part two#
#############################################################################
arrival_time_str = st.sidebar.text_input(':rainbow[Arrival Time (hh : mm)]', '07:10')

if not time_pattern.match(arrival_time_str):
    st.sidebar.error('Please enter a valid time in the format (hh : mm)')
    st.stop()

arrival_time = (pd.to_datetime(arrival_time_str).hour % 24 + 4) // 4
arrival_hours, arrival_minutes = map(int, arrival_time_str.split(':'))



result_arrival_time = time_category_mapping.get(arrival_time, 'Unknown')
encoded_arrival_time_list = [0, 0, 0, 0, 0, 0]
arrival_time_list = ['Late Night', 'Early Morning', 'Morning',
                         'Afternoon', 'Evening', 'Night']
for i in range(len(arrival_time_list)):
    if result_arrival_time == arrival_time_list[i]:
        encoded_arrival_time_list[i] = 1

encoded_arrival_time_list_1 = encoded_arrival_time_list[1:]





### Class

# THE ELEMENTS OF THE RADIO BUTTON
class_list = ['economy', 'business']

# create  the radio button with the NAME CLASS AND IT WILL CONTAIN  elements from the class_list AS CHOISCES
class_str = st.sidebar.radio(':rainbow[Class]', class_list, index=None)

# IF THE USER CLICED ON ONE OF THE CHOISES
if class_str:
    class_num = class_list.index(class_str)
    



### Stops
# THE ELEMENTS OF THE RADIO BUTTON 
stop_list = ['Non-Stop', '1 Stop', '+2 Stops']

#CREATE A RADIO BUTTON WITH THE NAME STOP AND IT WILL CONTAIN THE ELEMENTS FROM THE stop_list AS CHOICES
stop_str = st.sidebar.radio(':rainbow[Stop]', stop_list, index=None)
# CREATE A DICTION*** AND MAKE THE LIST ELEMENT THE KEYS  
stop_dec = {'Non-Stop': 0, '1 Stop':1, '+2 Stops':2}




# Duration is going to be calculated by subtracting the arrival time from departure time
duration_str = st.sidebar.title(':rainbow[Duration]' )

# change the time from hours to minutes and add the remaing minutes and then subtract the arrival time in minutes from depature time in minutes 
duration_in_minutes = (arrival_hours*60 + arrival_minutes) - (depar_hours*60 + depar_minutes)

# after changing calculating the duration time in minutes, this section is going to make the data be able to fit in the model
duration = np.round(((duration_in_minutes)/60),2)

# showing the duration  to the user  
st.sidebar.write(f'{int(duration_in_minutes/60)}:{int(duration_in_minutes%60)} hours')







### Days Left
# dd-mm-yyyy 
# THE SAME THING WE DID WITH TIME PATTREN BUT ON DATE 
dagte_pattern = re.compile(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$')

date_str = st.sidebar.text_input(':rainbow[Date (dd : mm : yyyy)]', '25-01-2024')

# IF THE GIVEN DATE BY THE USER DOESN'T FIT PATTREN WE MADE GIVE AN ERROR TO THE USER AND STOP THE CODE 
if not dagte_pattern.match(date_str):
    st.sidebar.error('Please enter a valid date in the format (dd : mm : yyyy)')
    st.stop()

# SPLIT THE DATA INTO DAY-MONTH-YEAR
day, month, year = map(int, date_str.split('-'))

# USE THE DATETIME FUNCTION FROM TIME LIBARY TO STORE THE DAY,MONTH,YEAR AS A DATE
selected_date = datetime(year, month, day).date()

# Calculate days left
current_date = datetime.now().date() # .NOW() WILL READ THE CURRENT DATE FROM THE USER'S DEVICE
days_left = (selected_date - current_date).days

# IF THE AMOUNT OF DAYS LEFT IS LESS THAN ZERO THEN THE HAVE PASSED SO THE USER MUST ENTER A DATE IN THE FUTURE
if days_left < 0:
    st.sidebar.error('Please enter a future date.')
    st.stop()

st.sidebar.write(f'{days_left} days')





### Model
if st.button('Predict'):

    # this part will prevent the user from choosing the same city as a source city and a destination 
    if encoded_source_city_list == encoded_destenation_city_list:
        st.error("You can't choose the same city as a source city and a destination city")
        st.stop()
    
    # This part takes the collected data from the user
    input_data.append(duration)
    input_data.append(stop_dec[stop_str])
    input_data.append(class_num)
    input_data.append(days_left)
    input_data.extend(encoded_airline_list)
    input_data.extend(encoded_source_city_list)
    input_data.extend(encoded_destenation_city_list)
    input_data.extend(encoded_departure_time_list_1)
    input_data.extend(encoded_arrival_time_list_1)

    #change the input data into 2d array
    input_data_2D = np.asarray([input_data])

    price = model.predict(input_data_2D)
    st.write(f'The Price in rubee : {np.round(price[0], 2)} ₹')
    st.write(f'The Price in usd   : {np.round(price[0] * 0.012 ,2) } $')
    st.snow()
    