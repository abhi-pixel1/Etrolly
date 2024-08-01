import streamlit as st
from streamlit_server_state import server_state
from streamlit_star_rating import st_star_rating
import mysql.connector
from PIL import Image
from datetime import datetime





st.set_page_config(layout='wide',initial_sidebar_state='collapsed')






root = mysql.connector.connect(host = 'localhost', password = 'root', user = 'root', database = 'etrolly')
sql_select_Query = f"select * from product where product_id = '{server_state.prd}' "
cursor = root.cursor()





cursor.execute(sql_select_Query)
records = cursor.fetchall()






if "disable_cart" not in server_state:
   server_state.disable_cart = True



if len(server_state.cust_auth) > 1:
    server_state.disable_cart = False
else:
    server_state.disable_cart = True



qunatity_in_cart = 1
quantity_query = f"select total_count from cart where product_id='{records[0][0]}' and customer_id='{server_state.cust_auth}'"
cursor.execute(quantity_query)
cart_data = cursor.fetchall()
if cart_data != []:
    qunatity_in_cart = cart_data[0][0]    


















col1, col2, col3 = st.columns([1, 3, 1], gap = "large")


image = Image.open('C:\\Users\\bhara\\Desktop\\ama-img\\'+records[0][5])
col1.image(image.resize((340, 330)))
with col1:
    stars = st_star_rating("", size=20,maxValue=5, defaultValue=3.5, key="rating", dark_theme = True)

col2.subheader(records[0][2])
col2.write(records[0][3])
with col2.expander("Add a review"):
    with st.form("my_form"):
        user_rating = st_star_rating("Please rate the product", size=20, maxValue=5, defaultValue=3.5, dark_theme = True)
        comments = st.text_input("Add comments")
        submit_review = st.form_submit_button('Submit')
col2.write("---")

col2.subheader("Reviews")


review_getter = f"select * from review where product_id='{records[0][0]}'"
cursor.execute(review_getter)
reviews_list = cursor.fetchall()

with col2:
    for i in reviews_list:
        cust_review_name_query = f"select name from customer where customer_id='{i[0]}'"
        cursor.execute(cust_review_name_query)
        cust_review_name = cursor.fetchall()
        st.write(cust_review_name[0][0])
        st.write(i[2])
        stars = st_star_rating("", size=20,maxValue=5, defaultValue=i[4], dark_theme = True)
        st.write(i[3])
        st.write("---")



    







if submit_review:
    curr_date = current_date = datetime.now().date()
    curr_date_string = current_date.strftime("%Y-%m-%d")
    review_query = f"INSERT INTO review VALUES ('{server_state.cust_auth}', '{records[0][0]}', '{curr_date_string}', '{comments}', {user_rating});"
    cursor.execute(review_query)
    root.commit()
    





cart = col3.form('cart')
quantity = cart.number_input("Quantity", value=qunatity_in_cart, min_value=1, step=1, disabled=server_state.disable_cart)
cart_button = cart.form_submit_button("Add to cart")
remove = col3.button("Remove from cart", disabled=server_state.disable_cart)






if cart_button:
    if(len(server_state.cust_auth) > 1):
        try:
            q = f"insert into cart values ('{records[0][0]}', '{server_state.cust_auth}', {quantity}, {records[0][4]*quantity})"
            cursor.execute(q)
            root.commit()
        except Exception as e:
            q = f"UPDATE cart set total_count = {quantity}, final_amount = {records[0][4]*quantity} where product_id='{records[0][0]}' and customer_id='{server_state.cust_auth}'"
            cursor.execute(q)
            root.commit()

        col3.write(f"{quantity} items added to cart")
    else:
        col3.write("error")



if remove:
    remove_query = f"DELETE FROM cart WHERE product_id ='{records[0][0]}' and customer_id='{server_state.cust_auth}';"
    cursor.execute(remove_query)
    root.commit()
    






# st.write(server_state.prd)
# sql_select_Query = f"select * from product where product_id = '{server_state.prd}' "
# cursor = root.cursor()
# cursor.execute(sql_select_Query)
# records = cursor.fetchall()

# st.write(records)

st.stop()

# st.write(prd)
# prod_id = st.session_state["product"]
# st.write(prod_id)

# sql_select_Query = "select * from product where "
# cursor = root.cursor()
# cursor.execute(sql_select_Query)
# records = cursor.fetchall()


