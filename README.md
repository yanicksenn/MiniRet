# How to use

1. Run `prepare_documents.py`
1. Run `prepare_queries.py`
1. Run `miniret.py` with languange (german, french, etc.) and the length of the ranking (> 0)
    ```shell
   # E.g.
   python3 miniret.py german 10
   python3 miniret.py french 100
   python3 miniret.py latin 1000
   ```