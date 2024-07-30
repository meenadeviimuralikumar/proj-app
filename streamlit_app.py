import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = "Toolkit",
    initial_sidebar_state = "expanded",
    menu_items={},
    layout="wide"
)

@st.cache_data
def load_data(data_path):
    return pd.read_csv(data_path)

df = load_data("./data/display_sexismdata.csv")

def perspective_data():
    if call_me and (not ben) and (not hos):
        return df[df['Dataset']=="call_me"].sample(n = rows)
    elif ben and (not call_me) and (not hos):
        return df[df['Dataset']=="benevolent"].sample(n = rows)
    elif hos and (not call_me) and (not ben):
        return df[df['Dataset']=="hostile"].sample(n = rows)
    else:
        return df.sample(n = rows)
    
###
### UI Layout Code Starts
###

st.title("Data Explorer")

sb1 = st.columns(4)
with sb1[0]:
    option = st.selectbox(
        "Select a dataset",
        ("Sexist_Comment_Dataset", "Other"),
        index = None,
        placeholder=" ",
    )
with sb1[1]:
    pass
with sb1[2]:
    pass
with sb1[3]:
    pass

if option == 'Sexist_Comment_Dataset':
    sb2 = st.columns(4)
    with sb2[0]:
        option = st.selectbox(
        "Select a model for scoring the data",
        ("Perspective", "GPT"),
        index = None,
        placeholder=" ",)
    with sb2[1]:
        pass
    with sb2[2]:
        pass
    with sb2[3]:
        pass
    st.markdown('######')
    with st.container():
        if(option == 'Perspective' or option == 'GPT'):
            first = st.columns(3)
            with first[0]:
                st.write("Filter data by different forms of sexism ")
                call_me = st.checkbox("Call Me Sexist")
                ben = st.checkbox("Benevolent Sexism")
                hos = st.checkbox("Hostile Sexism")
            with first[1]:
                st.write("Select number of rows")
                rows = st.number_input(" ", 
                                    min_value = 5,
                                    max_value = 25,
                                    step = 5)
            with first[1]:
                pass
            st.write(" ")
            html_str = f"""
                <p><i>Viewing {rows} of 2636 rows</p>
                """
            st.markdown(html_str, unsafe_allow_html = True)

    if(option == 'Perspective'):
        st.table(perspective_data())



if option == 'Other':
    st.write("You can upload datasets using options in the sidebar.")

