import pdfplumber
import pandas as pd
import re


# check english
def is_english(text):
    try:
        text.encode('ascii')
        return True
    except:
        return False


# check table is english
def is_english_table(df):
    for col in df.columns:
        if not is_english(str(col)):
            return False

    for val in df.iloc[0]:
        if not is_english(str(val)):
            return False

    return True


# SAFE MIN/MAX EXTRACT (NO NULL EVER)
def extract_prices(value):
    if pd.isna(value):
        return 0, 0

    value = str(value)

    # find all numbers
    nums = re.findall(r"\d+", value)

    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    elif len(nums) == 1:
        return float(nums[0]), float(nums[0])
    else:
        return 0, 0


def parse_pdf(file):
    all_data = []

    # get date from filename
    date_match = re.findall(r"\d{4}\.\d{2}\.\d{2}", file)
    file_date = date_match[0] if date_match else None

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:

            table = page.extract_table()
            if not table:
                continue

            df = pd.DataFrame(table)

            # ❌ skip broken tables
            if df.shape[0] < 3:
                continue

           
            # HEADER FIX (2 ROWS)
            
            header1 = df.iloc[0].fillna('')
            header2 = df.iloc[1].fillna('')

            headers = []
            seen = {}

            for h1, h2 in zip(header1, header2):
                col = (str(h1) + " " + str(h2)).strip()

                if col in seen:
                    seen[col] += 1
                    col = f"{col}_{seen[col]}"
                else:
                    seen[col] = 0

                headers.append(col)

            df = df[2:]
            df.columns = headers

            #  only english tables
            if not is_english_table(df):
                continue

            # =========================
            df = df.rename(columns={df.columns[0]: "Item"})
            df = df[df["Item"].notna()]

            
            # CATEGORY DETECT
            
            current_category = None
            clean_rows = []

            for _, row in df.iterrows():
                item = str(row["Item"]).strip()

                #  detect category rows
                if any(x in item for x in ["Vegetable", "Fruits"]):
                    current_category = item
                    continue

                # skip anamalu
                if "Anamalu" in item:
                    continue

                # fix sub-items
                if item.startswith("-"):
                    if clean_rows:
                        prev_item = clean_rows[-1]["Item"]
                        base = prev_item.split("(")[0].strip()
                        item = f"{base} ({item.replace('-', '').strip()})"
                    else:
                        continue

                # clean units
                item = item.replace("(Rs/Kg)", "").replace("(Rs/Fruit)", "").strip()

                row_dict = row.to_dict()
                row_dict["Item"] = item
                row_dict["Category"] = current_category
                clean_rows.append(row_dict)

            if not clean_rows:
                continue

            df = pd.DataFrame(clean_rows)

           
            # LONG FORMAT
           
            df_long = df.melt(
                id_vars=["Item", "Category"],
                var_name="Header",
                value_name="Price"
            )

            
            # DATE
            
            df_long["Date"] = df_long["Header"].str.extract(r"(\d{4}\.\d{2}\.\d{2})")
            df_long["Date"] = df_long["Date"].fillna(file_date)

           
            #  CITY
        
            df_long["City"] = df_long["Header"].str.replace(
                r"\d{4}\.\d{2}\.\d{2}", "", regex=True
            )
            df_long["City"] = df_long["City"].str.replace("Market", "", regex=False)
            df_long["City"] = df_long["City"].str.replace(r"[^A-Za-z ]", "", regex=True)
            df_long["City"] = df_long["City"].str.strip()
            df_long["City"] = df_long["City"].replace("", None)

            # MIN MAX (SAFE FIX)
           
            df_long[["Min", "Max"]] = df_long["Price"].apply(
                lambda x: pd.Series(extract_prices(x))
            )

            
            #  CLEANING
            
            bad_words = ["Average", "Change", "Range"]
            df_long = df_long[
                ~df_long["City"].str.contains('|'.join(bad_words), na=False)
            ]

            df_long = df_long[df_long["Item"].notna()]
            df_long = df_long[df_long["Item"].str.strip() != ""]
            df_long = df_long[~df_long["Item"].str.contains("\n", na=False)]
            df_long = df_long[~df_long["Category"].str.contains("Anamalu", na=False)]

           
            #  FINAL OUTPUT
            
            for i, r in df_long.iterrows():
                uid = f"{r['Date']}_{r['City']}_{r['Item']}_{i}"

                all_data.append({
                    "id": uid,
                    "date": r["Date"] if r["Date"] else None,
                    "city": r["City"] if r["City"] else None,
                    "item": r["Item"],
                    "category": r["Category"],
                    "min_price": float(r["Min"]),
                    "max_price": float(r["Max"])
                })

    return all_data