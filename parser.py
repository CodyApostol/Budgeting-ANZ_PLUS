import pandas as pd
import re
from datetime import datetime

VALID_MONTHS = {"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"}

def parse_statement(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    transactions = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        parts = line.split()
        
        if len(parts) >= 2:
            day_candidate = parts[0]
            month_candidate = parts[1]

            if day_candidate.isdigit() and month_candidate in VALID_MONTHS:
                try:
                    day = int(day_candidate)
                    month = month_candidate
                    year = "2025"  
                    date = datetime.strptime(f"{day} {month} {year}", "%d %b %Y")

                    amounts = re.findall(r'\$[\d,]+\.\d{2}', line)
                    if len(amounts) >= 1:
                        amount1 = float(amounts[-2].replace('$', '').replace(',', ''))

                        # Remove amounts and date from line to get description
                        line_clean = line
                        for amt in amounts[-1:]:
                            line_clean = line_clean.replace(amt, '').strip()
                        desc = re.sub(r'^\d{1,2} \w{3}', '', line_clean).strip()

                        # Append next line if not Effective Date (likely the address line)
                        if i + 1 < len(lines) and not lines[i + 1].lower().startswith("effective date"):
                            desc += " | " + lines[i + 1].strip()
                            i += 1

                        # Skip if transfer or rounding
                        if re.search(r"TRANSFER FROM|TRANSFER TO|ROUND UP", desc, re.IGNORECASE):
                            i += 1
                            continue

                        # Cleaning description
                        desc = re.sub(r"^.*?\b\d{4}\b\s*", "", desc)
                        desc = re.sub(r"\$\d+(?:\.\d{2})?", "", desc)
                        desc = re.sub(r"\s*\d+\.\d{2}$", "", desc)
                        desc = re.sub(r"/.*", "", desc).strip()
                        desc = desc.strip().rstrip('|').strip()

                        # Split into store and suburb
                        if "|" in desc:
                            store, temp = [part.strip() for part in desc.split("|", 1)]
                        else:
                            store = desc

                        # Remove all numbers from store and suburb
                        store = re.sub(r"\d+", "", store).strip()

                        transactions.append({
                            "Store": store,
                            "Spending": amount1
                        })
                except Exception as e:
                    print(f"[Skipped line {i}] {line}\n  → Reason: {e}")

        i += 1

    return pd.DataFrame(transactions)
