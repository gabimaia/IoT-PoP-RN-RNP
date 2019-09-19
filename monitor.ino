#include "EspMQTTClient.h"
#include "EmonLib.h"
int enableA = D3;
int enableB = D2;
int enableC = D1;

float tensao;

float aRef=3.3;

float relacao=75.75;

#define AMOSTRAS 12

void ConnectiON();
EnergyMonitor emon1;


EspMQTTClient client(
  "Bolsistas",           // Wifi ssid
  "bolsistas1234",           // Wifi password
  "192.168.70.147",  // MQTT broker ip
  1883,             // MQTT broker port
  "aluno",            // MQTT username
  "alunopop",       // MQTT password
  "pcaluno",          // Client name
  ConnectiON, // Connection established callback
  true,             // Enable web updater
  true              // Enable debug messages
);

void setup() {
   
  Serial.begin(115200);
  Serial.println();
  String thisBoard = ARDUINO_BOARD;
  Serial.println(thisBoard);
  emon1.current(A0,29);
  pinMode(enableA, OUTPUT);
  pinMode(enableB, OUTPUT);
  pinMode(enableC, OUTPUT);
  //pinMode(port2, OUTPUT);
}

void ConnectiON()
{
  client.subscribe("testesp", [] (const String &payload)
  {
    Serial.println(payload);
  });
}

float lePorta(uint8_t portaAnalogica) {
  float total=0;  
  for (int i=0; i<AMOSTRAS; i++) {
    total += 1.0 * analogRead(portaAnalogica);
    delay(5);
  }
  return (((total / (float)AMOSTRAS)*aRef)/ 1024.0)*(relacao);
}  

void loop() {
  
  digitalWrite(enableA, HIGH);
  digitalWrite(enableB, LOW);
  digitalWrite(enableC, LOW);
  
  delay(500);
  
  tensao = lePorta(A0);
  String V = String(tensao);
  client.publish("testeP8", V);

  digitalWrite(enableB, HIGH);
  delay(500);
  
  double Irms = emon1.calcIrms(1480);
  String c = String(Irms);
  client.publish("testeSCT", c);
  
  
  float potencia = tensao * Irms;;
  String P = String(potencia);
  client.publish("testepower", P);

  
  client.loop();
  
  delay(500);
  
}
