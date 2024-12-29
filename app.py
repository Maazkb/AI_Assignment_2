import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests
import io

st.title('Transaction Analysis Dashboard')

url = 'https://raw.githubusercontent.com/Maazkb/AI_Assignment_2/refs/heads/main/Enhanced_Dummy_HBL_Data.xlsx'
response = requests.get(url)

if response.status_code == 200:
    data = pd.read_excel(io.BytesIO(response.content))
else:
    st.error("Failed to load the Excel file.")
    data = None

if data is not None:
    st.write(data.head())

  
    fig, ax = plt.subplots(figsize=(8, 6))
    data['Account Type'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3', ax=ax)
    ax.set_title('Account Type Distribution')
    ax.set_ylabel('')
    st.pyplot(fig)

   
    top_beneficiary_banks = (
        data.groupby(['Region', 'Transaction To'])['Credit']
        .sum()
        .reset_index()
        .sort_values(by='Credit', ascending=False)
    )
    top_5_banks = top_beneficiary_banks.groupby('Region').head(5)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.catplot(
        data=top_5_banks,
        x='Credit', y='Transaction To', hue='Region',
        kind='bar', height=6, aspect=2
    )
    ax.set_title('Top 5 Beneficiary Banks by Credit Transactions per Region')
    st.pyplot(fig)

    transaction_heatmap_data = data.groupby('Region')[['Credit', 'Debit']].sum()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(transaction_heatmap_data, annot=True, fmt='.0f', cmap='YlGnBu', ax=ax)
    ax.set_title('Geographic Heatmap of Transactions (Credit and Debit)')
    st.pyplot(fig)


    from scipy.stats import zscore

    data['Credit_Z'] = zscore(data['Credit'])
    data['Debit_Z'] = zscore(data['Debit'])

    credit_outliers = data[np.abs(data['Credit_Z']) > 3]
    debit_outliers = data[np.abs(data['Debit_Z']) > 3]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data.index, data['Credit'], label='Normal Credit Transactions', alpha=0.5)
    ax.scatter(credit_outliers.index, credit_outliers['Credit'], color='red', label='Credit Outliers')
    ax.set_title('Credit Transaction Anomalies')
    ax.set_xlabel('Index')
    ax.set_ylabel('Credit Amount')
    ax.legend()
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data.index, data['Debit'], label='Normal Debit Transactions', alpha=0.5)
    ax.scatter(debit_outliers.index, debit_outliers['Debit'], color='red', label='Debit Outliers')
    ax.set_title('Debit Transaction Anomalies')
    ax.set_xlabel('Index')
    ax.set_ylabel('Debit Amount')
    ax.legend()
    st.pyplot(fig)

    
    fig, ax = plt.subplots(figsize=(12, 6))
    credit_debit_data = data.melt(
        id_vars=['Account Type'], 
        value_vars=['Credit', 'Debit'], 
        var_name='Transaction Type', 
        value_name='Amount'
    )
    sns.boxplot(data=credit_debit_data, x='Account Type', y='Amount', hue='Transaction Type', ax=ax)
    ax.set_title('Comparative Analysis of Transaction Types by Account Type')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

   
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'])
        time_analysis_data = data.groupby('Date')[['Credit', 'Debit']].sum()

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(time_analysis_data.index, time_analysis_data['Credit'], label='Credit', marker='o')
        ax.plot(time_analysis_data.index, time_analysis_data['Debit'], label='Debit', marker='x')
        ax.set_title('Transaction Trends Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Transaction Amount')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    customer_insights_data = data.groupby('Account Type')[['Credit', 'Debit']].sum()
    customer_insights_data.plot(
        kind='bar', stacked=True, figsize=(10, 6), cmap='viridis', edgecolor='k', ax=ax
    )
    ax.set_title('Total Credit and Debit Amounts by Account Type')
    ax.set_xlabel('Account Type')
    ax.set_ylabel('Total Transaction Amount')
    ax.legend(title='Transaction Type')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
