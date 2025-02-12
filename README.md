# Data Quality Check Tool

## Overview
This Streamlit-based application allows users to upload a CSV file and perform various data quality checks, including:
- Checking for null values
- Validating date formats
- Detecting primary key duplicate values
- Identifying non-numerical values in numerical columns
- Finding negative numbers in numerical columns

## Installation
To set up the application, install the required dependencies:
```sh
pip install -r requirements.txt
```

## Usage
1. Run the application using the following command:
```sh
streamlit run app.py
```
2. Upload a CSV file through the web interface.
3. Select the relevant columns for validation (date, primary key, numerical columns).
4. Click the "Run Data Quality Checks" button to generate a report.

## Requirements
- Python 3.x
- Streamlit
- Pandas
- NumPy

## Features
- Interactive file upload
- Customizable column selection
- Detailed data quality report
- Easy-to-use UI built with Streamlit

## License
This project is open-source and available under the MIT License.

## Author
[NG]