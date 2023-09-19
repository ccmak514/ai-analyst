# AI Analyst (Chat with your PDF & EDA by Automatic Visualization)
AI Analyst is written by **Isaac Mak**
- [LinkedIn](https://www.linkedin.com/in/isaac-ccmak/)
- [Source Code](https://github.com/ccmak514/ai-analyst)
- [GitHub](https://github.com/ccmak514)
- [Try the Demo!!!](https://isaac-mak-ai-ana-lyst.streamlit.app/)

The objective of this project is to assist analysts in answering questions according to the uploaded PDF file and analyzing CSV data.
This application consists of two main functions:

**1. Chat with your PDF**

**2. EDA by Automatic Visualization**

**Try the Demo:**
https://isaac-mak-ai-ana-lyst.streamlit.app/

## 1. Chat with your PDF

The **AI Analyst: Chat with your PDF** can help answer your questions **based on the provided PDF file** by following the guidelines below:

0. Enter the OpenAI API Key
1. Upload a PDF file.
2. Ask any questions about the PDF file after loading.
3. Answer **based on the PDF file** will be displayed.
4. The answers will depend on the **previous chat history**.

### Testing PDF File: [Royal Bank of Canada Annual Report 2022](https://www.rbc.com/investor-relations/_assets-custom/pdf/ar_2022_e.pdf)
The **235-page Royal Bank of Canada Annual Report 2022** is used for testing. Questions about the report are asked:
1. What bank is this report for?
2. Introduce this report.
3. What is the total revenue in 2022?
4. How is the financial performance of the bank?
5. What is the total revenue in 2021?

The **AI Analyst: Chat with your PDF** can answer each question according to the content of the annual report within 10-15 seconds.

### Demo:
![chatbot_gif1](https://github.com/ccmak514/ai-analyst/assets/101066418/b3b6a6cc-0609-4d3c-b88b-0696d77c5469)

![chatbot_gif2](https://github.com/ccmak514/ai-analyst/assets/101066418/2df3e59b-eb13-4b50-8746-b05484e67278)

## 2. EDA by Automatic Visualization

The AI Analyst: EDA by Automatic Visualization can help you do the **Exploratory Data Analysis (EDA) automatically** by following the guidelines below:

0. Enter the OpenAI API Key
1. Upload a CSV file to preview and display a summary (numerical and categorical).
2. Choose the number of visualizations you want.
3. Click the button to do **EDA through visualization** by AI automatically.
4. The **reasons** and **goals** behind the visualizations will be displayed.
5. The **code** for plotting the charts can be found in the **code tab**.

### Testing CSV File: [Home Loan Approval](https://www.kaggle.com/datasets/rishikeshkonapure/home-loan-approval?select=loan_sanction_train.csv)
The **615-row CSV file of Home Loan Approval** is used for the testing. 

### Demo:
![visualization_gif1](https://github.com/ccmak514/ai-analyst/assets/101066418/34a7a679-7320-4ee1-8087-d3a65f1e395c)

![visualization_gif2](https://github.com/ccmak514/ai-analyst/assets/101066418/49d78e2a-ad84-4482-870b-96d24da56e80)

## Run the Code Locally
1. `python3 -m venv ./venv/ai_analyst/` - Create a virtual environment
2. `source ./venv/ai_analyst/bin/activate` - Activate it (it is for Mac)
3. `pip3 install -r requirements.txt` - install the packages into the virtual environment
4. `streamlit run chatbot.py`

