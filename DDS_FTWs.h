/*u8 reg11_FTW_PR1[4] = {  0x49, 0x24, 0x92, 0x49 };        //1Ghz@ref clk = 3.5G
u8 reg11_FTW_PR1_100Mhz[4] = {  0x0A, 0x3D, 0x70, 0xA3 }; //100Mhz
u8 reg11_FTW_PR1_50Mhz[4] = {  0x05, 0x1E, 0xB8, 0x51 };  //100Mhz
u8 reg11_FTW_PR1_90Mhz[4] = {  0x06, 0x95, 0x36, 0x20 };  //100Mhz@ref clk = 3.5G
u8 reg11_FTW_PR1_900Mhz[4] = {  0x41, 0xD4, 0x1D, 0x41 }; //900Mhz@ref clk = 3.5G
u8 reg11_FTW_PR1_800Mhz[4] = {  0x3A, 0x83, 0xA8, 0x3A }; //800Mhz@ref clk = 3.5G
u8 reg11_FTW_PR1_700Mhz[4] = {  0x33, 0x33, 0x33, 0x33 }; //800Mhz@ref clk = 3.5G
u8 reg11_FTW_PR1_600Mhz[4] = {  0x2B, 0xE2, 0xBE, 0x2B }; //800Mhz@ref clk = 3.5G
u8 reg11_FTW_PR1_500Mhz[4] = {  0x24, 0x92, 0x49, 0x24 }; //800Mhz@ref clk = 3.5G
*/
static const uint32_t FTWlookup[8] ={

0x051EB851,	//50 Mhz
0x0A3D70A3, //100
0x24924924, //500
0x2BE2BE2B, //600
0x33333333,	//700
0x3A83A83A,	//800
0x41D41D41,	//900 
0x49249249  //1000
};