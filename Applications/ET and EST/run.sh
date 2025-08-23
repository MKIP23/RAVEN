for i in {1..1}
do
make clean && make EST=1
./crun 0 > EST.csv
python3 plot.py EST 1
done
#rerun sim after few seconds if R2 is less than 0.009; value should be around 0.01 greater the better; 
#check monitor cpu usage and writing should be near zero; then run attack
#0    1   2   3   4   5   6   7   8  9   10  11  12   13  14 15
#3    d   2   4   1   8   b   3   5  c    f   c   4    b   b  b
#36  d0  24  46   1d  84  b8  37  5f c0   f9  c0  4c   ba  b6 bb