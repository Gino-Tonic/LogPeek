README.md

# A simple log searching tool using python

Features
- Regex-based search in any log file
- Exports matched entries
- Optional JSON export

### Usage
`python3 logsniff.py --log ./sample_logs/auth.log --pattern accepted --json accepted.json`

    --log Path to the log file 
    --pattern Regex pattern to search for
    --json Optional: output matched lines to a JSON file


MIT License – do whatever...