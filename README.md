# Sensor Data Visualiser

<img width="150" height="150" src="./src/resources/icon.svg"/>

This application is a flexible framework for wirelessly visualising sensor data via Bluetooth. Simply transmit data in the specified format over Bluetooth.

## Features
- Support for Bluetooth Low Energy and Bluetooth Serial Port
- Customisable Charts
- Real-time data streaming

<br>

# Table of Contents  
- [Data Packet Format](#Data-Format-for-Transmission-via-Bluetooth)
- [Installation](#Installation)
- [Running the App](#Running-the-App)
- [Compatibility](#Compatibility)


## Data Format for Transmission via Bluetooth
### Structure
Data is passed as strings, with each line being constructed of

```
<name_sensor_1>: data_sensor_1, <name_sensor_2>: data_sensor_2, ...
```
where each line represents a single reading for each sensor.

#### Requirements
- Names are alphanumeric characters with no spaces
- Data are floats
- The comma at the end is required

<br>

***Note: Not following the data format will lead to errors.***

### Example 1
```
<temperature>: 32,
```
### Example 2
```
<temperature>: 32, <weight>: 53.21, <height>: 173.21, 
```


## Installation
1. Install Python version 3.12 (Any version 3.12+ should work)
2. Create a virtual environment
```console
python -m venv venv
```
3. Activate the virtual environment
```console
source venv/bin/activate
```
4. Install dependencies
```console
pip install -r requirements.txt
```

## Running the App
### Standalone App
```console
python src/app.py
```
### App Debug Mode
```console
python src/app.py -d
```

### Backend Only Mode
```console
python src/play_backend.py
```

## Compatibility
- This app has been tested on both Windows and MacOS
- Linux should be compatible
