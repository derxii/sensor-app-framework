# Sensor Data Visualiser

<img width="150" height="150" src="./src/resources/icon.svg"/>

This application is a flexible tool for wirelessly visualising sensor data via Bluetooth. Simply transmit data in the specified format over Bluetooth.

## Features
- Support for Bluetooth Low Energy and Bluetooth Classic
- Customisable Charts
- Real-time data streaming

## Data Format for Transmission via Bluetooth

***Note: Not following the data format will lead to errors.***


## Installation
1. Install Python version 3.10 (Any version from 3.9 - 3.12 should work)
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
5. Run the app
```console
python src/app.py
```
6. To run the app in debug mode, pass the -d flag
```console
python src/app.py -d
```