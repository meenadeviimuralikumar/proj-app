import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title = "Interactive Prototype",
    initial_sidebar_state = "expanded",
    menu_items={},
    layout="wide"
)


###if 'clicked' not in st.session_state:
###    st.session_state.clicked = False

if 'list_of_annotations' not in st.session_state:
    st.session_state.list_of_annotations = []   

if 'box_x' not in st.session_state:
    st.session_state.box_x = [0, 0]

if 'box_y' not in st.session_state:
    st.session_state.box_y = [0, 0]

def add_annotation():
    annotation = st.session_state.text_key
    annotation_dict = {
        "annotation": annotation,
        "x1": st.session_state.box_x[0],
        "x2": st.session_state.box_x[1],
        "y1": st.session_state.box_y[0],
        "y2": st.session_state.box_y[1],
        "attr": st.session_state.model_attr
    }
    st.session_state.list_of_annotations.append(annotation_dict)
    st.session_state.text_key = ''


attr_name_dict = {
    "Perspective_Toxicity": "Toxicity",
    "Perspective_Insult": "Insult",
    "Perspective_Profanity": "Profanity",
    "Perspective_Identity_Attack": "Identity Attack",
    "GPT_Sexism_Score" : "Sexism"
}

###
### Button Functions
###
###def click_button():
###    st.session_state.clicked = True

###def reset_button():
###    st.session_state.clicked = False



### 
### Data Functions
###

@st.cache_data
def load_original_dataset(csv_path):
    df = pd.read_csv(csv_path)
    df = df[['Community', 'Comment', 'User_Rated_Sexism', 'User_Reasoning',
             'Perspective_Toxicity', 'Perspective_Identity_Attack', 'Perspective_Insult','Perspective_Profanity',
            'GPT_Sexism_Score']]
    return df

@st.cache_data
def load_data(data_path):
    return pd.read_csv(data_path)

df = load_original_dataset("./data/sexism_prototype.csv")

toxicity_pp = load_data("./data/toxicity.csv")
identityattack_pp = load_data("./data/identityattack.csv")
insult_pp = load_data("./data/insult.csv")
profanity_pp = load_data("./data/profanity.csv")

gptsexism_pp = load_data("./data/gptsexism.csv")

st.title("Interactive Analysis")


st.markdown("In this section, you can understand how well :blue[users' perceptions of sexism] correspond to different :red[model judgements], and assess impact of factors as well.")
st.markdown("Start by selecting different model attributes. The statistical analysis runs in the backend and interactive visualizations will be displayed here to convey the results.")

st.divider()

dummy1 = st.columns(2)
with dummy1[0]:
    st.selectbox("Select user attribute",
                 ("User_Rated_Toxicity", 
            "User_Rated_Identity_Attack",
            "User_Rated_Insult",
            "User_Rated_Profanity",
            "User_Rated_Sexism"),
                 index = 4,
                 placeholder="User_Rated_Sexism",
                 key = 100,
                 disabled=True)
with dummy1[1]:
    pass

dummy2 = st.columns(2)
with dummy2[0]:
    st.selectbox("Select factors of interest",
                 ("Community", 
            "User Gender",
            "User Age",
            "Comment Length"),
                 index = 0,
                 placeholder="Community",
                 key = 200,
                 disabled=True)
    

dummy = st.columns(2)
with dummy[0]:
    iv1 = st.selectbox(
            "Choose the model attribute you would like to test",
            ("Perspective_Profanity",
             "Perspective_Identity_Attack",
            "GPT_Sexism"),
            index = 0,
            placeholder=" ", 
            key = "model_attr"
        )
    c = iv1.split('_')
    model = c[0]
    if (len(c) == 2):
        attr = c[1]
    else:
        attr = "Identity Attack"
with dummy[1]:
    pass


html_option2 = f"""
<h5 style="text-align: center">User_Rated_Sexism &ensp; ~ &ensp; {iv1} &ensp; + &ensp; Communities</h5>
<br>
<p style ="text-align:center;font-style:italic">How do User ratings of Sexism and {model} {attr} scores correspond? Does this vary across the different communities?</p>
"""

st.markdown("");
st.markdown("");
st.markdown("");

st.markdown(html_option2, unsafe_allow_html=True)

st.markdown("");
st.markdown("");

###button_columns = st.columns(4)
###with button_columns[0]:
###    pass
###with button_columns[1]:
###    pass
###with button_columns[2]:
###   st.button("Run Analysis", type="primary", on_click = click_button)
###with button_columns[3]:
###    pass

st.markdown("");
st.markdown("");
st.markdown("");

st.markdown("");
st.markdown("");
st.markdown("");


st.subheader("Results", divider="gray")

