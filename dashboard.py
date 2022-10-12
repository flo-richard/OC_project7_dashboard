import pandas as pd
import streamlit as st
import requests
import numpy as np
import lime
import matplotlib.pyplot as plt
from datetime import date


def request_prediction(model_url, payload):
    response = requests.post(model_url, json=payload)
    
    if response.status_code != 200:
        raise Exception(
            'Request failed with status ', response.status_code, '\n', response.text
        )
    return response.json()

def NumberOfDays(date1):
    return (date.today() - date1).days

URL_online = "https://scoring-oc7.herokuapp.com/getPrediction"

def main():

    st.title('Credit Prediction')

    st.write('Please file this form')

    with st.form('credit_form'):

        
            #GENERAL INFO
        st.write('General information')

        #Gender code
        gender = st.selectbox(
            label='Gender of the client',
            options=('Male', 'Female')
        )
        gender_code = 'M' if gender == 'Male' else 'F'

        #Date of birth
        st.write('Date of Birth')
        c1, c2, c3 = st.columns(3)        
        with c1:
            day_birth = st.number_input(
                label='Day of birth',
                min_value=1,
                max_value=31
            )
        with c2:
            month_birth = st.number_input(
                label='Month of birth (number)',
                min_value=1,
                max_value=12
            )
        with c3:
            year_birth = st.number_input(
                label='Year of birth',
                min_value=1900
            )
        date_birth = date(int(year_birth), int(month_birth), int(day_birth))     
        number_days_birth = -NumberOfDays(date_birth)
        #number_days_birth = birthday

        #email and phone
        email = st.selectbox(
            label='Did the client provide an email address?',
            options=('Yes', 'No')
        )
        flag_email = 1 if email == 'Yes' else 0

        phone = st.selectbox(
            label='Did the client provide a phone number?',
            options=('Yes', 'No')
        )
        flag_phone = 1 if phone == 'Yes' else 0


        #Family
        family_status = st.selectbox(
            label='Family status of the client',
            options=('Single / not married', 'Married', 'Civil marriage', 'Widow', 'Separated', 'Unknown')
        )

        family_members_count = st.number_input(
            label='Number of family members (Spouse, children) of the client',
            min_value=0
        )

        children_count_select = st.selectbox(
            label='Number of children of the client',
            options=('1', '2', '3', '4', '5+')
        )
        children_count = int(children_count_select) if children_count_select in ['1', '2', '3', '4'] else 5

        #Flag own car
        own_car = st.selectbox(
            label='Does the client own a car?',
            options=('Yes', 'No')
        )
        flag_own_car = 'Y' if own_car == 'Yes' else 'N'

        #Realty
        own_realty = st.selectbox(
            label='Does the client own a house/appartment/realty of any kind?',
            options=('Yes', 'No')
        )
        flag_own_realty = 'Y' if own_car == 'Yes' else 'N'

        housing_type = st.selectbox(
            label='What kind of housing does the client live in?',
            options=('House / apartment', 'Rented apartment', 'With parents', 'Municipal apartment', 'Office apartment', 'Co-op apartment')
        )


            # EDUCATION AND EMPLOYMENT
        st.write('Education and Work')

        education_type = st.selectbox(
            label='Education level',
            options=('Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary', 'Academic degree')
        )

        organization_type = st.selectbox(
            label='Organization type',
            options=(
                'Self-employed', 'School', 'University', 'Kindergarten',
                'Government', 'Security Ministries', 'Legal Services', 'Postal',
                'Military', 'Police', 'Security', 'Services', 
                'Religion', 'Medicine', 'Emergency', 'Electricity',
                'Construction', 'Realtor', 'Housing', 'Hotel',
                'Bank', 'Insurance', 'Mobile', 'Telecom',
                'Culture', 'Advertising', 'Agriculture', 'Restaurant',
                'Cleaning', 'Business Entity Type 1', 'Business Entity Type 2', 'Business Entity Type 3',
                'Transport: type 1', 'Transport: type 2', 'Transport: type 3', 'Transport: type 4',
                'Trade: type 1', 'Trade: type 2', 'Trade: type 3', 'Trade: type 4',
                'Trade: type 5', 'Trade: type 6', 'Trade: type 7', 'Industry: type 1',
                'Industry: type 2', 'Industry: type 3', 'Industry: type 4', 'Industry: type 5',
                'Industry: type 6', 'Industry: type 7', 'Industry: type 8', 'Industry: type 9',
                'Industry: type 10', 'Industry: type 11', 'Industry: type 12', 'Industry: type 13',
                'Other'
            )
        )

        #Income
        annual_income = st.number_input(
            label='Annual income',
            min_value=1
        )

        #Income type
        income_type = st.selectbox(
            label='Income type',
            options=('Working', 'State servant', 'Commercial associate', 'Pensioner',
                    'Unemployed', 'Student', 'Businessman', 'Maternity leave')
        )

        

        #Days employed
        st.write('Date of Employment')       
        c4, c5, c6 = st.columns(3)       
        with c4:
            day_emp = st.number_input(
                label='Day',
                min_value=1,
                max_value=31
            )
        with c5:
            month_emp = st.number_input(
                label='Month (number)',
                min_value=1,
                max_value=12
            )
        with c6:
            year_emp = st.number_input(
                label='Year',
                min_value=1900
            )
        date_employment = date(int(year_emp), int(month_emp), int(day_emp))        
        days_employed = NumberOfDays(date_employment)
        #days_employed = date_employment

            #CONTRACT
        st.write('Contract information')
        
        #Contract type
        contract_type = st.selectbox(
            label='Contract type',
            options=('Cash loans', 'Revolving loans')
        )

        #Credit amount
        amount_credit = st.number_input(
            label='Requested credit amout',
            min_value=1
        )

        #Goods price
        goods_price = st.number_input(
            label='Price of the good(s) the client wishes to buy',
            min_value=1
        )

        #Annuity
        years_payoff = st.number_input(
            label='Duration of the payoff (years)',
            min_value=1
        )
        annuity = amount_credit / years_payoff

        submitted = st.form_submit_button('Submit')

        if submitted:

            with st.spinner('Loading...'):
                payload = {
                    'NAME_CONTRACT_TYPE': contract_type,
                    'CODE_GENDER': gender_code,
                    'FLAG_OWN_CAR': flag_own_car,
                    'FLAG_OWN_REALTY': flag_own_realty,
                    'CNT_CHILDREN': children_count,
                    'AMT_INCOME_TOTAL': annual_income,
                    'AMT_CREDIT': amount_credit,
                    'AMT_ANNUITY': annuity,
                    'AMT_GOODS_PRICE': goods_price,
                    'NAME_INCOME_TYPE': income_type,
                    'NAME_EDUCATION_TYPE': education_type,
                    'NAME_FAMILY_STATUS': family_status,
                    'NAME_HOUSING_TYPE': housing_type,
                    'DAYS_BIRTH': number_days_birth,
                    'DAYS_EMPLOYED': days_employed,
                    'FLAG_MOBIL': flag_phone,
                    'FLAG_EMAIL': flag_email,
                    'CNT_FAM_MEMBERS': family_members_count,
                    'ORGANIZATION_TYPE': organization_type
                }

                response = request_prediction(URL_online, payload)

                st.write(response['Prediction'])
                if response['Prediction'] == 1:
                    st.write('Credit Granted')
                else:
                    st.write('Credit denied')

                st.write('Details')

                feature_list = [i for i in response['User info']]
                names = []
                colors = []

                for i in response['Explainer list']:
                    names.append(i[0])

                for i in range(len(result['Explainer map']['Feature_idx'])):
                    colors.append('green' if result['Explainer map']['Scaled_value'][i] > 0 else 'red')
                values = [i for i in result['Explainer map']['Scaled_value']]


                names.reverse()
                values.reverse()
                colors.reverse()

                plt.barh(range(len(names)), values, tick_label=names, color=colors)
                plt.title('Most impactful parameters')

                plt.grid()
                st.pyplot()

                st.write('Details')

                j=1
                fig = plt.figure(figsize=(12, 7))
                for i in response['Distributions']:
                    ax = fig.add_subplot(2, 3, j)
                    h = ax.hist(response['Distributions'][i], bins=40)
                    plt.axvline(response['User info'][i], c='k')
                    ax.set_title(i)
                    j += 1

                st.pyplot(fig)




            st.success('Completed')    











        
if __name__ == '__main__':
    main()