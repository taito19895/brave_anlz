

観測した data の分析をする。

ccs で、エラーが起こった状態で break をかけ、そのときに 4096 の buffer length を持つ
i2s_obs1[4096] の data を save し ~/brave/obs_data/ へ保存。


drwxr-x--x+ 1 toa19895 Domain Users 0 1月  10 11:58   fpga_24	<- fpga 24
fpga_24/id0		uwerr が起こったら即座に A/B 切り替え
fpga_24/id9		uwerr が起こったとき、切り替え先の系が 10個以上連続で正しかったらら系統切り替え

保存した data に対して cygwin term から

% ./brave_anlz.csh ../../brave/obs_data/fpga_24/id9/[s-u]*.dat > anl.dat

してから、anl.dat に対して

% grep Error anl.dat

すると、全観測データごとの Error 率が表示される
