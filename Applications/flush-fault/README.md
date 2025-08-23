# Instruction Flush+Fault PoCs

Contains one PoC for the default Flush+Fault (`./flush-fault.c`) and one for the return-based variant (`./flush-ret.c`).


# Run Code
Run `make` then `./flush-fault` or `./flush-ret`.
Afterward, execute `python3 stats.py flush-fault.csv` or `python3 stats.py flush-ret.csv`.

# Works on 
C906,U74,C910,C908


mahreen@mahreen-Precision-3571:~/Downloads/Security-RISC-main/flush-fault$ python3 stats.py flush-fault.csv
median cached:		 1720.0
median uncached:	 1720.0
min cached:		 1718
min uncached:		 1718
Threshold: 1720.0
True Positive: 36
False Positive: 5
True Negative: 18
False Negative: 12
=============================================
Accuracy: 0.75
F1: 0.87
