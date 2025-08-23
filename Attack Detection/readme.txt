source venv/bin/activate
python3 extract_metrics.py
cd grepped
python3 ML_stats_best.py
python3 ML_stats_test.py

