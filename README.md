# Sensor Data Visualiser

<img width="150" height="150" src="./src/resources/icon.svg"/>

This application is a flexible framework for wirelessly visualising sensor data via Bluetooth. Simply transmit data in a specified format over Bluetooth.

## Features
- Support for Bluetooth Low Energy and Bluetooth Serial Port
- Customisable Charts
- Real-time data streaming

<br>

## System Overview
```mermaid
flowchart LR
    A[User] --> |Interacts| B[Frontend]
    B[Frontend] <--> C[Backend]
    C[Backend] --> D{Prototype}
    D --> |Bluetooth Data Transmission| C
```

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
### App Virtual Port Mode (For Debugging without Bluetooth Devices)
In Terminal 1,
1. Install socat
2. Customise the create_virtual_port.sh script to emit any type of data packet
3. Run the create_virtual_port.sh script with
```console
bash create_virtual_port.sh
```

In Terminal 2, run with the -v argument
```console
python src/app.py -v /tmp/vcomport1
```

### Backend Only Mode
```console
python src/play_backend.py
```

## Compatibility
- This app has been tested on both Windows and MacOS
- Linux should be compatible

## Testing the app
The arduino code that was used to test the app is located in the "arduinoTestCode" folder. This code can be used to test the app when additional features or fixes are added to the app.

The hardware needed for the test code includes:
- An Arduino Uno
- A joystick sensor 
- A temperature sensor 
- A touch sensor

The hardware pin out connections are commented at the top of the test code file
