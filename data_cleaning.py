import pandas as pd
import os.path

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

def output_file(
        df,
        quarantine,
        output_file,
        quarantine_file
):
    if quarantine_file and not quarantine.empty:
        quarantine.to_csv(quarantine_file, index=False)

    df.to_csv(output_file, index = False)

    return df, quarantine


## SystemBook

df = load_file(
    input_file="data/03_Library Systembook.csv"
)

clean_df = clean_file(
    df = df,
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

output_file(
    df = silver_df,
    quarantine = quarantine_df,
    output_file="silver_data/library_systembook_silver.csv",
    quarantine_file="quarantine/library_systembook.csv"
)


## SystemCustomer

df =load_file(
    input_file="data/03_Library SystemCustomers.csv"
)

silver_df, quarantine_df = quarantine(
    df = df,
    not_null_columns=('Customer ID', 'Customer Name')
)

output_file(
    df = silver_df,
    quarantine = quarantine_df,
    output_file="silver_data/library_systemcustomers_silver.csv",
    quarantine_file="quarantine/library_systemcustomers.csv"
)




