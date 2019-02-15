#!/bin/csh -f

set a=`getopt u:l: $*`
set c=`getopt u:l: $*`

echo "set a=$a"

if  ($#argv == 0) then
	echo "useage: % command  ok.dat  * "
	exit
endif

foreach arg ($a)
	switch ($arg)

		case -u:  #unique word
			set UW=$c[2]
			shift c; shift c
		breaksw
		case -l:  #length
			set LENGTH=$c[2]
			shift c; shift c
		breaksw
	endsw
end


shift c
foreach file ($c)
	echo ""

	./brave_anlz.py -hex \
	../../brave/obs_data/fpga_24/id0/ok.dat $file
#	../../brave/obs_data/fpga_24/id0/$file

end
