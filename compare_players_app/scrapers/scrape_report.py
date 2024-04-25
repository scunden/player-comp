import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_scouting_report(url):
    df = get_raw_report(url)
    df = clean_raw_report(df)
    df = parse_categories(df)
    return df

def get_raw_report(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all table elements
    tables = soup.find_all('table')
    
    # Loop through each table
    for table in tables:
        # Attempt to find a caption for the table
        caption = table.find('caption')
        if caption is None:
            # If no caption is found, check for the closest preceding header (h1, h2, h3, etc.)
            for sibling in table.previous_siblings:
                if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    caption = sibling.text.strip()
                    break
        
        # Use caption text or a default name if caption is not found
        
        if caption:
            table_name = caption if isinstance(caption, str) else caption.text.strip()
            table_name = table_name.replace('/', ' or ')  # Replace problematic characters in file names
            if "Complete" in table_name:
        
                # Convert the table to a DataFrame
                df = pd.read_html(str(table))[0]
    return df

def clean_raw_report(df):
    df = df[~(df.isnull().all(axis=1))]
    df = df[~df.apply(lambda row: all(row[col] == col[1] for col in df.columns), axis=1)]
    return df

def generate_category_range(df_cat):
    range_dict = {}
    prev_key = None
    for key, value in df_cat.items():
        if prev_key is not None:
            range_dict[(prev_key, key)] = df_cat[prev_key]
        prev_key = key
        
    # Assuming the DataFrame does not exceed the maximum index from series
    range_dict[(prev_key, float('inf'))] = df_cat[prev_key]
    return range_dict

def extract_categories(df):
    df_cat = df[df.apply(identify_categories, axis=1)]
    row = pd.DataFrame(data=[["Standard","Standard","Standard"]], columns=df.columns, index=[0])
    df_cat = pd.concat([df_cat, row]).sort_index()
    df_cat.columns = [x[1] for x in df_cat.columns]
    df_cat = df_cat.Statistic
    
    return df_cat


def identify_categories(row):
    return all(x == row.iloc[0] for x in row)

def map_category(index, cat_range):
    for (start, end), category in cat_range.items():
        if start <= index < end:
            return category
    return None  # in case no category matches

def parse_categories(df):
    df_cat = extract_categories(df)
    cat_range = generate_category_range(df_cat)

    # Apply the function to the index of df to create a new column
    df['Category'] = df.index.map(lambda x: map_category(x, cat_range))
    df = df.drop(index=df_cat.index)
    df.columns = [x[1] if x[1]!="" else x[0] for x in df.columns]
    return df
