# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import panda as pd_df

# Write directly to the app
st.title(":cup_with_straw: Customize your Smothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

#convert the snowopark dateframe to a panda dataframe so we can use the loc function
pd_df=my_dataframe.to_panda()
st.stop()

ingredients_list = st.multiselect(
    'Choose up tp 5 ingredients:' 
    , my_dataframe
    , max_selections=5
    )
if ingredients_list:
  

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
        st.subheader(fruit_chosen + 'Nutritrion information')
        smoothiefroot_response = requests.get("https://FRUITYVICE.com/api/fruit/watermelon" + fruit_chosen)
        st.df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" + name_on_order + """')"""
     
    time_to_insert = st.button('Submit order')
     
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
        
       st.success("Your Smoothie is ordered!", icon="✅")

        
       

