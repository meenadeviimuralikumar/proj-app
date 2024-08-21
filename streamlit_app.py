import streamlit as st
import pandas as pd


st.set_page_config(
    page_title = "Interactive Prototype",
    initial_sidebar_state = "expanded",
    menu_items={},
    layout="wide"
)


@st.cache_data
def load_data(data_path):
    df = pd.read_csv(data_path)
    df = df.drop(columns=['Dataset','Comment_Id'])
    df = df[['Community', 
             'Comment', 
             'User_Rated_Sexism', 
             'User_Reasoning',
             'Perspective_Toxicity',
             'Perspective_Identity_Attack',
             'Perspective_Insult',
             'Perspective_Profanity','GPT_Sexism_Rating','GPT_Sexism_Score']]
    return df

@st.cache_data
def getPerspectiveToxicityData(df):
    toxicity_df = df.drop(columns = ['Perspective_Identity_Attack' ,
                                'Perspective_Insult' ,
                                'Perspective_Profanity',
                                'GPT_Sexism_Score', 
                                'GPT_Sexism_Rating'])
    return toxicity_df

@st.cache_data
def getPerspectiveIDAData(df):
    ida_df = df.drop(columns = ['Perspective_Toxicity' ,
                                'Perspective_Insult' ,
                                'Perspective_Profanity',
                                'GPT_Sexism_Score', 
                                'GPT_Sexism_Rating'])
    return ida_df

@st.cache_data
def getPerspectiveInsultData(df):
    insult_df = df.drop(columns = ['Perspective_Toxicity' ,
                                'Perspective_Identity_Attack' ,
                                'Perspective_Profanity',
                                'GPT_Sexism_Score', 
                                'GPT_Sexism_Rating'])
    return insult_df

@st.cache_data
def getPerspectiveProfanityData(df):
    profanity_df = df.drop(columns = ['Perspective_Toxicity' ,
                                'Perspective_Identity_Attack' ,
                                'Perspective_Insult',
                                'GPT_Sexism_Score', 
                                'GPT_Sexism_Rating'])
    return profanity_df

@st.cache_data
def getGPTData(df):
    gpt_df = df.drop(columns = ['Perspective_Toxicity', 
                                'Perspective_Identity_Attack' ,
                                'Perspective_Insult' ,
                                'Perspective_Profanity',
                                'GPT_Sexism_Rating'])
    return gpt_df


df = load_data("./data/sexism_prototype.csv")
toxicity_df = getPerspectiveToxicityData(df)
ida_df = getPerspectiveIDAData(df)
insult_df = getPerspectiveInsultData(df)
profanity_df = getPerspectiveProfanityData(df)
gpt_df = getGPTData(df)

model_attributes_list = ["Perspective Toxicity", 
         "Perspective Identity Attack",
         "Perspective Insult",
         "Perspective Profanity",
         "GPT Sexism"]
