# -*- coding: utf-8 -*-
"""Netflix Sotck Price Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dmxSOkb85B73tTqE-lckzT6cg8FhqGPr
"""

#Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

"""### **Data Gathering**"""

#Loading the Dataset
df = pd.read_csv('/content/NFLX.csv')
df.head()

df.info()

"""### **Data Cleansing**"""

#Checking for Missing Values
missing_values = df.isnull().sum()
missing_values

#Checking for Duplicates
duplicates = df.duplicated().sum()
duplicates

"""### **Exploratory Data Analysis (EDA)**"""

# Checking the distribution of numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
numeric_distribution = df[numeric_columns].hist(bins=20, figsize=(12, 8))

#Checking the distribution of categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns
categorical_distribution = df[categorical_columns].value_counts()
categorical_distribution

"""**Data Visualization**"""

numeric_df = df.select_dtypes(include=['number'])

corr_matrix = numeric_df.corr()
corr_matrix

# Correlation heatmap for numerical features
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Numeric Features')
plt.show()

# Convert the 'Date' column to datetime format for time series analysis
df["Date"] = pd.to_datetime(df["Date"])

# Set the 'Date' column as the index
df.set_index('Date', inplace=True)

# --- Feature Engineering ---
# Calculate Moving Averages (e.g., 50-day, 200-day)
df['50_MA'] = df['Close'].rolling(window=50).mean()
df['200_MA'] = df['Close'].rolling(window=200).mean()

# Calculate daily return percentage
df['Daily_Return'] = df['Close'].pct_change()

# --- Volatility Analysis ---
# Calculate 30-day rolling volatility
df['Volatility'] = df['Daily_Return'].rolling(window=30).std() * np.sqrt(30)

# --- Calculate max_price, max_date, min_price, min_date ---
max_price = df['Close'].max()
max_date = df['Close'].idxmax()

min_price = df['Close'].min()  # Find the minimum closing price
min_date = df['Close'].idxmin() # Find the date of the minimum closing price

# Plot Netflix Stock Price, Moving Averages, and Volume
plt.figure(figsize=(14, 8))
plt.plot(df['Close'], label='Netflix Stock Price', color='blue', alpha=0.6)
plt.plot(df['50_MA'], label='50-Day Moving Average', color='red', linestyle='--', alpha=0.7)
plt.plot(df['200_MA'], label='200-Day Moving Average', color='green', linestyle='--', alpha=0.7)
plt.title('Netflix Stock Price with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Stock Price (USD)')
plt.legend(loc='upper left')
plt.annotate(f'Highest: {max_price}', xy=(max_date, max_price), xytext=(max_date, max_price + 10),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='red')

plt.annotate(f'Lowest: {min_price}', xy=(min_date, min_price), xytext=(min_date, min_price - 10),
             arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='blue')
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot Netflix Stock Volatility
plt.figure(figsize=(12, 6))
plt.plot(df['Volatility'], label='30-Day Rolling Volatility', color='purple', alpha=0.6)
plt.title('Netflix Stock Price Volatility (30-Day Rolling)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend(loc='upper left')
plt.grid(True)

# Plot Netflix Daily Return Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Daily_Return'].dropna(), bins=100, kde=True, color='blue')
plt.title('Distribution of Netflix Daily Returns')
plt.xlabel('Daily Return')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()