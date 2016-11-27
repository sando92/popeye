#include <Wire.h>
#include <LiquidCrystal.h>
#include "notes.h"
#define DS3231_I2C_ADDRESS 0x68

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// Musique Mario
int melody[] = {
  NOTE_E7, NOTE_E7, 0, NOTE_E7,
  0, NOTE_C7, NOTE_E7, 0, NOTE_G7, 0, 0,  0,
  NOTE_G6, 0, 0, 0,
 
  NOTE_C7, 0, 0, NOTE_G6,
  0, 0, NOTE_E6, 0,
  0, NOTE_A6, 0, NOTE_B6,
  0, NOTE_AS6, NOTE_A6, 0,
 
  NOTE_G6, NOTE_E7, NOTE_G7,
  NOTE_A7, 0, NOTE_F7, NOTE_G7,
  0, NOTE_E7, 0, NOTE_C7,
  NOTE_D7, NOTE_B6, 0, 0
};
/*{
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};*/
// note durations: 4 = quarter note, 8 = eighth note, etc.:
// Tempo Mario
int noteDurations[] = {
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12
};
/*{
  4, 8, 8, 4, 4, 4, 4, 4
};*/
//Fonction qui gère le haut parleur
void ringAlarm() {
  // iterate over the notes of the melody:
  int sizeM = sizeof(melody) / sizeof(int);
  for (int thisNote = 0; thisNote < sizeM; thisNote++) {

    // to calculate the note duration, take one second
    // divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(4, melody[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(4);
  }
}