rows = 5

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
        "Select a model and attribute to view scores",
        ("Perspective Identity Attack",
         "GPT Sexism",
         "Perspective Insult"),
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
        if(model_option in model_attributes_list):
            st.divider()
            first = st.columns(3)
            #st.write(pd.crosstab(df['Community'], df['User_Rated_Sexism']))
            #if(model_option == model_attributes_list[0]):
            #    histcol = 'Perspective_Toxicity'
            #elif(model_option == model_attributes_list[1]):
            #    histcol = 'Perspective_Identity_Attack'
            #elif(model_option == model_attributes_list[2]):
            #    histcol = 'Perspective_Insult'
            #elif(model_option == model_attributes_list[3]):
            #    histcol = 'Perspective_Profanity'
            #else:
            #    histcol = 'GPT_Sexism_Score'
            #fig = px.histogram(df, x = histcol)
            #fig.show()
            #df.hist(column=histcol, bins = 10)

            with first[0]:
                st.write("Filter data by the Community from which the comment was sourced.")
                cat_list = df.Community.unique()
                val = [None]* len(cat_list) # this list will store info about which category is selected
                for i, cat in enumerate(cat_list):
                    val[i] = st.checkbox(cat, value=True) # value is the preselect value for first render
            with first[1]:
                st.write("Filter data by sexist or non-sexist comments  ")
                pos = st.radio(
                    " ",
                    ["Sexist", "Not Sexist"],
                )
                bool_pos =  True if pos == 'Sexist' else False
            with first[2]:
                st.write("Select upper or lower range of model scores, with cutoff at 0.5/50")
                #rows = st.number_input(" ", 
                #                    min_value = 5,
                #                    max_value = 25,
                #                    step = 5)
                
                scores = st.radio(
                    " ",
                    ["Lower Range (< 0.5)", "Upper Range (> 0.5)"],
                )
               
            st.write(" ")
            #html_str = f"""
            #    <p><i>Viewing {rows} rows</p>
            #    """
            #st.markdown(html_str, unsafe_allow_html = True)
            if(scores == 'Lower Range (< 0.5)'):
                lb_score = 1
            elif(scores == 'Upper Range (> 0.5)'):
                lb_score = 0

    if(model_option == model_attributes_list[0]):
        st.write(toxicity_df[toxicity_df.Community.isin(cat_list[val]) 
         & (toxicity_df['User_Rated_Sexism'] == bool_pos)])

    if(model_option == model_attributes_list[1]):
        if(lb_score) == 1:
            st.write(ida_df[ida_df.Community.isin(cat_list[val]) 
                & (ida_df['User_Rated_Sexism'] == bool_pos)
                & (ida_df['Perspective_Identity_Attack'] >= 0.0)
                & (ida_df['Perspective_Identity_Attack'] < 0.5)
                ])
        else:
            st.write(ida_df[ida_df.Community.isin(cat_list[val]) 
                & (ida_df['User_Rated_Sexism'] == bool_pos)
                & (ida_df['Perspective_Identity_Attack'] >= 0.5)
                & (ida_df['Perspective_Identity_Attack'] < 1.0)
                ])
        
    if(model_option == model_attributes_list[2]):
        if(lb_score) == 1:
            st.write(insult_df[insult_df.Community.isin(cat_list[val]) 
                & (insult_df['User_Rated_Sexism'] == bool_pos)
                & (insult_df['Perspective_Insult'] >= 0.0)
                & (insult_df['Perspective_Insult'] < 0.5)
                ])
        else:
            st.write(insult_df[insult_df.Community.isin(cat_list[val]) 
                & (insult_df['User_Rated_Sexism'] == bool_pos)
                & (insult_df['Perspective_Insult'] >= 0.5)
                & (insult_df['Perspective_Insult'] < 1.0)
                ])
        
    if(model_option == model_attributes_list[3]):
        if(lb_score) == 1:
            st.write(profanity_df[profanity_df.Community.isin(cat_list[val]) 
                & (profanity_df['User_Rated_Sexism'] == bool_pos)
                & (profanity_df['Perspective_Profanity'] >= 0.0)
                & (profanity_df['Perspective_Profanity'] < 0.5)
                ])
        else:
            st.write(profanity_df[profanity_df.Community.isin(cat_list[val]) 
                & (profanity_df['User_Rated_Sexism'] == bool_pos)
                & (profanity_df['Perspective_Profanity'] >= 0.5)
                & (profanity_df['Perspective_Profanity'] < 1.0)
                ])
        
    if(model_option == model_attributes_list[4]):
        if(lb_score) == 1:
            st.write(gpt_df[gpt_df.Community.isin(cat_list[val]) 
                & (gpt_df['User_Rated_Sexism'] == bool_pos)
                & (gpt_df['GPT_Sexism_Score'] >= 0)
                & (gpt_df['GPT_Sexism_Score'] < 50)
                ])
        else:
            st.write(gpt_df[gpt_df.Community.isin(cat_list[val]) 
                & (gpt_df['User_Rated_Sexism'] == bool_pos)
                & (gpt_df['GPT_Sexism_Score'] >= 50)
                & (gpt_df['GPT_Sexism_Score'] < 100)
                ])


if data_option == 'Other':
    st.write("You can upload datasets using options in the sidebar.")

