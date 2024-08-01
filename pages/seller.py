import streamlit as st
import hydralit as hy
import webbrowser
from PIL import Image
import mysql.connector
from streamlit_server_state import server_state
from PIL import Image
import os
import uuid







app = hy.HydraApp(title='Simple Multi-Page App')












if "auth" not in st.session_state:
   st.session_state["auth"] = None
   st.session_state["record"] = []





root = mysql.connector.connect(host = 'localhost', password = 'root', user = 'root', database = 'etrolly')
cursor = root.cursor()



def save_image(uploaded_file, file_name, file_extention):
    image = Image.open(uploaded_file)
    save_path = f'C:\\Users\\bhara\\Desktop\\ama-img\\{file_name}.{file_extention}'
    image.save(save_path)


def runner():
    if st.session_state["auth"] == None:
        login_page()
    elif len(st.session_state["auth"]) > 1:
        dashboard_redirect(st.session_state["record"])
    else:
        exception_redirect()





def dashboard_redirect(records):
    # st.write(records)
    st.subheader("Your Products")
    product_list_query = f"SELECT * FROM product WHERE product_id IN (SELECT product_id FROM sells WHERE seller_id = '{st.session_state['auth']}')"
    cursor.execute(product_list_query)
    product_list = cursor.fetchall()


    cart_key = 0
    cart_view = []
    for i in product_list:
        image = Image.open('C:\\Users\\bhara\\Desktop\\ama-img\\'+i[5])

        cart_view.append(st.container())
        col1, col2 = cart_view[-1].columns(2)
        col1.image(image.resize((140, 130)))

        col2.write(i[2])
        col2.write(i[3])
        col2.write(i[4])
        # col2.button("view item", args=(i[0],i[1]), on_click=product_page_redirect, key=cart_key)
        st.write("---")

        cart_key = cart_key+1


    with st.expander("Add a new product"):
        new_product_form = st.form("my_form")
        product_name = new_product_form.text_input('Enter the name of the product')
        product_description = new_product_form.text_area('Enter the product description')
        product_price = new_product_form.number_input("Enter the price of the product",min_value=1)
        uploaded_file = new_product_form.file_uploader("Choose an image...", type=["jpg", "png"])

        add_product = new_product_form.form_submit_button('Add')
        
        if add_product:
            webbrowser.open("www.google.com")
            # st.write(product_name)
            # file_extension = ''
            # file_name = str(uuid.uuid4())
            # if uploaded_file is not None:
            #     _, file_extension = os.path.splitext(uploaded_file.name)
            #     save_image(uploaded_file, file_name, file_extension)

            # add_product_query = f"call InsertProduct('{product_name}', {product_price}, '{product_description}', '{st.session_state['auth']}', '{file_name}.{file_extension}')"
            # cursor.execute(add_product_query)
            # root.commit()
    st.stop()












def exception_redirect():
    st.write("error")
    st.stop()





@app.addapp()
def login_page():
    st.write(st.session_state["auth"])

    login_input = []
    signup_input = []



    login, signup = st.tabs(["Login to existing account", "Creat new account"])

    with login:
        _,log2,_ = st.columns(3)
        with log2:
            with st.form('Login'):
                login_input.append(st.text_input("E-mail/Phone Number"))
                login_input.append(st.text_input('Password', type="password"))
                log_usr = st.form_submit_button('Login')
                # usr = st.text_input("E-mail/Phone Number")
                # pas1 = st.text_input('Password', type="password")
                # log_usr = st.form_submit_button('Login')




    with signup:
        _,sign2,_ = st.columns(3)
        with sign2:
            with st.form('addition'):
                signup_input.append(st.text_input("Name"))
                signup_input.append(st.text_input("E-mail"))
                signup_input.append(st.text_input("Phone Number"))
                signup_input.append(st.text_area("Home Address"))
                signup_input.append(st.text_input("Enter your password", type="password"))
                signup_input.append(st.text_input("confirm password", type="password"))
                sign_usr = st.form_submit_button('Sign Up')
                # name = st.text_input("Name")
                # mail = st.text_input("E-mail")
                # phone = st.number_input("Phone Number")
                # address = st.text_area("Home Address")
                # pas = st.text_input("Enter your password", type="password")
                # pas_c = st.text_input("confirm password", type="password")
                # sign_usr = st.form_submit_button('Sign Up')



    if log_usr:
        if login_input[0].isdigit():
            q = "select * from seller where phno = \'" + login_input[0] + "\' and password = \'" + login_input[1] + "\'"
        elif "@" in login_input[0]:
            q = "select * from seller where email = \'" + login_input[0] + "\' and password = \'" + login_input[1] + "\'" 
        else:
            st.session_state["auth"] = '0'
            exception_redirect()


        cursor.execute(q)
        # get all records
        records = cursor.fetchall()
        st.session_state["auth"] = records[0][0]
        st.session_state["record"] = records
        runner()
        # dashboard_redirect(records,pas1)
        # else:
            # exception_redirect()

    

    if sign_usr:
        if("" in signup_input):
            exception_redirect()

        elif(signup_input[4] != signup_input[5]):
            exception_redirect()

        else:
            q = f"insert into seller values (UUID(), '{signup_input[0]}', '{signup_input[5]}', 1, 1, '{signup_input[3]}', '{signup_input[1]}', '{signup_input[2]}')"
            cursor.execute(q)
            root.commit()
            st.write(signup_input)











# runner()
app.run()