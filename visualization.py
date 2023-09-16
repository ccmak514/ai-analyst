import streamlit as st
from lida import Manager, TextGenerationConfig, llm
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

# API Key
# import constant
# openai_api_key = constant.APIKEY
st.title("AI Analyst: EDA by Automatic Visualization")

if 'temp_csv' not in st.session_state:
    st.session_state['temp_csv'] = []

# Introduction
st.markdown('''
# Introduction:
Welcome to the **:red[AI Analyst: EDA by Automatic Visualization]**. The AI can help you do the **:red[Exploratory Data Analysis (EDA) automatically]** by following the guidelines below:

1. Upload a CSV file to preview and display a summary (numerical and categorical).
2. Choose the number of charts you want.
3. Click the button to do **:red[EDA through visualization]** by AI automatically.
4. The **:red[reasons]** and **:red[goals]** behind the visualization will be displayed.
5. The **:red[code]** for plotting the charts can be found in the **:red[code tab]**.
''')

st.divider()

with st.sidebar:
    st.markdown('''
    # About the AI Analyst:
    The objective of this app is to provide assistance in **analyzing CSV data and answering questions according to the provided PDF file.** 
    This application consists of two main functions:

    **1. EDA by Automatic Visualization**
    
    **2. Chat with your PDF**

    AI Analyst is written by **Isaac Mak**. 
    - [LinkedIn](https://www.linkedin.com/in/isaac-ccmak/)
    - [Source Code](https://github.com/ccmak514/ai-analyst)
    - [GitHub](https://github.com/ccmak514)
    ''')
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    st.title("Upload a CSV File")
    csv_file = st.file_uploader(" ", type=["csv"])


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
    num_chart = st.slider('Number of Charts', 1, 10)
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
