import re
import pandas as pd

def validate_gst(gst_id):
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_id))

def detect_duplicates(df):
    return df[df.duplicated(subset=['invoice_number'], keep=False)]