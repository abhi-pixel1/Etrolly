import streamlit as st
import hydralit_components as hc
import datetime
from PIL import Image
import webbrowser
import mysql.connector



#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label':"Left End"},
    {'id':'Copy','icon':"🐙",'label':"Copy"},
    {'icon': "fa-solid fa-radar",'label':"Dropdown1", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Sub-item 1"},{'id':'subid12','icon': "💀", 'label':"Sub-item 2"},{'id':'subid13','icon': "fa fa-database", 'label':"Sub-item 3"}]},
    {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
    {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
    {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    {'icon': "far fa-copy", 'label':"Right End"},
    {'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)




def btn_acc(i,j):
    st.write(i)
    st.write(j)
    st.button("cheers!!!")
    st.stop()
    # webbrowser.open("http://localhost:8501/pg1")


cols = []
cols = st.columns(4,gap="small")
k = 1

for i in range(3):
    # col1.header("A cat")
    image = Image.open('hd-spider-wallpaper-1.jpg')
    cols[0].image(image.resize((340, 330)), caption=i)
    cols[0].button("add to cart", key=str(k), args = (k,'hd-spider-wallpaper-1.jpg'), on_click=btn_acc)
    k = k+1


    # col2.header("A dog")
    image = Image.open('insect.jpg')
    cols[1].image(image.resize((340, 330)), caption=str(i+1))
    cols[1].button("add to cart", key=str(k), args = (k, 'insect.jpg'), on_click=btn_acc)
    k = k+1


    # col3.header("An owl")s
    image = Image.open('pexels-michael-willinger-3483007.jpg')
    cols[2].image(image.resize((340, 330)), caption=str(i+2))
    cols[2].button("add to cart", key=str(k), args = (k, 'pexels-michael-willinger-3483007.jpg'), on_click=btn_acc)
    k = k+1


    image = Image.open('Screenshot 2023-09-13 155859.png')
    cols[3].image(image.resize((340, 330)), caption=str(i+3))
    cols[3].button("add to cart", key=str(k), args = (k, 'Screenshot 2023-09-13 155859.png'), on_click=btn_acc)
    k = k+1