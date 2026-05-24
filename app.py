import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

API_KEY = "5b6eefa98cc33b0d547a54b0dda17f94"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if str(data.get("cod")) != "200":
            return None

        return {
            "City": city,
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Pressure": data["main"]["pressure"],
            "Wind Speed": data["wind"]["speed"]
        }

    except:
        return None


st.title("🌦️ Weather Data Analyzer")

st.write("Enter multiple cities to analyze real-time weather data")

city_input = st.text_input("Enter cities (comma-separated)", "Delhi, Mumbai, Bangalore")

if st.button("Analyze Weather"):

    cities = [city.strip().title() for city in city_input.split(",")]

    weather_list = []

    for city in cities:
        result = get_weather(city)
        if result:
            weather_list.append(result)
        else:
            st.warning(f"⚠️ Could not fetch data for {city}")

    df = pd.DataFrame(weather_list)

    if df.empty:
        st.error("❌ No data available. Check API key or city names.")
    
    else:
        st.subheader("📊 Weather Data")
        st.dataframe(df)

        hottest = df.loc[df['Temperature'].idxmax()]
        humid = df.loc[df['Humidity'].idxmax()]

        st.subheader("🔥 Insights")
        st.write(f"🔥 Hottest City: **{hottest['City']}**")
        st.write(f"💧 Most Humid City: **{humid['City']}**")

        st.subheader("📈 Visualizations")

        fig1, ax1 = plt.subplots()
        sns.barplot(x='City', y='Temperature', data=df, ax=ax1, color="#C8054C")
        ax1.set_title("Temperature Comparison")
        for bars in ax1.containers:
            ax1.bar_label(bars)
        st.pyplot(fig1)
        
        fig2, ax2 = plt.subplots()
        sns.barplot(x='City', y='Humidity', data=df, ax=ax2,color="#02FFFB")
        ax2.set_title("Humidity Comparison")
        for bars in ax2.containers:
            ax2.bar_label(bars)
        st.pyplot(fig2)

        st.subheader("🥧 Humidity Distribution")

        st.subheader("🥧 Pie Chart Comparison")

        # Create two columns
        col1, col2 = st.columns(2)

        with col1:
            fig3, ax3 = plt.subplots()
            
            max_index = df['Temperature'].idxmax()
            explode = [0.1 if i == max_index else 0 for i in range(len(df))]
            ax3.pie(
                df['Temperature'],
                labels=df['City'],
                autopct='%1.1f%%',
                startangle=90,
                shadow=True,
                explode=explode
            )

            ax3.set_title("Temperature Distribution")
            st.pyplot(fig3)


        with col2:
            fig4, ax4 = plt.subplots()

            # Highlight most humid city
            max_index = df['Humidity'].idxmax()
            explode = [0.1 if i == max_index else 0 for i in range(len(df))]

            ax4.pie(
                df['Humidity'],
                labels=df['City'],
                autopct='%1.1f%%',
                startangle=90,
                explode=explode,
                shadow=True
            )

            ax4.set_title("Humidity Distribution (Highlighted)")
            st.pyplot(fig4)

        # Heatmap
        fig5, ax5 = plt.subplots()
        sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax5,cmap="icefire")
        ax5.set_title("Correlation Heatmap")
        st.pyplot(fig5)