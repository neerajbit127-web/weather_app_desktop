import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
from dotenv import load_dotenv

load_dotenv()




class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("City Label")
        self.city_input.setObjectName("City Input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
                            QLabel, QPushButton{
                           font-family: calibri;
                           }
                           QLabel#city_label{
                              font-size: 40px;
                               font-style:italic;
                           }
                           QLineEdit#city_input{
                               font-size: 40px;
                           }
                           QPushButton#get_weather_button{
                                  font-size: 30px;
                                  font-weight:bold;
                           }
                           QLabel#temperature_label{
                                 font-size: 75px;
                           }
                           QLabel#emoji_label{
                                font-size: 100px;
                               font-family: segoe UI emoji;
                           }
                           QLabel#description_label{
                                font-size: 50px;
                           }
                                 """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
            api_key = os.getenv("API_KEY")
            city = self.city_input.text()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                 response = requests.get(url, timeout=5)
                 response.raise_for_status()
                 data = response.json()
                 print(data)

                 if data["cod"] == 200:
                   self.display_weather(data)

            except requests.exceptions.HTTPError as http_error:
                 match response.status_code:
                      case 400:
                           self.display_error("Bad request:\nPlease check your input")
                      case 401:
                           self.display_error("Unauthorized:\nInvalid API key")
                      case 403:
                           self.display_error("Forbidden:\nAccess is denied")
                      case 404:
                           self.display_error("NOT FOUND:\nCity not found")
                      case 500:
                           self.display_error("Internal server error:\nPlease try again later")
                      case 502:
                           self.display_error("Bad Gateway:\nInvalid resp[onse from the server")
                      case 503:
                           self.display_error("Service unavilabel:\nserver is down")
                      case 504:
                           self.display_error("Gateway timeout:\nNO response from the server")
                      case _:
                           self.display_error(f"HTTP error occured:\n{http_error}")
                    
            except requests.exceptions.ConnectionError:
                 self.display_error("Connection error:\ncheck your internet connection")
            except requests.exceptions.Timeout:
                 self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                 self.display_error("Too many redirects:\ncheck the url")           
            except requests.exceptions.RequestException as req_error:
                 self.display_error(f"Request error:\n{req_error}")
     
    def get_weather_emoji(self, weather_id):

      if 200 <= weather_id <= 232:
        return "⛈️"      

      elif 300 <= weather_id <= 321:
        return "🌦️"  

      elif 500 <= weather_id <= 531:
        return "🌧️"

      elif 600 <= weather_id <= 622:
        return "❄️"

      elif 701 <= weather_id <= 781:
        return "🌫️"      

      elif weather_id == 800:
        return "☀️"    

      elif 801 <= weather_id <= 804:
        return "☁️" 

      else:
        return "🌍"
                
            
    def display_error(self,message):
            self.temperature_label.setStyleSheet("font-size: 30px;")
            self.temperature_label.setText(message)
            self.emoji_label().clear
            self.description_label().clear

    
    def display_weather(self,data):
               self.temperature_label.setStyleSheet("font-size: 20px;")
               temperature_c = data['main']['temp']
               temperature_k = 273.15+temperature_c
               temperature_f = (temperature_c * 9/5) + 32
               self.temperature_label.setText(f"{temperature_c}°C")
               weather_description = data["weather"][0]["description"]
               weather_id = data["weather"][0]["id"]

               self.description_label.setText(weather_description)

               emoji = self.get_weather_emoji(weather_id)
               self.emoji_label.setText(emoji)


                           
        

if __name__== "__main__":
    app = QApplication(sys.argv)
    Weather_app = WeatherApp()
    Weather_app.show()
    sys.exit(app.exec_())