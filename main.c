#include <stdio.h>
#include <stdint.h>

#define max(a, b) (a > b ? a : b)
#define min(a, b) (a > b ? b : a)
#define range(x, a, b) (min(max(a, x), b))

typedef struct openmv_data
{
    int16_t cx;       //Tag目标x坐标
    int16_t cy;       //Tag目标y坐标
    int16_t sx;       //目标Tag x坐标
    int16_t sy;       //目标Tag y坐标
    int16_t rotaion;  //目标Tag 偏转角
}OpenMv_Data;

OpenMv_Data Openmv;
uint8_t rx_buf_mv[64] = {35, 49, 160, 0, 120, 0, 149, 0, 131, 0, 42, 255, 42};
void output(const uint8_t *buf)
{
    for (int i = 0; i < 14; i++)
    {
        printf("%x ", buf[i]);
    }
}

/**
 * @brief: 将有符号float类型数据分成两个byte便于传输
 */
void Float2Uint8s(float src, uint8_t *byte_L, uint8_t *byte_H)
{
    int16_t int16Src = (int16_t)(src * 100);
    *byte_H = (int16Src >> 8) & 0xFF;
    *byte_L = (int16Src)&0xFF;
}

/**
 * @brief: 将两个uint8_t类型数据恢复成一个float数据
 */
void Uint8s2Float(float *dest, uint8_t byte_L, uint8_t byte_H)
{
    *dest = (float)((int16_t)(byte_H << 8) | byte_L) / 100.0f;
}

uint8_t MV_Process(void)
{
    if(rx_buf_mv[0] != 0x23 || rx_buf_mv[12] != 0x2A)
        return 1;
    Openmv.cx = (int16_t)(rx_buf_mv[3] << 8) | rx_buf_mv[2];
    Openmv.cy = (int16_t)(rx_buf_mv[5] << 8) | rx_buf_mv[4];
    Openmv.sx = (int16_t)(rx_buf_mv[7] << 8) | rx_buf_mv[6];
    Openmv.sy = (int16_t)(rx_buf_mv[9] << 8) | rx_buf_mv[8];
    Openmv.rotaion = (int16_t)(rx_buf_mv[11] << 8) | rx_buf_mv[10];
    return 0;
}

int main()
{
    MV_Process();
    printf("angle %d", Openmv.rotaion);
    return 0;
}