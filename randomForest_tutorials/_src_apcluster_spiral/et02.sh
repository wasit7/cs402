#!/bin/bash
Aclmax=(""500")
Aspc=("1e1" "1e2" "1e3")

for spc in ${Aspc[@]}
do
	for clmax in ${Aclmax[@]}
	do
        rm -rf sp_${clmax}_${spc}
        mkdir sp_${clmax}_${spc}
        run="ipython scmain.py sp_${clmax}_${spc} >> sp_${clmax}_${spc}/log"
        tt=$(date +"%y%m%d_%H%M_%S")
		echo ">>>start:${tt}, spc:${spc}, clmax:${clmax} "
    	echo "$run"
    	eval "$run"
    	tt=$(date +"%y%m%d_%H%M_%S")
    	echo "     end:${tt}"
    done
done

