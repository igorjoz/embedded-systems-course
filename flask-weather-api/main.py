from datetime import datetime
from flask import Flask, render_template, request
import requests
import os
from flask_sqlalchemy import SQLAlchemy
 
 
import smbus
from time import sleep
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
 
 
# Adres urządzenia
device_address = 0x76
 
# I2C na RPi 4
i2c = smbus.SMBus(1)
 
# Adresy rejestrów
reg_chip_id = 0xD0
reg_chip_version = 0xD1
reg_status = 0xF3
reg_control = 0xF4
reg_config = 0xF5
reg_msb_pressure = 0xF7
reg_lsb_pressure = 0xF8
reg_xlsb_pressure = 0xF9
reg_msb_temperature = 0xFA
reg_lsb_temperature = 0xFB
reg_xlsb_temperature = 0xFC
reg_calibration_1 = 0x88
reg_calibration_2 = 0xA1
reg_calibration_3 = 0xE1
 
# Opcje próbkowania 0 .. 5, tryb 0 .. 3
osrs_t = 2 
osrs_p = 2
mode = 1
 
# OpenWeatherMap API key
API_KEY = "a5e449f2f406f9c0ec11477736c36ea6"
CITY = "Gdansk"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
 
data_list = []
labels = []
 
data_list_temp = []
labels_temp = []
 
app = Flask(__name__)
 
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sensor_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class TemperatureData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    temperature = db.Column(db.Float)
 
    def __repr__(self):
        return f"Temperature: {self.temperature} at {self.timestamp}"
 
with app.app_context():
    db.create_all()
 
def get_sensor_value():
    (chip_id, chip_version) = i2c.read_i2c_block_data(device_address, reg_chip_id, 2)
 
    # Ustawienie opcji próbkowania i trybu
    i2c.write_byte_data(device_address, reg_control, osrs_t << 5 | osrs_p << 2 | mode)
 
    # Dane kalibracyjne z pamięci EEPROM
    calibration_data_1 = i2c.read_i2c_block_data(device_address, reg_calibration_1, 24)
    calibration_data_2 = i2c.read_i2c_block_data(device_address, reg_calibration_2, 1)
    calibration_data_3 = i2c.read_i2c_block_data(device_address, reg_calibration_3, 7)
    dig_T1 = (calibration_data_1[1] << 8) + calibration_data_1[0]
    dig_T2 = c_short((calibration_data_1[3] << 8) + calibration_data_1[2]).value
    dig_T3 = c_short((calibration_data_1[5] << 8) + calibration_data_1[4]).value
    dig_P1 = (calibration_data_1[7] << 8) + calibration_data_1[6]
    dig_P2 = c_short((calibration_data_1[9] << 8) + calibration_data_1[8]).value
    dig_P3 = c_short((calibration_data_1[11] << 8) + calibration_data_1[10]).value
    dig_P4 = c_short((calibration_data_1[13] << 8) + calibration_data_1[12]).value
    dig_P5 = c_short((calibration_data_1[15] << 8) + calibration_data_1[14]).value
    dig_P6 = c_short((calibration_data_1[17] << 8) + calibration_data_1[16]).value
    dig_P7 = c_short((calibration_data_1[19] << 8) + calibration_data_1[18]).value
    dig_P8 = c_short((calibration_data_1[21] << 8) + calibration_data_1[20]).value
    dig_P9 = c_short((calibration_data_1[23] << 8) + calibration_data_1[22]).value
    dig_H1 = calibration_data_2[0] 
    dig_H2 = c_short((calibration_data_3[1] << 8) + calibration_data_3[0]).value
    dig_H3 = calibration_data_3[2] 
    dig_h4 = calibration_data_3[3]
    if dig_h4 > 127:
        dig_h4 -= 256
    dig_H4 = (dig_h4 << 24) >> 20
    dig_h4 = calibration_data_3[4]
    if dig_h4 > 127:
        dig_h4 -= 256
    dig_H4 = dig_H4 | (dig_h4 & 0x0F)
    dig_h5 = calibration_data_3[5]
    if dig_h5 > 127:
        dig_h5 -= 256
    dig_H5 = (dig_h5 << 24) >> 20
    dig_h5 = calibration_data_3[4] & 0xFF
    dig_H5 = dig_H5 | ((dig_h5 >> 4) & 0x0F)
    dig_H6 = calibration_data_3[6]
    if dig_H6 > 127:
        dig_H6 -= 256
 
    # Odczyt danych pomiarowych
    measurement = i2c.read_i2c_block_data(device_address, reg_msb_pressure, 8)
    pressure_raw = (measurement[0] << 12) | (measurement[1] << 4) | (measurement[2] >> 4)
    temperature_raw = (measurement[3] << 12) | (measurement[4] << 4) | (measurement[5] >> 4)
 
    # Wyznaczenie temperatury
    var1 = ((((temperature_raw >> 3) - (dig_T1 << 1)))*(dig_T2)) >> 11
    var2 = (((((temperature_raw >> 4) - (dig_T1))*((temperature_raw >> 4) - (dig_T1))) >> 12)*(dig_T3)) >> 14
    t_fine = var1 + var2
    temperature = float(((t_fine*5) + 128) >> 8)/100.0
 
    # Wyznaczanie ciśnienia
    var1 = t_fine/2.0 - 64000.0
    var2 = var1*var1*dig_P6/32768.0
    var2 = var2 + var1*dig_P5*2.0
    var2 = var2/4.0 + dig_P4*65536.0
    var1 = (dig_P3*var1*var1/524288.0 + dig_P2*var1)/524288.0
    var1 = (1.0 + var1/32768.0)*dig_P1
    if var1 == 0:
        pressure = 0
    else:
        pressure = 1048576.0 - pressure_raw
        pressure = ((pressure - var2/4096.0)*6250.0)/var1
        var1 = dig_P9*pressure*pressure/2147483648.0
        var2 = pressure*dig_P8/32768.0
        pressure = int((pressure + (var1 + var2 + dig_P7)/16.0))/ 100.0
 
    return [pressure, temperature]
 
