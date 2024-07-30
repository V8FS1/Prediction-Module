# Flight Price Prediction
This project is a comprehensive flight price prediction system using machine learning models. It processes and analyzes flight data to predict flight prices based on various features such as flight duration, departure and arrival times, stops, and more. The project includes data preprocessing, feature engineering, model training, and a Streamlit web application for user interaction.

## Project Overview
The workflow involves the following steps:

### 1. Data Loading and Cleaning
* Load datasets for business and economy class flights.
* Merge datasets and clean data by handling missing values, duplicates, and inconsistencies.
* Feature engineering to create meaningful features like flight codes and transformed duration.

### 2. Data Exploration and Visualization
* Analyze and visualize data to understand distributions and relationships between variables.
* Use plots to explore factors influencing flight prices, such as duration, class, and departure/arrival times.

### 3. Feature Engineering
* Convert categorical variables to numerical features using one-hot encoding.
* Process and transform time and date features to make them suitable for modeling.

### 4. Model Training
* Train and evaluate multiple regression models, including:
* Linear Regression
* Gradient Boosting Regressor
* Decision Tree Regressor
* Random Forest Regressor
* Extra Tree Regressor
* Save the best-performing model using pickle.

### 5. Web Application
* Implement a Streamlit web application to allow users to input flight details and predict prices.
* The application features radio buttons and text inputs for user interaction and data submission.

## Requirements
To run this project, you need the following Python packages:
* numpy
* pandas
* seaborn
* matplotlib
* scikit-learn
* streamlit
* plotly
* pickle
* re
* datetime
* PIL
### Install the required packages using pip:
``` pip install numpy pandas seaborn matplotlib scikit-learn streamlit plotly pillow ```

## Usage
### 1. Run the Streamlit Application
Navigate to the project directory and run the Streamlit app:
``` streamlit run app.py ```

### 2. Input Flight Details

Use the web interface to input flight details:
* Select airline, source city, destination city, departure and arrival times.
* Specify the flight class and number of stops.
* Enter the date of booking.

### 3. Predict and View Results
* Click the "Predict" button to get the estimated flight price. The predicted price will be displayed in both INR and USD.
