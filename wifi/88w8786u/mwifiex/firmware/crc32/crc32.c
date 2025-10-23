#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <byteswap.h>

/* reflexted */
uint32_t crc32(const uint8_t *data, size_t len) {
    uint32_t crc = 0;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i] << 24;
        for (int j = 0; j < 8; j++) {
            crc = (crc << 1) ^ (0x04C11DB7 & -(crc >> 31));
        }
    }
    return crc;
}

void test(uint32_t cmd, uint32_t addr, uint32_t len, uint32_t crc)
{
    uint32_t data[4];
    uint32_t calc;

    printf("Target CRC: 0x%08X\n", crc);

    data[0] = cmd;
    data[1] = addr;
    data[2] = len;
    data[3] = crc;
   
    calc = crc32((uint8_t*)data, sizeof(data) - sizeof(uint32_t));
    printf("CRC32 reflected+swapped: 0x%08X\n", __builtin_bswap32(calc));

    calc = crc32((uint8_t*)data, sizeof(data));
    printf("Test: %d\n\n", calc);
}

int main() {
    size_t n;
    FILE *f;
    uint32_t crc;
    uint8_t buf[528];
    uint32_t* data = (uint32_t*)buf;

    printf("Test: 0=OK\n\n");

    // crc: no payload
    test(0, 0, 0, 0);
    test(4, 0, 0, 0x188CDB1F);
    test(6, 0, 0, 0x144A3610);
    test(6, 0x00080A4D, 0, 0x39416A7F);
    test(6, 0x00080CF9, 0, 0xAEE2B639);
    test(6, 0x00080D2D, 0, 0x9AB29F76);
    test(6, 0x00080ECD, 0, 0xF9A9F63F);
    test(6, 0x00080F2D, 0, 0xB86231E8);
    test(7, 3, 3, 0x227E559B);

    // read blob file
    f = fopen("segm.bin", "rb");
    if (!f) {
        perror("ERROR: file does not exist");
        return 1;
    }

    n = fread(buf, 1, sizeof(buf), f);
    if (n != sizeof(buf))
        fprintf(stderr, "warning: read %zu bytes (expected 528)\n", n);

    fclose(f);

    // crc: with payload
    printf("Target CRC: 0x%08X\n", data[3]);
    crc = crc32(buf, 12);
    printf("CRC32 header: 0x%08X\n", __builtin_bswap32(crc));
    crc = crc32(buf, 16);
    printf("Test header: %d\n", crc);
    crc = crc32(buf + 16, 512);
    printf("Test payload: %d\n", crc);
}
