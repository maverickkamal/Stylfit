# Stylfit: Your AI-Powered Personal Stylist 🧙‍♀️

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stylfit-team.streamlit.app/) 
[![GitHub stars](https://img.shields.io/github/stars/maverickkamal/Stylfit.svg?style=social)](https://github.com/maverickkamal/Stylfit)

**Don't know what to wear? Stylfit's got you covered!**

Stylfit is a revolutionary AI-powered personal stylist app that takes the guesswork out of getting dressed.  Built with Google Gemini AI, Stylfit analyzes real-time weather data, considers your personal style preferences, and even searches the web for style trends to provide you with smart and stylish outfit recommendations.

## Demo

Check out a live demo of Stylfit here: [https://stylfit-team.streamlit.app/](https://stylfit-team.streamlit.app/) 

**Love Stylfit? Give us a star on GitHub!** ✨ [https://github.com/maverickkamal/Stylfit](https://github.com/maverickkamal/Stylfit)

## Features

* **Real-time Weather Integration:** Stylfit checks the weather in your city to make sure your outfit is appropriate for the current conditions.
* **Personalized Style Recommendations:** Stylfit learns your style preferences over time to provide you with increasingly tailored suggestions.
* **Style Vibe Selection:** Choose from a range of styles, from casual to formal, to get outfit recommendations that match your mood or the occasion.
* **Web Search for Trends:**  Stylfit can browse the web for trending styles and suggest new clothing items to add to your wardrobe.
* **Easy-to-Use Chat Interface:** Simply type in your request and Stylfit will respond with helpful and fashionable suggestions.

## How it Works

1. **Tell Stylfit your city:** This allows the app to access real-time weather data.
2. **Choose a style vibe:** Select from a list of options like casual, formal, streetwear, etc.
3. **Stylfit provides recommendations:** Get instant outfit suggestions tailored to your preferences and the weather.
4. **Feedback and Refinement:** Stylfit learns from your choices, providing even better recommendations over time.

## Technologies Used

* **Google Gemini AI:** The powerful AI model that drives Stylfit's intelligent outfit suggestions.
* **Streamlit:**  A user-friendly Python framework for building interactive web apps.
* **Tavily API:** Used for searching the web for style trends and outfit ideas.
* **WeatherAPI:**  Provides real-time weather data.

## Getting Started

**Prerequisites:**

* Python 3.11.6 
* A Google Gemini API key
* A Tavily API key
* A WeatherAPI key

**Installation:**

1. Clone the repository: `git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git`
2. Install the required packages: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add your API keys:
GOOGLE_AI_API_KEY=YOUR_GOOGLE_AI_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
WEATHER_API_KEY=YOUR_WEATHER_API_KEY


**Running the App:**

1. Navigate to the project directory in your terminal.
2. Run the following command: `streamlit run main.py`
3. Open your browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

## Contributing

Contributions are welcome! 

## License

This project is licensed under the MIT License.
