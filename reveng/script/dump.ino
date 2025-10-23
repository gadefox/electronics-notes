#include <SPI.h>

#define PIN_CS   15  // D8
#define PIN_WP   4   // D2
#define PIN_HOLD 5   // D1

const uint32_t FLASH_SIZE = 4UL * 1024UL * 1024UL; // 4 MB
byte buf[256];

byte xfer(byte b) { return SPI.transfer(b); }

void readData(uint32_t addr, uint8_t *outBuf, uint16_t len) {
  digitalWrite(PIN_CS, LOW);
  xfer(0x03); // READ command
  xfer((addr >> 16) & 0xFF);
  xfer((addr >> 8) & 0xFF);
  xfer(addr & 0xFF);
  for (uint16_t i = 0; i < len; ++i)
    outBuf[i] = xfer(0x00);
  digitalWrite(PIN_CS, HIGH);
}

void setup() {
  Serial.begin(115200);
  delay(200);

  pinMode(PIN_CS, OUTPUT);
  pinMode(PIN_WP, OUTPUT);
  pinMode(PIN_HOLD, OUTPUT);
  digitalWrite(PIN_CS, HIGH);
  digitalWrite(PIN_WP, HIGH);
  digitalWrite(PIN_HOLD, HIGH);

  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV8); // ~10 MHz
  SPI.setDataMode(SPI_MODE0);

  Serial.println("--- 4MB HEX DUMP ---");

  uint32_t addr = 0;
  while (addr < FLASH_SIZE) {
    readData(addr, buf, 256);
    for (uint16_t i = 0; i < 256; i += 16) {
      char line[100];
      int p = sprintf(line, "%06X: ", addr + i);
      for (byte j = 0; j < 16; j++)
        p += sprintf(line + p, "%02X ", buf[i + j]);
      Serial.println(line);
    }
    addr += 256;
    yield();
  }

  Serial.println("--- DONE ---");
}

void loop() {}
