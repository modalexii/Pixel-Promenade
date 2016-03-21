#include <Artnet.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>
#include <OctoWS2811.h> // modified for this project
#include <NewPing.h>

#define BETWEEN(value, min, max) (value < max && value > min)

// Controller setup
char ctrlrIDLetter = 'A'; // change ID to value A-L

int ctrlrID = ctrlrIDLetter - '0' - 16; // convert to int so A->1, B->2, etc, preferred over 12 case switch)
int networkOctet = 100 + ctrlrID;

// OctoWS2811 setup
const int ledsPerStrip = 115*4; // only using 2 data pins, but zig-zagging data over 4 rows each (configured in MADRIX)
const byte numStrips = 2;
DMAMEM int displayMemory[ledsPerStrip*6];
int drawingMemory[ledsPerStrip*6];
const int config = WS2811_GRB | WS2811_800kHz;
OctoWS2811 leds(ledsPerStrip, displayMemory, drawingMemory, config);

// Artnet setup
Artnet artnet;
const int startUniverse = (8 * ctrlrID) - 7; // A: UVSE 1-8, B: 9-16, etc
const int numberOfChannels = ledsPerStrip * numStrips * 3; 
byte channelBuffer[numberOfChannels]; 
//const int maxUniverses = 2;//numberOfChannels / 512 + ((numberOfChannels % 512) ? 1 : 0); // often 1
//bool universesReceived[maxUniverses]; // array to mark universes as rcvd
//bool sendFrame = 1;

// ArtNet remote control setup
byte serverIP[] = {10,0,1,1};
unsigned int artNetPort = 6454;
const int remoteUniverse = 0;
const int numChannels=512;
char ANProtoHead[8]="Art-Net";
const int ANProtoHeaderSize=17;
short OpOutput= 0x5000;
byte DmxBuffer[numChannels];
EthernetUDP Udp;
byte  ArtDmxBuffer[(ANProtoHeaderSize+numChannels)+8+1];
// channel is startUniverse for sA and startUniverse+1 for sB
elapsedMillis remoteTimer;
const int remoteFrequency = 500;

// Network setup 
byte ip[] = {10,0,1,networkOctet};
byte mac[] = {0x04, 0xE9, 0xEE, 0x00, 0x69, ctrlrID};

// HC-SR04 sensor setup
#define TRIGGER_PIN_A 3
#define ECHO_PIN_A 5
#define TRIGGER_PIN_B 6
#define ECHO_PIN_B 7
#define MAX_DISTANCE 511 // Dist value must be 0-255, so /2
NewPing sonar_a(TRIGGER_PIN_A, ECHO_PIN_A, MAX_DISTANCE);
NewPing sonar_b(TRIGGER_PIN_B, ECHO_PIN_B, MAX_DISTANCE);

// Sensor data persistance
int read_a;
int read_b;

void setup() {
  
  Serial.begin(9600);
  delay(2000);
  initPrint();

  // ArtNet Reciever
  artnet.begin(mac, ip);
  leds.begin();
  initTest();
  artnet.setArtDmxCallback(onDmxFrame);

  // ArtNet Remote Control
  initANHeader();
  Ethernet.begin(mac,ip);
  Udp.begin(artNetPort);
  
}

void loop() {
  
  // Recieve ArtNet
  artnet.read();

  // Send sensor data (ArtNet Remote)
  if (remoteTimer > remoteFrequency) {
    // get new readings
    Serial.println("read");
    remoteTimer = 0;
    bufferSensorReads();
  }
  // send a value every loop
  initANHeader(); // does this need to be done twice??
  Udp.beginPacket(serverIP, artNetPort);
  Udp.write(ArtDmxBuffer,(ANProtoHeaderSize+numChannels+1)); // was Udp.sendPacket
  Udp.endPacket();
  
}

