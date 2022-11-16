N=`nproc`
for i in $(seq 1 $N);
do
  php $1 > result-$i.log &
done

wait

grep Total result-*.log | awk -v n=$N -v b=$1 '{sum += $2} END {print b " " n/sum}'

rm -rf result-*.log
