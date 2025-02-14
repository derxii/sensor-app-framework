// File name: sensorAppTestCode.ino
// This file is used for testing the sensor app
// The sensors used include a joystick sensor, temperature sensor and touch sensor. The bluetooth module used was a HMSoft.
// The program also generates fake temperature data so the app can test sensor matrices and heatmaps 

/*
   Hardware Pinout Connection
   Arduino UNO        joy stick sensor
        3.3v ----------- VCC
        GND ------------ GND
        A1 ------------- VRx
        A2 ------------- VRy
        D2 ------------- SW
  ________________________________________
   Arduino UNO         temperature sensor
        3.3v ----------- VCC
        GND ------------ GND
        A0 ------------- Out
  ________________________________________
   Arduino UNO         touch sensor
      3.3v ----------- VCC
      GND ------------ GND
      D3  ------------ Out
  ________________________________________
   Arduino UNO        HMSoft
          3.3v ----------- VCC
          GND ------------ GND
          D0 ------------- TX
          D1 ------------- RX
  ________________________________________
  
*/

float temp;
int tempPin = A0;
int touchPin = 3;
#define VRX_PIN  A1 // Arduino pin connected to VRX pin
#define VRY_PIN  A2 // Arduino pin connected to VRY pin

int xValue = 0; // To store value of the X axis
int yValue = 0; // To store value of the Y axis

String sensorNames[9] = {"<temperature1>:", "<temperature2>: ", "<temperature3>: ", "<temperature4>: ", "<temperature5>: ", "<temperature6>: ", "<temperature7>: ", "<temperature8>: ", "<temperature9>: "};

void setup() {
   Serial.begin(9600);
   pinMode(tempPin, INPUT);
   pinMode(touchPin, INPUT);
}

void loop() {
   // read analog X and Y analog values
  xValue = analogRead(VRX_PIN);
  yValue = analogRead(VRY_PIN);

  // print data to Serial Monitor on Arduino IDE
  Serial.print("<joystickX>: ");
  Serial.print(xValue);
  Serial.print(",");
  Serial.print("<joystickY>: ");
  Serial.print(yValue);
  Serial.print(",");
   temp = analogRead(tempPin);
   // read analog volt from sensor and save to variable temp
   temp = temp * 0.48828125;
   // convert the analog volt to its temperature equivalent
   int touchVal = digitalRead(touchPin);
   Serial.print("<temperature>: ");
   Serial.print(temp); // display temperature value
   Serial.print(",");
   Serial.print("<touch>: ");
   Serial.print(touchVal); // display temperature value
   Serial.print(", ");
    for (int i = 0; i < 9; i++) {
      Serial.print(sensorNames[i]);
      long randTempVal = random(1, 10);
      Serial.print(randTempVal);
      Serial.print(", ");
    }
    Serial.println();
   
   delay(100); // update sensor reading each one second
}