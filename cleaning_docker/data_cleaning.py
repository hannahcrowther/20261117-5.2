import pandas as pd
import os.path
from datetime import datetime

## Create function for loading and cleaning a file

def load_file(
        input_file
):
    df = pd.read_csv(input_file)

    return df

def clean_file(
        df,
        replacements=None
):
    if replacements:
        for column, old_value, new_value in replacements:
            df[column] = df[column].str.replace(
                old_value,
                new_value,
                regex=False
            )
    return df

def quarantine(
        df,
        not_null_columns=None,
        date_columns=None
):
    quarantine_masks = []

    if not_null_columns:
        invalid_rows = df[list(not_null_columns)].isna().any(axis=1)

        quarantine_masks.append(invalid_rows)

    if date_columns:
        for column, fmt in date_columns.items():
            converted_dates = pd.to_datetime(
                df[column],
                format=fmt,
                errors='coerce'
            )

            quarantine_masks.append(
                df[column].notna() & converted_dates.isna()
            )

            df[column] = converted_dates

    
    if quarantine_masks:
        invalid_rows = quarantine_masks[0]

        for mask in quarantine_masks[1:]:
            invalid_rows |= mask

        quarantine = df[invalid_rows]
        df = df[~invalid_rows]
    else:
        quarantine = pd.DataFrame()

    return df, quarantine

def diff_days(
        df,
        start_date,
        end_date
):
    date_difference = df[end_date] - df[start_date]

    df['date_difference'] = date_difference
    
    return df

def output_file(
        df,
        output_file,
        quarantine=None,
        quarantine_file=None
):
    if quarantine_file and not quarantine.empty:
        quarantine.to_csv(quarantine_file, index=False)

    df.to_csv(output_file, index = False)

    return df, quarantine


## SystemBook

if __name__ == "__main__":

    start_time = datetime.now()

    raw_df = load_file(
        input_file="data/03_Library Systembook.csv"
    )

    rows_processed = len(raw_df)

    print(raw_df)

    clean_df = clean_file(
        df = raw_df,
        replacements=[
            ('Book checkout', '"', ''),
            ('Books', 'the kind', 'the king')
        ]
    )

    silver_df, quarantine_df = quarantine(
        df = clean_df,
        not_null_columns=('Id', 'Customer ID'),
        date_columns={
            'Book checkout': '%d/%m/%Y', 
            'Book Returned': '%d/%m/%Y'
            }
    )

    error_count = len(quarantine_df)

    silver_df = diff_days(
        df = silver_df,
        start_date = 'Book checkout',
        end_date = 'Book Returned'
    )

    output_file(
        df = silver_df,
        quarantine = quarantine_df,
        output_file="silver_data/library_systembook_silver.csv",
        quarantine_file="quarantine/library_systembook.csv"
    )

    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()

    log = pd.DataFrame([{
        'Total rows' : rows_processed, 
        'Error rows': error_count,
        'Duration' : duration
        }])

    output_file(
        df = log,
        output_file="log/library_systembook_logs.csv"
    )

    ## SystemCustomer

    start_time = datetime.now()

    raw_df =load_file(
        input_file="data/03_Library SystemCustomers.csv"
    )

    rows_processed = len(raw_df)

    silver_df, quarantine_df = quarantine(
        df = raw_df,
        not_null_columns=('Customer ID', 'Customer Name')
    )

    error_count = len(quarantine_df)

    output_file(
        df = silver_df,
        quarantine = quarantine_df,
        output_file="silver_data/library_systemcustomers_silver.csv",
        quarantine_file="quarantine/library_systemcustomers.csv"
    )

    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()

    log = pd.DataFrame([{
        'Total rows' : rows_processed, 
        'Error rows': error_count,
        'Duration': duration
        }])


    output_file(
        df = log,
        output_file="log/library_systemcustomers_logs.csv"
    )




