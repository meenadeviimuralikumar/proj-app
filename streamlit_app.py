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
    df = pd.read_csv(data_path)
    df = df.rename(columns={"User_Is_Sexist": "User_Rated_Sexism", 
                            "User_Rated_Sexist_Content_Reasoning": "User_Reasoning"})
    df = df[['Comment_Id', 'Dataset', 'Comment', 'User_Rated_Sexism', 'User_Reasoning',
             'Perspective_Toxicity', 'Perspective_Identity_Attack', 'Perspective_Insult','Perspective_Profanity',
             'GPT_Sexism_Rating','GPT_Sexism_Score']]
    return df

@st.cache_data
def getPerspectiveData(df):
    perspective_df = df.drop(columns = ['GPT_Sexism_Score', 'GPT_Sexism_Rating'])
    perspective_df.set_index('Comment_Id', inplace=True)
    return perspective_df

@st.cache_data
def getGPTData(df):
    gpt_df = df.drop(columns = ['Perspective_Toxicity', 
                                'Perspective_Identity_Attack' ,
                                'Perspective_Insult' ,
                                'Perspective_Profanity'])
    gpt_df.set_index('Comment_Id', inplace=True)
    return gpt_df



df = load_data("./data/display_sexismdata.csv")
perspective_df = getPerspectiveData(df)
gpt_df = getGPTData(df)



###
### UI Layout Code Starts
###

st.title("Data Explorer")

sb1 = st.columns(4)
with sb1[0]:
    data_option = st.selectbox(
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

if data_option == 'Sexist_Comment_Dataset':
    sb2 = st.columns(4)
    with sb2[0]:
        model_option = st.selectbox(
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
        if(model_option == 'Perspective' or model_option == 'GPT'):
            st.divider()
            first = st.columns(3)
            with first[0]:
                st.write("Filter data by different forms of sexism  ")
                cat_list = df.Dataset.unique()
                val = [None]* len(cat_list) # this list will store info about which category is selected
                for i, cat in enumerate(cat_list):
                    val[i] = st.checkbox(cat, value=True) # value is the preselect value for first render
                #call_me = st.checkbox("Call Me Sexist")
                #ben = st.checkbox("Benevolent Sexism")
                #hos = st.checkbox("Hostile Sexism")
            with first[1]:
                st.write("Filter data by sexist or non-sexist comments  ")
                pos = st.radio(
                    " ",
                    ["Sexist", "Not Sexist"],
                )
                bool_pos =  True if pos == 'Sexist' else False
            with first[2]:
                st.write("Select number of rows")
                rows = st.number_input(" ", 
                                    min_value = 5,
                                    max_value = 25,
                                    step = 5)
            st.write(" ")
            html_str = f"""
                <p><i>Viewing {rows} of 2636 rows</p>
                """
            st.markdown(html_str, unsafe_allow_html = True)

    if(model_option == 'Perspective'):
        st.table(perspective_df[perspective_df.Dataset.isin(cat_list[val]) 
         & (perspective_df['User_Rated_Sexism'] == bool_pos)].sample(n = rows))

    if(model_option == 'GPT'):
        st.table(gpt_df[perspective_df.Dataset.isin(cat_list[val]) 
         & (gpt_df['User_Rated_Sexism'] == bool_pos)].sample(n = rows))

if data_option == 'Other':
    st.write("You can upload datasets using options in the sidebar.")