# Function to fetch weather data
def get_weather():
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
 
    try:
        # Make the API request
        response = requests.get(URL)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
 
        # Parse the JSON response
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"].capitalize(),
        }
 
        return weather
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching weather data: {e}"}
    except KeyError:
        return {"error": "Error parsing weather data. Check the API key or city name."}
 
@app.route("/")
def index(name='time'):
    global labels
    data = get_sensor_value()
    if len(labels) == 0:
        labels = [0]
    else:
        labels.append(int(labels[-1])+1)
    data_list.append(data[0])
    value = "Pressure = " + str(data[0])
 
    return render_template(
        "index.html",
        l = labels,
        dl = data_list,
        v=value
    )
 
@app.route("/temperature")
def temperature():
    global labels_temp
    data = get_sensor_value()
    if len(labels_temp) == 0:
        labels_temp = [0]
    else:
        labels_temp.append(int(labels_temp[-1])+1)
    tmp_data = TemperatureData(temperature=data[1])
    db.session.add(tmp_data)
    db.session.commit()
    data_list_temp.append(data[1])
    value = "Temperature = " + str(data[1])
 
    return render_template(
        "index.html",
        l = labels_temp,
        dl = data_list_temp,
        v=value
    )
 
@app.route("/db")
def historic_temperature():
    temperatures = TemperatureData.query.order_by(TemperatureData.timestamp.desc()).all()
    temperatures_str = []
    for temperature in temperatures:
        temperatures_str.append(str(temperature))
 
    return render_template("db.html", temp_data = temperatures_str, temperatures_length = len(temperatures_str))
 
@app.route("/weather", methods=["GET", "POST"])
def weather_page():
    global CITY
    weather = None
    city = None
    if request.method == "POST":
        city = request.form.get("city")
    if city:
        CITY = str(city)
        weather = get_weather()
    else:
        weather = {"error": "Please enter a city name."}
    return render_template("weather.html", weather=weather)
    #return template(page_content, l = labels, dl = data_list, v=value)
#run(host='192.168.1.112', port=80)
    #return template('<span style="color: red; font-weight: 700; font-size: 100px; ">{{v}}</span>', v=value)
#run(host='192.168.1.112', port=80)