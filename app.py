import streamlit as st
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import zscore

st.title('Transaction Analysis Dashboard')

url = 'https://raw.githubusercontent.com/Maazkb/AI_Assignment_2/refs/heads/main/Enhanced_Dummy_HBL_Data.xlsx'
response = requests.get(url)

if response.status_code == 200:
    data = pd.read_excel(io.BytesIO(response.content))
else:
    st.error("Failed to load the Excel file.")
    data = None

if data is not None:
    
    data.isnull().sum()
  
    sdata.columns


    plt.figure(figsize=(8, 6))
    data['Account Type'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3')
    plt.title('Account Type Distribution')
    plt.ylabel('')
    st.pyplot(plt)

    top_beneficiary_banks = (
        data.groupby(['Region', 'Transaction To'])['Credit']
        .sum()
        .reset_index()
        .sort_values(by='Credit', ascending=False)
    )

    top_5_banks = top_beneficiary_banks.groupby('Region').head(5)
    sns.catplot(
        data=top_5_banks,
        x='Credit', y='Transaction To', hue='Region',
        kind='bar', height=6, aspect=2
    )
    plt.title('Top 5 Beneficiary Banks by Credit Transactions per Region')
    st.pyplot(plt)

    transaction_heatmap_data = data.groupby('Region')[['Credit', 'Debit']].sum()
    sns.heatmap(transaction_heatmap_data, annot=True, fmt='.0f', cmap='YlGnBu')
    plt.title('Geographic Heatmap of Transactions (Credit and Debit)')
    st.pyplot(plt)

    data['Credit_Z'] = zscore(data['Credit'])
    data['Debit_Z'] = zscore(data['Debit'])

    credit_outliers = data[np.abs(data['Credit_Z']) > 3]
    debit_outliers = data[np.abs(data['Debit_Z']) > 3]

    plt.figure(figsize=(10, 6))
    plt.scatter(data.index, data['Credit'], label='Normal Credit Transactions', alpha=0.5)
    plt.scatter(credit_outliers.index, credit_outliers['Credit'], color='red', label='Credit Outliers')
    plt.title('Credit Transaction Anomalies')
    plt.xlabel('Index')
    plt.ylabel('Credit Amount')
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(10, 6))
    plt.scatter(data.index, data['Debit'], label='Normal Debit Transactions', alpha=0.5)
    plt.scatter(debit_outliers.index, debit_outliers['Debit'], color='red', label='Debit Outliers')
    plt.title('Debit Transaction Anomalies')
    plt.xlabel('Index')
    plt.ylabel('Debit Amount')
    plt.legend()
    st.pyplot(plt)

    plt.figure(figsize=(12, 6))
    credit_debit_data = data.melt(
        id_vars=['Account Type'], 
        value_vars=['Credit', 'Debit'], 
        var_name='Transaction Type', 
        value_name='Amount'
    )
    sns.boxplot(data=credit_debit_data, x='Account Type', y='Amount', hue='Transaction Type')
    plt.title('Comparative Analysis of Transaction Types by Account Type')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        time_analysis_data = data.groupby('Date')[['Credit', 'Debit']].sum()

        plt.figure(figsize=(14, 6))
        plt.plot(time_analysis_data.index, time_analysis_data['Credit'], label='Credit', marker='o')
        plt.plot(time_analysis_data.index, time_analysis_data['Debit'], label='Debit', marker='x')
        plt.title('Transaction Trends Over Time')
        plt.xlabel('Date')
        plt.ylabel('Transaction Amount')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

    customer_insights_data = data.groupby('Account Type')[['Credit', 'Debit']].sum()
    customer_insights_data.plot(
        kind='bar', stacked=True, figsize=(10, 6), cmap='viridis', edgecolor='k'
    )
    plt.title('Total Credit and Debit Amounts by Account Type')
    plt.xlabel('Account Type')
    plt.ylabel('Total Transaction Amount')
    plt.legend(title='Transaction Type')
    plt.xticks(rotation=45)
    st.pyplot(plt)
