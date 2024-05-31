# CheckPoint_Query_Py
A tool to quickly query a checkpoint management servers logs through the API, populating search terms from a file 

# install

pip install -r requirements.txt

# Usage

with a file (see CVE-2024-24919.txt for example) 
```
python3 searchLogs.py --file test.txt --server mgmt.checkpoint.local --user admin  --password changeme!
```
with a query 
python3 searchLogs.py --query 'blade:firewall and src:192.168.1.2' --server mgmt.checkpoint.local --user admin  --password changeme!

either query or file must be provided 

out is saved to logs.json - can be ingested into other tools quickly

mgmt cert fingerprint on first run is saved to fingerprint.txt