analysis = st.columns(2)
with analysis[0]:
    if(attr == 'Toxicity'):
        fig = px.line(toxicity_pp, 
                x="Perspective_Toxicity", 
                y="probability_of_user_finding_comment_sexist", 
                color = 'Community',
                labels={
                        "Perspective_Toxicity": "Perspective Toxicity Score",
                        "probability_of_user_finding_comment_sexist": "Probability (User finds Comment -> Sexist)",
                        "Community": "Community"
                },
                category_orders={"Community": ['A','B','C']},
                title = "Relationship b/w Perspective's Toxicity score <br> & Probability (User finds comment Sexist)")
        fig.update_xaxes(tick0=0.1, dtick=0.1)
        fig.update_yaxes(range=[0.0, 1.0], dtick = 0.25)
        fig.update_yaxes(range=[0.0, 1.0], dtick = 0.25)
        sub = st.plotly_chart(fig, 
                        use_container_width = True, 
                        selection_mode = "box",
                        on_select="rerun")
        
    elif(attr == 'Identity Attack'):
        fig = px.line(identityattack_pp, 
                x="Perspective_Identity_Attack", 
                y="probability_of_user_finding_comment_sexist", 
                color = 'Community',
                labels={
                        "Perspective_Identity_Attack": "Perspective Identity Attack Score",
                        "probability_of_user_finding_comment_sexist": "Probability (User finds Comment -> Sexist)",
                        "Community": "Community"
                    },
                category_orders={"Community": ['A','B','C']},
                title = "Relationship b/w Perspective's Identity Attack score <br> & Probability (User finds comment Sexist)")
        fig.update_xaxes(tick0=0.0, dtick=0.1)
        fig.update_yaxes(tickvals = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        sub = st.plotly_chart(fig, 
                        use_container_width = True, 
                        selection_mode = "box",
                        on_select="rerun")
        
    elif(attr == 'Insult'):
        fig = px.line(insult_pp, 
                x="Perspective_Insult", 
                y="probability_of_user_finding_comment_sexist", 
                color = 'Community',
                labels={
                        "Perspective_Insult": "Perspective Insult Score",
                        "probability_of_user_finding_comment_sexist": "Probability (User finds Comment -> Sexist)",
                        "Community": "Community"
                    },
                category_orders={"Community": ['A','B','C']},
                title = "Relationship b/w Perspective's Insult score <br> & Probability (User finds comment Sexist)")
        fig.update_xaxes(tick0=0.1, dtick=0.1)
        fig.update_yaxes(tickvals = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        sub = st.plotly_chart(fig, 
                        use_container_width = True, 
                        selection_mode = "box",
                        on_select="rerun")
            
    elif(attr == 'Profanity'):
        fig = px.line(profanity_pp, 
                x="Perspective_Profanity", 
                y="probability_of_user_finding_comment_sexist", 
                color = 'Community',
                labels={
                        "Perspective_Profanity": "Perspective Profanity Score",
                        "probability_of_user_finding_comment_sexist": "Probability (User finds Comment -> Sexist)",
                        "Community": "Community"
                    },
                category_orders={"Community": ['A','B','C']},
                title = "Relationship b/w Perspective's Profanity score <br> & Probability (User finds comment Sexist)")
        fig.update_xaxes(tick0=0.1, dtick=0.1)
        fig.update_yaxes(range=[0.0, 1.0], dtick = 0.25)
        #fig.update_yaxes(tickvals = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        sub = st.plotly_chart(fig, 
                        use_container_width = True, 
                        selection_mode = "box",
                        on_select="rerun")
            
    elif(attr == 'Sexism'):
        fig = px.line(gptsexism_pp, 
                    x="GPT_Sexism_Score", 
                    y="probability_of_user_finding_comment_sexist", 
                    color = 'Community',
                    labels={
                        "GPT_Sexism_Score": "GPT Sexism Score",
                        "probability_of_user_finding_comment_sexist": "Probability (User finds Comment -> Sexist)",
                        "Community": "Community"
                    },
                    category_orders={"Community": ['A','B','C']},
                    title = "Relationship b/w GPT's Sexism score <br> & Probability (User finds comment Sexist)")
        fig.update_xaxes(range = [0, 100], dtick=5)
        fig.update_yaxes(tickvals = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        #fig.update_yaxes(range=[0.0, 1.0], dtick = 0.25)
        sub = st.plotly_chart(fig, 
                        use_container_width = True, 
                        selection_mode = "box",
                        on_select="rerun")

with analysis[1]:
        values = sub.selection.box

        html_cta = f"""
        <p style ="font-style:italic; color:gray">Select regions in the visualization to drill down on the data.</p>
        """
        if(len(values) == 0):
            st.write(html_cta, unsafe_allow_html = True)
        else:
            for i in values:
                st.session_state.box_x[0] = round(i["x"][0], 2)
                st.session_state.box_x[1] = round(i["x"][1], 2)
                
            for i in values:
                st.session_state.box_y[0] = round(i["y"][1], 2)
                st.session_state.box_y[1] = round(i["y"][0], 2)

            #tab1, tab2 = st.tabs(["Annotate", "Selected Data"])
            #with tab1:    
            #    ### code goes here
            #    st.write("You can annotate the selected region. Enter insights or questions here.")
            #    annotation = st.text_area(label='Add Annotation',
            #                              value=None,
            #                              key = 'text_key',
            #                              label_visibility="hidden",
            #                              on_change=add_annotation)
           
            st.write("Data that corresponds to the selected range of model attribute scores")
            key = [name for name in attr_name_dict if attr_name_dict[name] == attr]
            colname = key[0]
                #st.write(colname)
                #st.write(x1, x2)
                #st.write(y1, y2)
            x1 = st.session_state.box_x[0]
            x2 = st.session_state.box_x[1]

            y2 = st.session_state.box_y[0]
            y1 = st.session_state.box_y[1]

            subset = df[['Community', 'Comment', 'User_Rated_Sexism', 'User_Reasoning', colname]]
            subset = subset[(subset[colname] >= x1) & (subset[colname] <= x2)]
            if(colname == 'Perspective_Toxicity'):
                use_df = toxicity_pp
                use_df = use_df[(use_df['Perspective_Toxicity'] >= x1) &
                                        (use_df['Perspective_Toxicity'] <= x2)]
            elif(colname == 'Perspective_Identity_Attack'):
                use_df = identityattack_pp
                use_df = use_df[(use_df['Perspective_Identity_Attack'] >= x1) &
                                        (use_df['Perspective_Identity_Attack'] <= x2)]
            elif(colname == 'Perspective_Insult'):
                use_df = insult_pp
                use_df = use_df[(use_df['Perspective_Insult'] >= x1) &
                                        (use_df['Perspective_Insult'] <= x2)]
            elif(colname == 'Perspective_Profanity'):
                use_df = profanity_pp
                use_df = use_df[(use_df['Perspective_Profanity'] >= x1) &
                                        (use_df['Perspective_Profanity'] <= x2)]
            else:
                use_df = gptsexism_pp
                use_df = use_df[(use_df['GPT_Sexism_Score'] >= x1) &
                                        (use_df['GPT_Sexism_Score'] <= x2)]
                    
            use_df = use_df[(use_df['probability_of_user_finding_comment_sexist'] >= y2) & 
                                    (use_df['probability_of_user_finding_comment_sexist'] <= y1)]
            selected_communities = use_df['Community'].unique()
                #st.write(selected_communities)
            subset = subset[subset['Community'].isin(selected_communities)]
            st.write(subset.sort_values(by=[colname]))



#st.markdown("**Notes/Observations**")
#n = len(st.session_state.list_of_annotations)
#ncols = 2
#nrows = 1
#if n != 0:
#    if (n < ncols):
#       nrows = 1
#    elif (n % 2 == 0):
#        nrows = int(n/2)
#    elif (n % 2 != 0):
#        nrows = int(n/2) + 1

#    list_iter = 0
#    for i in range(nrows):
#        cols = st.columns(2)
#        with cols[0]:
#            item = st.session_state.list_of_annotations[list_iter]
#            t1 = item["annotation"]
#            t2 = item["x1"]
#            t3 = item["x2"]
#            t4 = item["y1"]
#            t5 = item["y2"]
#            t6 = item["attr"]
#            st.markdown("")
#            st.markdown(f"*Model Attribute:* {t6}")
#            st.markdown(f"*X-axis range* {t2} - {t3}")
#            st.markdown(f"*Y-axis range* {t4} - {t5}")
#            st.markdown(f":blue-background[Annotation]: {t1} ")
#            st.markdown("")
#            list_iter = list_iter + 1
#        with cols[1]:
#            if (list_iter == n or list_iter > n):
#                pass
#            else:
#                item = st.session_state.list_of_annotations[list_iter]
#                t1 = item["annotation"]
#                t2 = item["x1"]
#                t3 = item["x2"]
#                t4 = item["y1"]
#                t5 = item["y2"]
#                t6 = item["attr"]
#                st.markdown("")
#                st.markdown(f"*Model Attribute:* {t6}")
#                st.markdown(f"*X-axis range* {t2} - {t3}")
#                st.markdown(f"*Y-axis range* {t4} - {t5}")
#                st.markdown(f":blue-background[Annotation]: {t1} ")
#                st.markdown("")
#                list_iter = list_iter + 1

        
