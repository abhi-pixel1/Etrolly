import streamlit as st
from PIL import Image
# new_image = image.resize((600, 400))

col1, col2, col3 = st.columns(3,gap="small")

# with col1:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/cat.jpg")

# with col2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg")

# with col3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg")


for i in range(3):
    col1.header("A cat")
    col1.image("https://static.streamlit.io/examples/cat.jpg")
    st.empty()


    col2.header("A dog")
    col2.image("https://static.streamlit.io/examples/dog.jpg")
    st.empty()

    col3.header("An owl")
    col3.image("https://static.streamlit.io/examples/owl.jpg")


































# for i in range(3):
#     # col1.header("A cat")
#     image = Image.open('hd-spider-wallpaper-1.jpg')
#     col1.image(image.resize((340, 330)))

#     # col2.header("A dog")
#     image = Image.open('insect.jpg')
#     col2.image(image.resize((340, 330)))

#     # col3.header("An owl")s
#     image = Image.open('pexels-michael-willinger-3483007.jpg')
#     col3.image(image.resize((340, 330)))

#     image = Image.open('Screenshot 2023-09-13 155859.png')
#     col4.image(image.resize((340, 330)))