import streamlit as st
from lida import Manager, TextGenerationConfig, llm
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

# API Key
import constant
openai_api_key = constant.APIKEY

st.title("AI Analyst: EDA by Automatic Visualization")

if 'temp_csv' not in st.session_state:
    st.session_state['temp_csv'] = []

# Introduction
st.markdown('''
#### Introduction:
- Upload a csv file, preview and summary (numerical and categorical) are displayed.
- Click the button, exploratory data analysis(EDA) by visualization will be donw by AI.
- The reasons and goals behind the visualization will be displayed.
- The code for plotting the chart can be found in the code tab.
- You may choose the number of visualization you want by using the slider.
''')

st.divider()

with st.sidebar:
    st.title("Upload a CSV File")
    csv_file = st.file_uploader(" ", type=["csv"])
    st.markdown('''
    ## About the author
    This app is written by **Isaac Mak**
    - [LinkedIn](https://www.linkedin.com/in/isaac-ccmak/)
    - [GitHub](https://github.com/ccmak514)
    ''')


def main():
    if csv_file:

        data = pd.read_csv(csv_file)
        st.markdown("Data Preview: ")
        st.dataframe(data.head())
        st.markdown("Summary (Numerical): ")
        st.dataframe(data.describe())
        st.markdown("Summary (Categorical): ")
        st.dataframe(data.describe(include="O").astype(str))
        st.divider()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            data.to_csv(temp_file.name, index=False)
            temp_file_path = temp_file.name
        st.session_state['temp_csv'].append(temp_file_path)
        # st.write(temp_file_path)

    ############# EDA #############
    num_chart = st.slider('Number of Visualization', 1, 10)
    if st.button("Automatic Visualization"):

        lida = Manager(text_gen=llm("openai", api_key=openai_api_key))
        # Configuration for summary and goals
        textgen_config = TextGenerationConfig(
            n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
        summary = lida.summarize(
            temp_file_path, summary_method="default", textgen_config=textgen_config)
        goals = lida.goals(summary, n=num_chart, textgen_config=textgen_config)

        for i in range(len(goals)):
            # Underscore is added automatically by the summarizer
            # Use the temp csv version
            data = pd.read_csv(temp_file_path)
            st.markdown("Chart " + str(i+1))
            st.markdown(":red[Goal]: " + goals[i].question)
            st.markdown(":red[Chart]: " + goals[i].visualization)
            st.markdown(":red[Reason]: " + goals[i].rationale)
            library = "matplotlib"
            # Configuration for visualization
            # Use a better model for visualization
            textgen_config = TextGenerationConfig(
                n=1, temperature=0.2, model="gpt-3.5-turbo", use_cache=True)
            charts = lida.visualize(
                summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)
            ########## Bug ############
            # The lida.visualize may not be able to visualize the chart
            # and return a charts that is an empty list
            my_code = charts[0].code
            tab1, tab2 = st.tabs(["chart", "code"])
            with tab1:
                exec(my_code + "\nst.pyplot(chart)")
            with tab2:
                st.code(my_code)
            st.divider()

        # After plotting, remove the temp csv and reset it
        for temp_csv_path in st.session_state['temp_csv']:
            os.remove(temp_csv_path)
        st.session_state['temp_csv'] = []
###########################################


if __name__ == "__main__":
    main()