void onDmxFrame(uint16_t universe, uint16_t length, uint8_t sequence, uint8_t* data) {

  /*
   * read dmx data from packet and write it to the pixels
   */
  /*
  Serial.print(millis());
  Serial.print(" Recieved Art-Net Packet len: ");
  Serial.print(length);
  Serial.print(" UVSE: ");
  Serial.println(universe);
  */
  /*
  // mark which universe this packet was addresses to
  if (universe < maxUniverses)
    universesReceived[universe] = 1;

  for (int i = 0 ; i < maxUniverses ; i++) {
    if (universesReceived[i] == 0) {
      Serial.print("Universe ");
      Serial.print(universe);
      Serial.println(" is out of config range (ERR 'BROKE'). Ignoring data.");
      sendFrame = 0;
      break;
    }
  }
  */
  // read universe and put into the right part of the display buffer
  for (int i = 0 ; i < length ; i++) {
    int bufferIndex = i + ((universe - startUniverse) * length);
    if (bufferIndex < numberOfChannels) // to verify
      channelBuffer[bufferIndex] = byte(data[i]);
  }      

  // send to leds
  for (int i = 0; i < ledsPerStrip * numStrips; i++) {
    leds.setPixel(i, channelBuffer[(i) * 3], channelBuffer[(i * 3) + 1], channelBuffer[(i * 3) + 2]);
  }      
  
  //if (sendFrame) {
  leds.show();
  // Reset universeReceived to 0
  //memset(universesReceived, 0, maxUniverses);
  //}
  
}

void initPrint() {

  /*
   * print basic info to the serial console
   */

   Serial.println("----- BEGIN INIT INFO -----");
   Serial.print("Controller ID: ");
   Serial.print(ctrlrIDLetter);
   Serial.print(" / #");
   Serial.println(ctrlrID);
   Serial.print("Network octet: ");
   Serial.println(networkOctet);
   Serial.print("LEDs per strip: ");
   Serial.println(ledsPerStrip);
   Serial.print("Strip count: ");
   Serial.println(numStrips);
   Serial.print("DMX start universe: ");
   Serial.println(startUniverse);
   Serial.print("Remote universe: ");
   Serial.println(remoteUniverse);
   Serial.print("Sensor A channel: ");
   Serial.println(startUniverse);
   Serial.print("Sensor B channel: ");
   Serial.println(startUniverse+1);
   Serial.println("----- END INIT INFO -----");
   Serial.println();
   
}

void initTest() {

  /*
   * Show colors to indicate that strips work
   */

   Serial.println("init test - cycling colors after short sleep");

  // init strips in order in sets of 3
  delay(1000 * (ctrlrID % 4));

  int wait = 1000; // how long to show each color
  
  for (int i = 0 ; i < ledsPerStrip * numStrips ; i++)
    leds.setPixel(i, 127, 0, 0);
  leds.show();
  delay(wait);
  for (int i = 0 ; i < ledsPerStrip * numStrips  ; i++)
    leds.setPixel(i, 0, 127, 0);
  leds.show();
  delay(wait);
  for (int i = 0 ; i < ledsPerStrip * numStrips  ; i++)
    leds.setPixel(i, 0, 0, 127);
  leds.show();
  delay(wait);
  for (int i = 0 ; i < ledsPerStrip * numStrips  ; i++)
    leds.setPixel(i, 0, 0, 0);
  leds.show();
  
}

void initANHeader() {

  /*
   * Fill packet header in to buffer
   */
  
  for (int i=0;i<7;i++) {
    ArtDmxBuffer[i]=ANProtoHead[i];
  }   
  
  //Operator code low byte first  
  ArtDmxBuffer[8] = OpOutput;
  ArtDmxBuffer[9] = OpOutput >> 8;
  ArtDmxBuffer[10] = 0; // protocol
  ArtDmxBuffer[11] = 14;
  ArtDmxBuffer[12] = 0; // sequence
  ArtDmxBuffer[13] = 0; // physical
  ArtDmxBuffer[14] = remoteUniverse; // universe
  ArtDmxBuffer[15] = remoteUniverse>> 8;
  ArtDmxBuffer[16] = numChannels>> 8; // data length
  ArtDmxBuffer[17] = numChannels;

  for (int t= 0;t<numChannels;t++) {
    ArtDmxBuffer[t+ANProtoHeaderSize+1]=DmxBuffer[t];    
  }
     
}

void bufferSensorReads() {

  /*
   * Read from sensors and place data in DMX buffer
   */

  bool send = 0;
  
  // Read from sensors
  read_a = sonar_a.ping_cm() / 2;
  read_b = sonar_b.ping_cm() / 2;
  
  Serial.print("A: ");
  Serial.println(read_a);
  Serial.print("B: ");
  Serial.println(read_b);

  // Place readings in ArtNet Packet
  // Start channel is same as startUniverse
  // All remote happend in universe 0
  DmxBuffer[startUniverse-1] = read_a;
  DmxBuffer[startUniverse] = read_b;

}

