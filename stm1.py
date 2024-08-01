#when we import hydralit, we automatically get all of Streamlit
import streamlit as st
from streamlit_server_state import server_state
import hydralit as hy
import webbrowser
from PIL import Image
import mysql.connector


if "prd" not in server_state:
   server_state.prd = []

if "cust_auth" not in server_state:
   server_state.cust_auth = ""




if "cust_auth" not in st.session_state:
   st.session_state["cust_auth"] = ""
   st.session_state["cust_record"] = []



st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)





root = mysql.connector.connect(host = 'localhost', password = 'root', user = 'root', database = 'etrolly')
app = hy.HydraApp(title='Simple Multi-Page App')








def dashboard_redirect(records):
    st.write(records[0][0])
    st.write("============")
    st.write(records[0][1])
    st.stop()







def exception_redirect():
    st.write("error")
    st.stop()









def runner():
    if len(st.session_state["cust_auth"]) > 1:
        dashboard_redirect(st.session_state["cust_record"])
    else:
        exception_redirect()









def product_page_redirect(prod_id,i):
    server_state.prd = prod_id
    server_state.cust_auth = st.session_state["cust_auth"]
    webbrowser.open("http://localhost:8501/product")









if len(st.session_state["cust_auth"]) > 1:
    st.text(f'Welcome to Etrolly, {st.session_state["cust_record"][0][1]}')
    st.write("---")
else:
    st.text('Welcome to Etrolly')
    st.write("---")





@app.addapp(is_home=True)
def my_home():
    sql_select_Query = "select * from product"
    cursor = root.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    cols = []
    cols = st.columns(4,gap="small")

    card_keys = 0

    filling_col = 0
    for i in records:
        container = cols[filling_col].container()

        image = Image.open('C:\\Users\\bhara\\Desktop\\ama-img\\'+i[5])
        container.image(image.resize((340, 330)), caption=i[2])
        if len(i[3]) > 30:
            container.write(i[3][:30]+"...")
        else:
            container.write(i[3])
        container.write(i[4])
        container.button("View product", key=card_keys, args = (i[0],i[1]), on_click=product_page_redirect)

        card_keys = card_keys+1
        filling_col = filling_col+1
        if(filling_col == 4):
            filling_col = 0











@app.addapp()
def login():
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
                # pas = st.text_input('Password', type="password")
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
                # phone = st.text_input("Phone Number")
                # address = st.text_area("Home Address")
                # pas = st.text_input("Enter your password", type="password")
                # pas_c = st.text_input("confirm password", type="password")
                # sign_usr = st.form_submit_button('Sign Up')

    if log_usr:
        if login_input[0].isdigit():
            q = "select * from customer where phno = \'" + login_input[0] + "\' and password = \'" + login_input[1] + "\'"
        elif "@" in login_input[0]:
            q = "select * from seller where email = \'" + login_input[0] + "\' and password = \'" + login_input[1] + "\'" 
        else:
            st.session_state["auth"] = '0'
            exception_redirect()


        cursor = root.cursor()
        cursor.execute(q)
        # get all records
        records = cursor.fetchall()
        st.session_state["cust_auth"] = records[0][0]
        st.session_state["cust_record"] = records
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
            q = f"insert into customer values (UUID(), '{signup_input[0]}', '{signup_input[5]}', '{signup_input[1]}', '{signup_input[2]}', '{signup_input[3]}')"
            cursor = root.cursor()
            cursor.execute(q)
            root.commit()
            st.write(signup_input)








@app.addapp()
def cart():
    if len(st.session_state["cust_auth"])<1:
        st.write("Please login first")
        # st.write(st.session_state["cust_auth"])
        # st.write(st.session_state["cust_record"])
    else:
        cart_query = f"SELECT product.product_id AS product_id, product.img AS product_img, product.name AS product_name, product.price AS product_price, cart.total_count FROM product JOIN cart ON product.product_id = cart.product_id WHERE cart.customer_id = '{st.session_state['cust_auth']}';"
        cursor = root.cursor()
        cursor.execute(cart_query)
        full_cart = cursor.fetchall()
        
        # cart_col, pay_col = st.columns([3,1])
        cart_key = 0
        cart_sum = 0
        cart_view = []
        for i in full_cart:
            image = Image.open('C:\\Users\\bhara\\Desktop\\ama-img\\'+i[1])

            cart_view.append(st.container())
            col1, col2 = cart_view[-1].columns(2)
            col1.image(image.resize((140, 130)))

            col2.write(i[2])
            col2.write(i[3])
            col2.write(i[4])
            col2.button("view item", args=(i[0],i[1]), on_click=product_page_redirect, key=cart_key)
            st.write("---")

            cart_sum = cart_sum + (i[3]*i[4])
            cart_key = cart_key+1
        
        st.header("Rs. "+str(cart_sum))
        checkout = st.button("Checkout")

        if checkout:
            checkout_procedure = f"CALL MoveCartToOrderHistory('{st.session_state['cust_auth']}');"
            cursor = root.cursor()
            cursor.execute(checkout_procedure)
            root.commit()




@app.addapp()
def order_history():
    if len(st.session_state["cust_auth"])<1:
        st.write("Please login first")
        # st.write(st.session_state["cust_auth"])
        # st.write(st.session_state["cust_record"])
    else:
        order_history_query = f"SELECT product.product_id AS product_id, product.img AS product_img, product.name AS product_name, product.price AS product_price, order_history.total_count, order_history.date FROM product JOIN order_history ON product.product_id = order_history.product_id WHERE order_history.customer_id = '{st.session_state['cust_auth']}';"
        cursor = root.cursor()
        cursor.execute(order_history_query)
        full_order_history = cursor.fetchall()
        # st.table(full_order_history)


    order_history_key = 0
    order_history_sum = 0
    order_history_view = []
    for i in full_order_history:
            image = Image.open('C:\\Users\\bhara\\Desktop\\ama-img\\'+i[1])
            order_history_view.append(st.container())
            col1, col2 = order_history_view[-1].columns(2)
            col1.image(image.resize((140, 130)))


            col2.write(i[2])
            col2.write(i[3])
            col2.write(i[4])
            col2.write(i[5])
            col2.button("view item", args=(i[0],i[1]), on_click=product_page_redirect, key=order_history_key)
            st.write("---")


            order_history_sum = order_history_sum + (i[3]*i[4])
            order_history_key = order_history_key+1












app.run()