// Convert normal decimal numbers to binary coded decimal
byte decToBcd(byte val)
{
  return( (val/10*16) + (val%10) );
}
// Convert binary coded decimal to normal decimal numbers
byte bcdToDec(byte val)
{
  return( (val/16*10) + (val%16) );
}
//Timer day
int t=0;
int nbRing=0;
int heureActu = 0, minuteActu = 0, secondeActu = 0;
int heureAlarm = 0, minuteAlarm = 0, secondeAlarm = 0;
int dayOfWeek = 7;
int dayOfMonth = 27;
int month = 11;
int year = 16;
void setHourInternet() {
  if (Serial.available()) {
    delay(100); //allows all serial sent to be received together
    while(Serial.available()) {
      
      heureActu = (Serial.read()-48)*10;       
      delay(100);
      heureActu = Serial.read()-48 + heureActu; 
      Serial.print("Heure : ");
      Serial.println(heureActu, DEC);

      delay(100);
      minuteActu = (Serial.read()-48)*10;       
      delay(100);
      minuteActu = Serial.read()-48 + minuteActu; 
      Serial.print("Minute : ");
      Serial.println(minuteActu, DEC);

      delay(100);
      secondeActu = (Serial.read()-48)*10; 
      delay(100);
      secondeActu = Serial.read()-48 + secondeActu; 
      Serial.print("Seconde : ");
      Serial.println(secondeActu, DEC);
      
//ALARME
      delay(100);
      heureAlarm = (Serial.read()-48)*10; 
      delay(100);
      heureAlarm = Serial.read() + heureAlarm; 
      Serial.print("Heure alarme : ");
      Serial.println(heureAlarm-48, DEC);
      
      delay(100);
      minuteAlarm = (Serial.read()-48)*10; 
      delay(100);
      minuteAlarm = Serial.read() + minuteAlarm; 
      Serial.print("Minute alarme : ");
      Serial.println(minuteAlarm-48, DEC);
    }
  }
  // sets time and date data to DS3231
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set next input to start at the seconds register
  Wire.write(decToBcd(secondeActu)); // set seconds
  Wire.write(decToBcd(minuteActu)); // set minutes  
  Wire.write(decToBcd(heureActu)); // set hours
  
  Wire.write(decToBcd(dayOfWeek)); // set day of week (1=Sunday, 7=Saturday)
  Wire.write(decToBcd(dayOfMonth)); // set date (1 to 31)
  Wire.write(decToBcd(month)); // set month
  Wire.write(decToBcd(year)); // set year (0 to 99)
  Wire.endTransmission();
}
/*void setAlarm(byte *hourAlarm, byte* minuteAlarm, byte *secondeAlarm) {
  if (Serial.available()) {
    delay(100); //allows all serial sent to be received together
    while(Serial.available()) {
      
//ALARME
      delay(100);
      heureAlarm = (Serial.read()-48)*10; 
      delay(100);
      heureAlarm = Serial.read() + heureAlarm; 
      Serial.print("Heure alarme : ");
      Serial.println(heureAlarm-48, DEC);
      
      delay(100);
      minuteAlarm = (Serial.read()-48)*10; 
      delay(100);
      minuteAlarm = Serial.read() + minuteAlarm; 
      Serial.print("Minute alarme : ");
      Serial.println(minuteAlarm-48, DEC);
      
      delay(100);
      secondeAlarm = (Serial.read()-48)*10; 
      delay(100);
      secondeAlarm = Serial.read() + secondeAlarm; 
      Serial.print("Seconde alarme : ");
      Serial.println(secondeAlarm-48, DEC);
    }
  }
}*/
void setup()
{
  lcd.begin(16,2);  
  Wire.begin();
  Serial.begin(9600);
  // set the initial time here:
  //DS3231 seconds, minutes, hours, day, date, month, year
  
  //setHourInternet();
  //setDS3231time(40,22,21,7,21,11,16);
}
void setDS3231time(byte second, byte minute, byte hour, byte dayOfWeek, byte dayOfMonth, byte month, byte year)
{
  // sets time and date data to DS3231
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set next input to start at the seconds register
  Wire.write(decToBcd(second)); // set seconds
  Wire.write(decToBcd(minute)); // set minutes  
  Wire.write(decToBcd(hour)); // set hours
  Wire.write(decToBcd(dayOfWeek)); // set day of week (1=Sunday, 7=Saturday)
  Wire.write(decToBcd(dayOfMonth)); // set date (1 to 31)
  Wire.write(decToBcd(month)); // set month
  Wire.write(decToBcd(year)); // set year (0 to 99)
  Wire.endTransmission();
}
void readDS3231time(byte *second,byte *minute,byte *hour,byte *dayOfWeek,byte *dayOfMonth,byte *month,byte *year)
{
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0); // set DS3231 register pointer to 00h
  Wire.endTransmission();
  Wire.requestFrom(DS3231_I2C_ADDRESS, 7);
  // request seven bytes of data from DS3231 starting from register 00h
  *second = bcdToDec(Wire.read() & 0x7f);
  *minute = bcdToDec(Wire.read());
  *hour = bcdToDec(Wire.read() & 0x3f);
  *dayOfWeek = bcdToDec(Wire.read());
  *dayOfMonth = bcdToDec(Wire.read());
  *month = bcdToDec(Wire.read());
  *year = bcdToDec(Wire.read());
}
void displayTime(byte *second, byte *minute, byte *hour, byte *dayOfWeek, byte *dayOfMonth, byte *month, byte *year)
{
  lcd.clear();
  lcd.setCursor(0,0);  
  // send it to the serial monitor
  lcd.print(*hour, DEC);
  // convert the byte variable to a decimal number when displayed
  lcd.print(":");
  if (*minute<10)
  {
    lcd.print("0");
  }
  lcd.print(*minute, DEC);
  lcd.print(":");
  if (*second<10)
  {
    lcd.print("0");
  }
  lcd.print(*second, DEC);
}
void displayDay(byte *second, byte *minute, byte *hour, byte *dayOfWeek, byte *dayOfMonth, byte *month, byte *year)
{  
  lcd.clear();
  lcd.setCursor(0,0);
  switch(*dayOfWeek){
  case 1:
    lcd.print("Mon");
    break;
  case 2:
    lcd.print("Tue");
    break;
  case 3:
    lcd.print("Wed");
    break;
  case 4:
    lcd.print("Thu");
    break;
  case 5:
    lcd.print("Fri");
    break;
  case 6:
    lcd.print("Sat");
    break;
  case 7:
    lcd.print("Sun");
    break;
  }
  lcd.print(" ");
  lcd.print(*dayOfMonth, DEC);
  lcd.print("/");
  lcd.print(*month, DEC);
  lcd.print("/");
  lcd.print(*year, DEC);
}
void displayAlarmDef(byte *hourAlarm, byte *minuteAlarm, byte *secondAlarm)
{
  lcd.setCursor(0,2);  
  lcd.print("Alarme ");
  // send it to the serial monitor
  lcd.print(*hourAlarm, DEC);
  // convert the byte variable to a decimal number when displayed
  lcd.print(":");
  if (*minuteAlarm<10)
  {
    lcd.print("0");
  }
  lcd.print(*minuteAlarm, DEC);
  lcd.print(":");
  if (*secondAlarm<10)
  {
    lcd.print("0");
  }
  lcd.print(*secondAlarm, DEC);
}
void itsAlarm(byte *hourAlarm, byte *minuteAlarm, byte *secondAlarm)
{
  lcd.clear();
  lcd.setCursor(0,0);  
  lcd.print("Alarme !!!");
  // send it to the serial monitor
  lcd.setCursor(0,1);  
  lcd.print(*hourAlarm, DEC);
  // convert the byte variable to a decimal number when displayed
  lcd.print(":");
  if (*minuteAlarm<10)
  {
    lcd.print("0");
  }
  lcd.print(*minuteAlarm, DEC);
  lcd.print(":");
  if (*secondAlarm<10)
  {
    lcd.print("0");
  }
  lcd.print(*secondAlarm, DEC);
}

void loop()
{  
  byte second, minute, hour, dayOfWeek, dayOfMonth, month, year, hourAlarm, minuteAlarm, secondAlarm;
  // retrieve data from DS3231
  readDS3231time(&second, &minute, &hour, &dayOfWeek, &dayOfMonth, &month, &year);
//  readAlarm(&hourAlarm, &minuteAlarm, &secondAlarm);
  //en dur pour test
  hourAlarm = 12;
  minuteAlarm = 11;
  secondAlarm = 0;

  if (second==secondAlarm & minute==minuteAlarm & hour==hourAlarm){
      itsAlarm(&hourAlarm, &minuteAlarm, &secondAlarm);
      while (nbRing < 3){
          ringAlarm();
          delay(500);
          nbRing++;       
      }
      nbRing=0;
  }
  else{
      if (t>24){
        displayDay(&second, &minute, &hour, &dayOfWeek, &dayOfMonth, &month, &year);
        delay(3000);
        t=0;
      }
      else{  
        displayTime(&second, &minute, &hour, &dayOfWeek, &dayOfMonth, &month, &year); // display the real-time clock data on the Serial Monitor,
        t++;
      }
  }
  displayAlarmDef(&hourAlarm, &minuteAlarm, &secondAlarm);
  delay(1000); // every second
}
