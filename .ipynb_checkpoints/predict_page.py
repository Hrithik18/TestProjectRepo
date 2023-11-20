import pandas as pd
import streamlit as st
import pickle
import numpy as np
import plotly.express as px

def load_model():
   with open('classifier.pkl', 'rb') as f:
    clf = pickle.load(f)
    return clf
   
clf =load_model()

import streamlit as st

def show_predict_page():
    st.title("Risk Assessment Prediction")

    st.write("""### We need some information to predict risk assessment""")

    current_age = st.number_input('Current Age')
    # st.write('Current age is ', current_age)

    retired_age = st.number_input('RetiredAge')
    # st.write('RetiredAge is ', retired_age)

    annual_income = st.number_input('AnnualIncome')
    # st.write('AnnualIncome is ', annual_income)

    annual_spending = st.number_input('AnnualSpending')
    # st.write('AnnualSpending is ', annual_spending)

    if st.button('Generate Prediction'):
    # Make predictions on user data
        new_data = pd.DataFrame({
        'Current Age': [current_age],
        'Retired Age': [retired_age],
        'Annual Income': [annual_income],
        'Annual Spending': [annual_spending]
    })
        new_X = new_data[['Current Age', 'Retired Age', 'Annual Income', 'Annual Spending']]
        new_y_pred = clf.predict(new_X)
        # Generate retirement savings report
        report = generate_report(current_age, retired_age, annual_income, annual_spending, new_y_pred[0])
        # Display the retirement savings report
        st.markdown(report)
        # Create visualization diagrams
        color_discrete_map = {
        ('25', '100000'): 'blue',
        ('30', '500000'): 'green',
        ('25', '1000000'): 'teal',
        ('35', '100000'): 'orange',
        ('36', '500000'): 'purple',
        ('40', '1000000'): 'magenta',
        ('65', '100000'): 'red',
        ('73', '500000'): 'brown',
        ('75', '1000000'): 'maroon',
    }
        spending_vs_income_chart = px.bar(
            new_data, x='Retired Age', y='Annual Spending', color='Annual Income', orientation='v', color_discrete_map=color_discrete_map
        )
        st.plotly_chart(spending_vs_income_chart)



    # Display the predicted risk level
        st.success(f"Predicted Risk: {new_y_pred[0]}")
    else:
        st.info('Please enter your information and click the "Generate Prediction" button to see your predicted risk level.')

# Create the Streamlit app
st.title("Investment Risk Assessment")

# Call the show_predict_page function
def generate_report(current_age, retired_age, annual_income, annual_spending, risk):
    # Calculate the number of years until retirement
    years_until_retirement = retired_age - current_age

    # Calculate the total savings required
    total_savings_required = (annual_spending * years_until_retirement)

    # Calculate the annual savings required
    annual_savings_required = total_savings_required / years_until_retirement

    # Calculate the amount to save each month
    monthly_savings_required = annual_savings_required / 12

    # Calculate the recommended investment amount based on risk
    if risk == "low":
        recommended_investment_amount = annual_savings_required * 0.3
    elif risk == "medium":
        recommended_investment_amount = annual_savings_required * 0.5
    else:
        recommended_investment_amount = annual_savings_required * 0.7

    # Generate a report with Markdown formatting and styling
    report = """
    **Retirement Savings Report**

    **Personal Information**

    * Current Age: {} years
    * Retired Age: {} years
    * Annual Income: ${:,.2f}
    * Annual Spending: ${:,.2f}
    * Risk Tolerance: {}

    **Financial Projections**

    * Years Until Retirement: {} years
    * Total Savings Required: ${:,.2f}
    * Annual Savings Required: ${:,.2f}
    * Monthly Savings Required: ${:,.2f}

    **Investment Recommendations**

    * Recommended Investment Amount: ${:,.2f}

    **Recommendations**

    To achieve your retirement savings goals, consider the following recommendations:

    * **Start saving early.** The earlier you start saving, the more time your money has to grow.
    * **Contribute regularly.** Even small contributions can add up over time.
    * **Invest wisely.** Choose investments that are appropriate for your risk tolerance and time horizon.
    * **Seek professional advice.** If you need help with your retirement planning, consider consulting with a financial advisor.

    **Remember, these are just projections. Actual results may vary depending on a number of factors, including market conditions, investment performance, and personal circumstances.**
    """.format(current_age, retired_age, annual_income, annual_spending, risk, years_until_retirement, total_savings_required, annual_savings_required, monthly_savings_required, recommended_investment_amount)
    return report
