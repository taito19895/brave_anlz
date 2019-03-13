#! /cygdrive/t/cygwin64/home/ito/PycharmProjects/brave_anlz/Scripts/python.exe

#coding:utf-8

import argparse
import fileinput

I2S1_RX_FSYNK_MASK = 0x0800
I2S1_RX_UWERR_MASK = 0x0400
I2S1_RX_UW1_MASK = 0x0200
I2S1_RX_DIV_MASK = 0x0100


##################################################################
#from https://qiita.com/wyamamo/items/38789488bc008e9223e6
##################################################################

#	/* i2s FPGA からの I2S ch1  受信 format (FPGA ver 20190304以降)
#       +-----------------------------------------------  [15] 選択系 D[3]
#       |  +--------------------------------------------  [14] 選択系 D[2]
#       |  |  +-----------------------------------------  [13] 選択系 D[1]
#       |  |  |  +--------------------------------------  [12] 選択系 D[0]
#       |  |  |  |                                        
#       |  |  |  |  +-----------------------------------  [11] 選択系 FSYNC 選択されてる系が(0:SYNC, 1:ASYNC)
#       |  |  |  |  |  +--------------------------------  [10] 選択系 UWERR(1:error, 0:no error)
#       |  |  |  |  |  |  +-----------------------------  [9]  選択系 UWINFO[0]
#       |  |  |  |  |  |  |  +--------------------------  [8]  DIV (0:A, 1:B)
#       |  |  |  |  |  |  |  |                            
#       |  |  |  |  |  |  |  |  +-----------------------  [7] 選択系ADJUST クロック調整（1:あり、0:なし）
#       |  |  |  |  |  |  |  |  |  +--------------------  [6] 選択系RFレベル （1:15dBμV以上、0:15dBμV未満）
#       |  |  |  |  |  |  |  |  |  |  +-----------------  [5] 非選択系  FSYNC (0:chA SYNC, 1:chA ASYNC)
#       |  |  |  |  |  |  |  |  |  |  |  +--------------  [4] 非選択系  UWERR(1:error, 0:no error)
#       |  |  |  |  |  |  |  |  |  |  |  |                
#       |  |  |  |  |  |  |  |  |  |  |  |  +-----------  [3] 非選択系 ADJUST クロック調整（1:あり、0:なし）
#       |  |  |  |  |  |  |  |  |  |  |  |  |  +--------  [2] 非選択系 RFレベル （1:15dBμV以上、0:15dBμV未満）
#       |  |  |  |  |  |  |  |  |  |  |  |  |  |  +-----  [1] RESERVED
#       |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  +--  [0] 使用不可
#       |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
#      +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#      |15:14:13:12|11:10: 9: 8| 7: 6: 5: 4| 3: 2: 1: 0|  <<== Bit Position
#      +--+--+--+--+--+--+--+--+--+--+--+--+--+--:--:--+ */

# i2s FPGA からの I2S ch1  受信 format
#+-----------------------------------------------  [15] 選択系 D[3]
#|  +--------------------------------------------  [14] 選択系 D[2]
#|  |  +-----------------------------------------  [13] 選択系 D[1]
#|  |  |  +--------------------------------------  [12] 選択系 D[0]
#|  |  |  |
#|  |  |  |  +-----------------------------------  [11] 選択系 FSYNC 選択されてる系が(0:SYNC, 1:ASYNC)
#|  |  |  |  |  +--------------------------------  [10] 選択系 UWERR(1:error, 0:no error)
#|  |  |  |  |  |  +-----------------------------  [9]  選択系 UWINFO[0]
#|  |  |  |  |  |  |  +--------------------------  [8]  DIV (0:A, 1:B)
#|  |  |  |  |  |  |  |
#|  |  |  |  |  |  |  |  +-----------------------  [7] 非選択系 D[3]
#|  |  |  |  |  |  |  |  |  +--------------------  [6] 非選択系 D[2]
#|  |  |  |  |  |  |  |  |  |  +-----------------  [5] 非選択系 D[1]
#|  |  |  |  |  |  |  |  |  |  |  +--------------  [4] 非選択系 D[0]
#|  |  |  |  |  |  |  |  |  |  |  |
#|  |  |  |  |  |  |  |  |  |  |  |  +-----------  [3] 非選択系 FSYNC (0:chA SYNC, 1:chA ASYNC)
#|  |  |  |  |  |  |  |  |  |  |  |  |  +--------  [2] 非選択系 UWERR(1:error, 0:no error)
#|  |  |  |  |  |  |  |  |  |  |  |  |  |  +-----  [1] RESERVED
#|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  +--  [0] 使用不可
#|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
#+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#|15:14:13:12|11:10: 9: 8| 7: 6: 5: 4| 3: 2: 1: 0|  <<== Bit Position
#+--+--+--+--+--+--+--+--+--+--+--+--+--+--:--:--+




