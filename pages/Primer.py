import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    layout="centered"
)

@st.cache_data
def load_dummy_data(path):
    return pd.read_csv(path)

dummy_df = load_dummy_data("./data/expected_behavior_curves.csv")

st.header("Introduction to Likelihood Estimation")

st.write("This page will provide a short introduction to the likelihood estimation technique using more familiar examples in probability. ")

st.divider()

first_example = st.columns(2)
with first_example[0]:
    st.markdown("Consider the roll of a six-sided, fair dice.")
    st.markdown("With every roll, there is an equal chance of getting 1, 2, 3, 4, 5, or 6.")
    st.markdown("We can visualize the probability distribution of this phenomenon as shown in the plot (right).")
    st.markdown("Let us say you did not know if it is a fair dice.")
with first_example[1]:
    st.image("./images/uniform.jpg", caption = "Figure 1", width = None)

st.markdown("A loaded dice, for example, can be weighted on one side which causes some numbers to come up more often than others.")

st.markdown("However, if I did 1000 rolls of this dice, analyzed the data, and told you that the dice *still had a probability distribution as shown in Figure 1*, you can conclude that this is indeed a fair dice.")
st.divider()
second_example = st.columns(2)
with second_example[0]:
    st.markdown("Consider a second example - that of a normal distribution.")
    st.markdown("A normal distribution is a classic probability distribution that is bell-shaped and symmetrical around the mean value (see right). They are also interesting because they are governed by a rule which states:")
    st.markdown("_Approximately 68&percnt; of the data falls within one standard deviation of the mean_.")
with second_example[1]:
    st.image("./images/normal.jpg", caption = "Figure 2", width = None)

st.markdown("This means that, if you have to draw samples from a data that corresponds to the probability distribution in Figure 2, there is a 68&percnt; chance that it will fall within the range of (mean - 1sd, mean + 1sd) i.e., (0-1, 0+1) or (-1, 1)")

st.divider()

st.subheader("Just as the probability distribution tells us what kind of data we will deal with")
st.image("./images/exp1.jpg")
st.subheader("if we collect a large sample of data, we can tell something about its probability distribution.")
st.image("./images/exp2.jpg")
st.divider()

st.markdown("For example, **Perspective** has the following rubric for **Toxicity** detection")

st.markdown("- 0.0 - 0.30 corresponds to **Not Toxic**")
st.markdown("- 0.31 - 0.70 corresponds to **Hard to say if Toxic**")
st.markdown("- 0.71 - 1.00 corresponds to **Toxic**")
st.markdown("")
st.markdown("For a given set of comments if :green[Users] rated comments as :green[Not toxic, Hard to say, Toxic], and :violet[Perspective] scores the same comments from :violet[0.0 - 1.0] ...  What will perfect alignment will look like?")


fig = px.line(dummy_df, 
                x="Perspective_Toxicity", 
                y="Probability", 
                color = 'User_Rating',
                labels={
                        "Perspective_Toxicity": "Perspective Toxicity Score",
                        "Probability": "Probability of providing that User_Rating",
                        "User_Rating": "User_Rating"
                },
                title = "Expected Alignment between Model and User Judgements")

with st.expander("View it"):
    xyz = st.plotly_chart(fig, 
                      use_container_width = True)

st.divider()

st.markdown("In the next Section, you can run analyses to see such probability distributions.")
st.markdown("Since sexism is a binary variable (True/False), we will be running a _logistic regression analysis_ to generate the probability curves.")
st.markdown("You can play around with the variables and view different probability curves.")

