mkdir -p results/
NPROC=`nproc`
for i in `seq $NPROC`
do
    node --single-threaded --max-semi-space_size=128 cli.js > results/webtooling$i.log 2>&1  &
done

wait
grep --color Geometric  results/*.log | awk '{sum+=$3} END {print "mp", sum/NR}'
