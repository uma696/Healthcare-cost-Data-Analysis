#***********************
#****HEALTHCARE COST  INSURANCE DATA ANALYSIS*****
#Health related question
#What are the average BMI and blood pressure for different age groups?
#***************************************************************
#Insurance related question
#How do age, BMI, and blood pressure affect insurance charges?

import numpy as np
import pandas as pd #data manipulation and analysis
import matplotlib.pyplot as plt
import seaborn as sns
import csv
# Load dataset
data = pd.read_csv('Insurance_DataFile.csv')

#**ANALYSING DATA**#
#Display the number of rows and columns in the dataset-shape returns a tuple with the number of rows and columns in the dataset.
print("The number of rows and columns in the dataset", data.shape)
# Display the first 10 rows
print("\nThe first 10 rows:\n",data.head(10))
# Display the last 5 rows
print("\nThe last 5 rows:\n",data.tail())
#Display the data-type
print("\nThe Dataty3pes of Columns are:\n", data.dtypes)
#Display info ie concise summary about the data
print("\nConcise summary:\n",data.info())
#Display a summary of data
print("\nSummary of data:\n",data[['age', 'bmi', 'charges']].describe())

#**CLEANING DATA**#
#Data cleaning means fixing bad data ie Empty cells,Data in wrong format,Wrong data,Duplicates.
#Check for Missing Values: isnull or isna both can be used as both are same
print("\nthe total number of missing values for each column:\n", data.isnull().sum())
#Check for duplicates:
print("\nthe total number of duplicates rows in the dataframe:\n",data.duplicated().sum())
#Drop the missing values and the duplicates , inplace=Ture ->modify a DataFrame in place, without creating a new one:
# Drop rows with missing values
data.dropna(inplace=True)
# Drop duplicate rows
data.drop_duplicates(inplace=True)

# Display the cleaned dataset
print("\nCleaned Dataframe\n",data.head())
data.to_csv('Cleaned Dataframe.csv',index=False,sep=',', encoding='utf-8')
print("Cleaned dataframe written to 'Cleaned Dataframe.csv'")
#Check again for the missing values and duplicates
print("\nthe total number of missing values in the dataframe:\n",data.isnull().sum())
print("\nthe total number of duplicates in the dataframe:\n",data.duplicated().sum())
#Display a summary of data
print("\nSummary of data after data cleaning:\n",data[['age', 'bmi', 'charges']].describe())

#Data Transformation:
#Converting the specific columns to the correct dtype
data['PatientID'] = data['PatientID'].astype(int)
data['age'] = data['age'].astype(int)
#changing the way the Insurance cost data is displayed without altering the underlying values.
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#***********Analyzing the data for Descriptive analysis
#Univariate Analysis-deals with analyzing data within a single column or
# variable and is mostly used to describe data
#**********Visualizing Categorical Variables-
# visualizing the distribution of some of the categorical variables using bar plots.
# Bar plots for categorical variables
sns.countplot(x='sex', data=data)
plt.title("Number of clients per gender")
plt.show()

sns.countplot(x='smoker', data=data)
plt.title("Number of clients who are smokers")
plt.show()

sns.countplot(x='region', data=data)
plt.title("Number of clients per region")
plt.show()

#-------------------------------

#Exploratory Data Analysis :
#Find the highest age and their insurance charge
print("\nHighest age:\n",data.sort_values(by="age", ascending=False).head(10))

# Calculating correlation matrix
#Correlation provide valuable insights into how different variables are related.

# One-hot encoding for categorical columns
data_encoded = pd.get_dummies(data, columns=['sex', 'diabetic', 'smoker', 'region'])
# Convert boolean values to integers
for col in data_encoded.columns:
    if data_encoded[col].dtype == 'bool':
        data_encoded[col] = data_encoded[col].astype(int)
# Display the encoded DataFrame to verify columns
print("\nEncoded DataFrame:\n", data_encoded.head(20))
data_encoded.to_csv('encoded_df.csv',index=False,sep=';', encoding='utf-8')
print("Encoded dataframe written to 'encoded_df.csv'")
# Select only the numerical columns to find correlation as
# df.corr() method calculates the correlation between numerical columns
numerical_df = data_encoded.select_dtypes(include=['number'])

# Calculate the correlation matrix
correlation_matrix = numerical_df.corr()
print(correlation_matrix)
#Corr.Coefficient = 1->strong positive, -1->strong negative, 0->no correlation
correlation_matrix.to_csv('corr_matrix.csv',index=True,sep=' ', encoding='utf-8')
print("Correlation Matrix written to 'corr_matrix.csv'")
#*******************Heatmap*******************
#A heatmap is a graphical representation of data where individual values are represented as colors.
# It's particularly useful for displaying the correlation matrix.
#annot= If True, write the data value in each cell,cbar =Whether to draw a colorbar.
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix,annot=True,fmt='.2f', cmap='coolwarm', cbar=True,
            linewidth=.5,linecolor = "black",xticklabels = True,yticklabels = True)
plt.title('Correlation Matrix Heatmap')
plt.show()

#***************Health related question
#What are the average BMI and blood pressure for different age groups?
#Step1:Visualizing age distribution with Histogram - histogram to visualize the frequency of each age:
plt.hist(data['age'], bins=10)  # Adjust 'bins' as needed
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram-Age Distribution')
plt.show()
#Visualizing age distribution with Bar chart - Bar chart to show the count of each age:
age_counts = data['age'].value_counts().sort_index()
plt.bar(age_counts.index, age_counts.values)
plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Bar Chart- Age Distribution')
plt.show()
# Define age bins and labels
age_bins = [17, 29, 39, 49, 59, 69, 79, 89, 100]
age_labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']

# Create a new column 'age_group'
data['age_group'] = pd.cut(data['age'], bins=age_bins, labels=age_labels)

# Group by age group and calculate mean BMI and BP
cols_to_convert = ['bmi', 'blood-pressure']
for col in cols_to_convert:
    data[col] = pd.to_numeric(data[col], errors='coerce')
grouped_stats = data.groupby('age_group')[['bmi', 'blood-pressure']].mean().reset_index()
print(grouped_stats)

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(x='age_group', y='bmi', data=grouped_stats, color='blue', label='BMI')
sns.barplot(x='age_group', y='blood-pressure', data=grouped_stats, color='red', alpha=0.3, label='Blood Pressure')
plt.title('Average BMI and Blood Pressure Across Age Groups')
plt.xlabel('Age Group')
plt.ylabel('Average Value')
plt.legend()
plt.tight_layout()
plt.show()

#*******************#Insurance related question
#How do age, BMI, and blood pressure affect insurance charges?
plt.figure(figsize=(25, 7))

# Age vs Charges
plt.subplot(1, 3, 1)
sns.scatterplot(x='age', y='charges', data=data, alpha=0.5)
sns.lineplot(x='age', y='charges', data=data, color='red', label='Trend')
plt.title('Age vs Charges')

# BMI vs Charges
plt.subplot(1, 3, 2)
sns.scatterplot(x='bmi', y='charges', data=data, alpha=0.5)
sns.lineplot(x='bmi', y='charges', data=data, color='green',label='Trend')
plt.title('BMI vs Charges')

# Blood Pressure vs Charges
plt.subplot(1, 3, 3)
sns.scatterplot(x='blood-pressure', y='charges', data=data, alpha=0.5)
sns.lineplot(x='blood-pressure', y='charges', data=data, color='green',label='Trend')
plt.title('BP vs Charges')

plt.show()

print(data[['age', 'bmi', 'blood-pressure', 'charges']].corr())