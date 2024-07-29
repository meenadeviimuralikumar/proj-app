import streamlit as st

st.set_page_config(
    page_title = "Toolkit",
    initial_sidebar_state = "expanded",
    menu_items={}
)


st.title("Data Explorer")

option = st.selectbox(
    "Select a dataset",
    ("Sexist_Comment_Dataset", "Other"),
    index = None,
    placeholder=" ",
)

if option == 'Sexist_Comment_Dataset':
    option = st.selectbox(
    "Select a model for scoring the data",
    ("Perspective", "GPT"),
    index = None,
    placeholder=" ",)
    if(option == 'Perspective' or option == 'GPT'):
        st.write("Filter data by different forms of sexism captured in the comments")
        first = st.columns(4)
        with first[0]:
            st.write("Filters")
        with first[1]:
            call_me = st.checkbox("Call Me Sexist")
        with first[2]:
            ben = st.checkbox("Benevolent Sexism")
        with first[3]:
            hos = st.checkbox("Hostile Sexism")
        st.write(" ")
        second = st.columns(3)
        with second[0]:
            rows = st.number_input("Select number of rows", 
                                   min_value = 5,
                                   max_value = 25,
                                   step = 5)
        with second[1]:
            pass
        with second[2]:
            st.write("")
            st.button("Generate", type="primary")
    if(option == 'Perspective'):
        st.markdown('_Viewing 10 of 2636 rows.')
        st.text("Dataframe goes here")




if option == 'Other':
    st.write("You can upload datasets using options in the sidebar.")

