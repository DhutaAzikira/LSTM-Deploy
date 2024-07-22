import streamlit as st
import pandas as pd
import numpy as np

def get_tables():
    # Load the raw data CSV
    raw_data_csv = 'Jko.csv'  # Replace with your actual file name
    raw_df = pd.read_csv(raw_data_csv)
    raw_df['Date'] = pd.to_datetime(raw_df['Date'])
    raw_df = raw_df.sort_values(by='Date').tail(60)

    # Load the actual and predicted prices CSVs
    y_test_csv = 'Act.csv'  # Replace with your actual file name
    y_pred_csv = 'Pred.csv'  # Replace with your actual file name
    y_test_df = pd.read_csv(y_test_csv)
    y_pred_df = pd.read_csv(y_pred_csv)

    # Generate dates for the predicted comparison based on the last date from raw data
    last_date = raw_df['Date'].max()
    date_range = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
    comparison_df = pd.DataFrame({
        'Date': date_range,
        'Actual_Price': y_test_df['0'][:7],
        'Predicted_Price': y_pred_df['0'][:7]
    })

    # Calculate percentage difference
    comparison_df['Percentage_Difference'] = ((comparison_df['Predicted_Price'] - comparison_df['Actual_Price']) / comparison_df['Actual_Price']) * 100

    # Split the layout into two columns
    # Predict the next 7 days (dummy example, replace with your actual prediction logic)
    future_dates = pd.date_range(start=date_range[-1] + pd.Timedelta(days=1), periods=7)
    predicted_future_prices = y_pred_df['0'][7:14]  # Assuming you have future predictions
    future_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Future_Price': predicted_future_prices
    })

    # Split the layout into three columns
    col1, col2, col3 = st.columns(3)

    # Center-align content in all columns
    with col1:
        st.markdown("<h2 style='text-align: center;'>Bitcoin Prices for the Last 60 Days</h2>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>*this is static data</div>", unsafe_allow_html=True)
        st.dataframe(raw_df[['Date', 'BTC_Price']], height=1200, use_container_width=True)  # Adjust height to fit 6 rows approximately

    with col2:
        st.markdown("<h2 style='text-align: center;'>Comparison of Actual vs. Predicted Prices for the Next 7 Days</h2>", unsafe_allow_html=True)
        st.dataframe(comparison_df[['Date', 'Actual_Price', 'Predicted_Price', 'Percentage_Difference']], use_container_width=True)  # Horizontal scroll enabled by default
        st.line_chart(comparison_df.set_index('Date')[['Actual_Price', 'Predicted_Price']])  # Line chart for comparison
        st.bar_chart(comparison_df.set_index('Date')['Percentage_Difference'])  # Percentage difference bar chart

    with col3:
        st.markdown("<h2 style='text-align: center;'>Predicted Prices for the 7 Days Following the Last Date</h2>", unsafe_allow_html=True)
        st.dataframe(future_df, use_container_width=True)  # Horizontal scroll enabled by default
        st.line_chart(future_df.set_index('Date')['Predicted_Future_Price'])  # Line chart for future predictions


def main():
    st.set_page_config(
        page_title="LSTM Prediction Machine",
        page_icon=':smile:',
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("LSTM PREDICTION MACHINE")
    st.subheader("Made by @dhuta_azikira")
    st.write("A sophisticated LSTM Prediction machine forecasts daily Bitcoin prices with high accuracy, aiding investors in making informed decisions.")
    st.write("Its advanced algorithms analyze historical data to predict future price movements effectively. Investors rely on its insights to maximize their gains in the volatile cryptocurrency market.")
    st.divider()
    get_tables()
    



if __name__ == '__main__':
    main()



