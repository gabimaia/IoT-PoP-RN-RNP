/*
* Monitoramento de Grandezas Elétricas do PoP-RN/RNP
* Autores do code: Gabriel Maia e Helton P L Medeiros
* 
* Monitoramento de tensão, corrente e potência em redes de baixa tensão utilizando ESP-12 e a plataforma ThingSpeak.
* 23-05-2019
* 
* Libs utilizadas: ESP8266WiFi e EmonLib
* 
* I/Os utilizados: A0
*
* Versão 1.0
*/

//Include da lib de Wifi do ESP8266
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

//Include da lib EmonLib para o sensor de corrente
#include "EmonLib.h"

//Definir o SSID da rede WiFi
const char* ssid = "Bolsistas";
//Definir a senha da rede WiFi
const char* password = "bolsistas1234";
 
//API Key para escrita do canal
String apiKey = "PWQLPYWGV1K26KTO";
const char* server = "api.thingspeak.com";

//Parâmetros para coleta dos dados

int enable = D3;
float tensao;
float aRef=3.3;
float relacao=75.75;

#define AMOSTRAS 12

EnergyMonitor emon1;

void setup() {
  //Configuração da UART
  Serial.begin(9600);
  //Serial.begin(115200);
  //Inicializar o WiFi
  WiFi.begin(ssid, password);
 
  //Delay para estabelecimento da conexão
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  //String thisBoard = ARDUINO_BOARD;
  //Serial.println(thisBoard);
  emon1.current(A0,29);
  pinMode(enable, OUTPUT);

  //Logs na porta serial
  Serial.println("");
  Serial.print("Conectado na rede ");
  Serial.println(ssid);
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);   // imprime Endereco IP
  ipAddress = ip.toString();
}



// Inserir Codigo que faz a coleta dos sensores

float lePorta(uint8_t portaAnalogica) {
  float total=0;  
  for (int i=0; i<AMOSTRAS; i++) {
    total += 1.0 * analogRead(portaAnalogica);
    delay(5);
  }
  return (((total / (float)AMOSTRAS)*aRef)/ 1024.0)*(relacao);
}  

void loop() {
  
  digitalWrite(enable, HIGH);
  delay(500);
  
  tensao = lePorta(A0);
  //String V = String(tensao);
  //client.publish("testeP8", V);

  digitalWrite(enable, LOW);
  delay(500);
  
  double Irms = emon1.calcIrms(1480);
  //String c = String(Irms);
  //client.publish("testeSCT", c);
  
  
  float potencia = tensao * Irms;;
  //String P = String(potencia);
  //client.publish("testepower", P);

    float watt = potencia * 0.9;;
  //String P = String(potencia);
  //client.publish("testepower", P);
 
 //Inicia um client TCP para o envio dos dados
  if (client.connect(server,80)) {
    String postStr = apiKey;
           postStr +="&amp;field1=";
           postStr += String(tensao);
           postStr +="&amp;field2=";
           postStr += String(Irms);
           postStr +="&amp;field3=";
           postStr += String(potencia);
           postStr +="&amp;field4=";
           postStr += String(watt);
           postStr += "\r\n\r\n";
 
     client.print("POST /update HTTP/1.1\n");
     client.print("Host: api.thingspeak.com\n");
     client.print("Connection: close\n");
     client.print("X-THINGSPEAKAPIKEY: "+apiKey+"\n");
     client.print("Content-Type: application/x-www-form-urlencoded\n");
     client.print("Content-Length: ");
     client.print(postStr.length());
     client.print("\n\n");
     client.print(postStr);
 
     //Logs na porta serial
     Serial.print("Tensão em volts: ");
     Serial.print(tensao);
     Serial.print("Corrente em Amperes: ");
     Serial.println(Irms);
     Serial.print("Potencia Aparente em VA: ");
     Serial.print(potencia);
     Serial.print("Potencia em Watts: ");
     Serial.println(watt);
  }
  client.stop();
  
  delay(500);
  
}



