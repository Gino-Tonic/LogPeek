#!/usr/bin/env python3

import argparse
import re
import json
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def parse_log_file(log_path: str, pattern: str) -> list:
    matches = []
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append({
                        "timestamp": datetime.now().isoformat(),
                        "log_line": line.strip()
                    })
    except FileNotFoundError:
        logging.error(f"File not found: {log_path}")
    except PermissionError:
        logging.error(f"Permission denied: {log_path}")
    except IsADirectoryError:
        logging.error(f"Expected a file but found a directory: {log_path}")
    except re.error:
        logging.error(f"Invalid regex pattern: {pattern}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return matches

def save_to_json(matches: list, output_path: str, pattern: str) -> None:
    if not matches:
        logging.warning(f"No matches found for \"{pattern}\" to save.")
        return
    try:
        with open(output_path, 'w') as f:
            json.dump(matches, f, indent=4)
        logging.info(f"{len(matches)} results saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to write to JSON: {e}")

def main():
    parser = argparse.ArgumentParser(description="LogSniff - Simple Log Parser")
    parser.add_argument('--log', required=True, help="Path to the log file")
    parser.add_argument('--pattern', required=True, help="Regex pattern to search for")
    parser.add_argument('--json', help="Optional: output matched lines to a JSON file")
    args = parser.parse_args()

    logging.info(f"Scanning {args.log} for pattern: {args.pattern}")
    matches = parse_log_file(args.log, args.pattern)

    if matches:
        for match in matches:
            logging.info(f"Match found: {match['log_line']}")
    else:
        logging.info("No matches found.")

    if args.json:
        save_to_json(matches, args.json, args.pattern)

if __name__ == "__main__":
    main()