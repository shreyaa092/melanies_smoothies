# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in smoothie")

name_on_order= st.text_input('Name on smoothie')
st.write('The name on your smoothie is', name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the snowpark dataframe to a pandas dataframe so we can use the LOC function 
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list=st.multiselect(
    'choose up to 5 ingredients:'
    , pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string= ' '
    
    for fruit_chosen in ingredients_list:
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response=requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        fv_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #for fruit_chosen in ingredients_list:
        #ingredients_string += fruit_chosen + ' '

    #st.write( ingredients_string )
     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=st.button('Submit order')
    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
