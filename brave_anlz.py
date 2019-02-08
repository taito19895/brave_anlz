#! /cygdrive/t/cygwin64/home/ito/PycharmProjects/brave_anlz/Scripts/python.exe

#coding:utf-8

import argparse
import fileinput

##################################################################
#from https://qiita.com/wyamamo/items/38789488bc008e9223e6
##################################################################

#  +------------------------------------------------  [15] D[2]
#  |  +---------------------------------------------  [14] D[1]
#  |  |  +------------------------------------------  [13] D[0]
#  |  |  |  +---------------------------------------  [12] FSYNC (0:chB SYNC, 1:chB ASYNC)
#  |  |  |  |  +------------------------------------  [11] UWERR(1:error, 0:no error)  
#  |  |  |  |  |  +---------------------------------  [10] UWINFO[1]                   
#  |  |  |  |  |  |  +------------------------------  [9] UWINFO[0]                   
#  |  |  |  |  |  |  |  +---------------------------  [8] DIV (0:A, 1:B)
#  |  |  |  |  |  |  |  |  +------------------------  [7] DA[2]
#  |  |  |  |  |  |  |  |  |  +---------------------  [6] DA[1]
#  |  |  |  |  |  |  |  |  |  |  +------------------  [5] DA[0]
#  |  |  |  |  |  |  |  |  |  |  |  +---------------  [4] FSYNCA (0:chA SYNC, 1:chA ASYNC)
#  |  |  |  |  |  |  |  |  |  |  |  |  +------------  [3] DB[2]
#  |  |  |  |  |  |  |  |  |  |  |  |  |  +---------  [2] DB[1]
#  |  |  |  |  |  |  |  |  |  |  |  |  |  |  +------  [1] DB[0]
#  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  +---  [0] FSYNCB (0:chB SYNC, 1:chB ASYNC)
#  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
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

print('ref\t\tObs\t\tans\tchA\tchB\tA/B\tsyE\tsyAE\tsyBE\tuwE\tuwA\tuwB\tUW')
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

        #inum=inum2  #default
        inum=inum1  #for debug

        if( (inum1 & 0x0400) ):      #UWINFO[1]
            uw1 =  ((inum1>>11 )&  0x000C)
            uw2 = 0
            uwa1 =  ((inum1>>3 )&  0x000C)
            uwa2 = 0
            uwb1 =  ((inum1<<1 )&  0x000C)
            uwb2 = 0
        elif( (inum & 0x0200) ):    #UWINFO[0]
            uw2 =  ((inum>>14 )&  0x0003)
            uw = (uw1|uw2)
            uwa2 =  ((inum>>6 )&  0x0003)
            uwa = (uwa1|uwa2)
            uwb2 =  ((inum>>2 )&  0x0003)
            uwb = (uwb1|uwb2)

        Ans=  ((inum1 >>13) & 0x0007)  
        chA=  ((inum2 >>5 ) & 0x0007)  
        chB=  ((inum2 >>1 ) & 0x0007)  
        a_b=  ((inum2 >>8 ) & 0x0001) + 0xA 
        sync= ((inum2 >>12) & 0x0001) 
        uwer= ((inum2 >>11) & 0x0001)
        syerA =((inum2 >> 4) & 0x0001)
        syerB =((inum2 >> 0) & 0x0001)


        if (a_b == 0xA):        #A系統選択
            if (Ans != chA):
                err+=1
                Ans =  format(Ans, '01x')+'!\t'
            else:
                Ans =  format(Ans, '01x')+'\t'
        else:                   #B系統選択
            if (Ans != chB):
                err+=1
                Ans =  format(Ans, '01x')+'!\t'
            else:
                Ans =  format(Ans, '01x')+'\t'

        print('0x'+format(inum1, '04x')+'\t',       #正解生データ 
                '0x'+format(inum2, '04x')+'\t',     #観測生データ
                Ans ,           #正解の3bit
                format(chA, '01x')+'\t' ,           #chA 3bit
                format(chB, '01x')+'\t' ,           #chB 3bit
                format(a_b, '01X')+'\t' ,           #
                format(sync, '01x')+'\t',           #
                format(syerA, '01x')+'\t',           #
                format(syerB, '01x')+'\t',           #
                format(uwer, '01x')+'\t',           #
                format(uwa, '01x')+'\t' ,           #
                format(uwb, '01x')+'\t' ,           #
                format(uw, '01x')+'\n' ,            #
                end="")

errate = 100*err/4096
print('Error rate = '+format(errate)+'%')       #4096データ中の誤り率