parser = argparse.ArgumentParser(prog="brave_anlz.py", description="cat with file infomation, TI style")
#parser.add_argument('infile', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
parser.add_argument('infile1', metavar='reference_data_FILE',  help='参照信号')
parser.add_argument('infile2', metavar='observed_data_FILE',  help='観測信号')
parser.add_argument('-i', '--info', action='store_true', help='Print filename and line no')
parser.add_argument('-hex', '--hexstyle', action='store_true', help='treat input as hex')
args = parser.parse_args()

Infile1=open(args.infile1)      #正解データファイル
Infile2=open(args.infile2)      #観測データファイル

print('   \t\t   \t\t   \tsel\tunsl    sel\tunsl sel sel unsl')
print('ref\t\tObs\t\tans\tdat\tdat\tA/B\tsyE\tsyE uwE  UW  uw')
print('-----------------------------------------------------------------------------------')
uw1 = 0
uw2 = 0
uw = 0
uwa1 = 0
uwa2 = 0
uwa = 0
uwb1 = 0
uwb2 = 0
uwb = 0
err = 0
sync = 0
syerA = 0
syerB = 0
uw_info = 0
i = 0
Ans = 0

for l1,l2 in zip(Infile1,Infile2):  #1と2の要素数が異なる場合 zip では多い分は無視 -> itertools.zip_longest

    if(args.info):      # -i
        if(fileinput.isfirstline()):
            print("*** {}".format(fileinput.filename()))
        print("{:6}\t".format(fileinput.filelineno()), end="")

    else:
        #line0 = line.replace('0x', '')  #delete '0x'
        #line0 = '0x'+line.strip()
        #num = (line0.strip())          #改行削除
        line1 = l1.strip()      #正解参照 data
        line2 = l2.strip()      #観測 data

        if(args.hexstyle):   # -hex
            inum1 = int(line1, 16)  #正解参照 data
            inum2 = int(line2, 16)  #観測 data
        else:
            inum1 = int(line1, 10)  #正解参照 data
            inum2 = int(line2, 10)  #観測 data
        s_hnum1 = inum1 ^ 0xAAAA
        s_hnum2 = inum2 ^ 0xAAAA
        #print(hex(s_hnum)+'\t'+'\n', end="")
        #print(hex(s_hnum)+'\t'+'a'+'\n', end="")
        #print(hex(s_hnum)+'\t',hex(f_inum)+'\n', end="")
        #print('0x'+format((s_hnum), '04x')+'\t','0x'+format(inum, '04x')+'\n', end="")
        #print('0x'+format(inum, '04x')+' ','=>  0x'+format((s_hnum), '04x')+'\n', end="")

        #print('0x'+format(inum, '04x')+' ',  
        #        format(X, '04x'), 
        #        '=>  0x'+format((s_hnum), '04x')+'\n', 
        #        end="")

        inum=inum2  #default
        #inum=inum1  #for debug
        unsel_uw =0
        if( (inum & I2S1_RX_UW1_MASK ) ):      #UWINFO[1]
            uw =  ((inum2>>12 )&  0x000F)
            unsel_uw =  ((inum2>>4 )&  0x000F)

        ref_dat=  ((inum1 >>12 ) & 0x000F)
        sel_dat=  ((inum2 >>12 ) & 0x000F)
        unsel_dat=  ((inum2 >>4 ) & 0x000F)
        #chB=  ((inum2 >>1 ) & 0x0007)  
        a_b=  ((inum2 >>8 ) & 0x0001) + 0xA 
        sel_sync= ((inum2 >>11) & 0x0001)
        sel_uwer= ((inum2 >>10) & 0x0001)
        unsel_sync =((inum2 >> 3) & 0x0001)

        uw_info = inum2  & I2S1_RX_UW1_MASK
        if (uw_info!=0):
            i=1
        else:
            i=i+1
            i &= 15

        if (ref_dat != sel_dat):
            err+=1
            Ans =  format(i, '01x')+'!\t'
        else:
            Ans =  format(i, '01x')+'\t'

        print('0x'+format(inum1, '04x')+'\t',       #正解生データ 
                '0x'+format(inum2, '04x')+'\t',     #観測生データ
                Ans ,           #正解の3bit

                format(sel_dat, '01x')+'\t' ,       #選択系data 3bit
                format(unsel_dat, '01x')+'\t' ,     #非選択系data 3bit
                format(a_b, '01X')+'\t' ,           #
                format(sel_sync, '01x')+'\t',       #選択系 同期/非同期
                format(unsel_sync, '01x')+'\t',     #非選択系 同期/非同期
                format(sel_uwer, '01x')+'\t',       #選択系 UW error
                format(uw, '01x')+'\t' ,            #選択系 UW
                format(unsel_uw, '01x')+'\n' ,      #非選択系 UW
                end="")

errate = 100*err/4096
print('Error rate = '+format(errate)+'%')       #4096データ中の誤り率


