#include <ESP8266WiFi.h>

const char* ssid = "GTFO";
const char* password = "BosqRomain06";
bool b = 0;
String alarmTime, alarmH, alarmM;
int ledPin = 13; // GPIO13
int sortieH = 13;
int sortieM = 11;
int sortieS = 10;
char str[4];

WiFiServer server(80);

void setup() {
  Serial.begin(9600);
  delay(10);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  pinMode(sortieH, OUTPUT);
  //pinMode(sortieM, OUTPUT);
  //pinMode(sortieS, OUTPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  // Start the server
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();

  if (!client) {
    if (b == 1)
    {
      delay(7000);
      if ((alarmH.toInt() == getHMS()[0]) && (alarmM.toInt() <= getHMS()[1])) {
        //digitalWrite(ledPin, HIGH);
        return;
      }
    }
    return;
  }

  while (!client.available()) {
    delay(1);
  }

  // Read the first line of the request
  String request = client.readStringUntil('\r');
  client.flush();

  // Match the request

  if (request.indexOf("/ALARMTIME=") != -1)  {
    b = 1;
    alarmTime = request.substring(15, 19);
    alarmH = alarmTime.substring(0, 2);
    alarmM = alarmTime.substring(2, 4);
  }

  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  delay(2000);
  client.println("<br><br>");
  client.print("Alarm time: ");
  client.print(alarmH); client.print("h"); client.print(alarmM); client.print("min");
  client.println("</html>");
  delay(1);
  sendToArduino();
}

int* getHMS() {
  int tab[3];
  tab[0] = ((getTime().substring(17, 19).toInt() + 1) == 24) ? 0 : getTime().substring(17, 19).toInt() + 1;
  tab[1] = getTime().substring(20, 22).toInt();
  tab[2] = getTime().substring(23, 25).toInt();
  return tab;
}

void sendToArduino()
{
  int h = getHMS()[0];
  int m = getHMS()[1];
  int s = getHMS()[2];

  if (h < 10) Serial.write('0');
  itoa(h, str, 10);
  Serial.write(str);
  delay(100);
  itoa(m, str, 10);
  Serial.write(str);
  delay(100);
  itoa(s, str, 10);
  Serial.write(str);
  
  delay(100);
  Serial.write(alarmH.c_str());
  delay(100);
  Serial.write(alarmM.c_str());
}

String getTime() {
  WiFiClient client;
  while (!!!client.connect("google.fr", 80)) {
  }

  client.print("HEAD / HTTP/1.1\r\n\r\n");

  while (!!!client.available()) {
    yield();
  }

  while (client.available()) {
    if (client.read() == '\n') {
      if (client.read() == 'D') {
        if (client.read() == 'a') {
          if (client.read() == 't') {
            if (client.read() == 'e') {
              if (client.read() == ':') {
                client.read();
                String theDate = client.readStringUntil('\r');
                client.stop();
                return theDate;
              }
            }
          }
        }
      }
    }
  }
}
