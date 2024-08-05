import pandas as pd

def comma_form(column):
    column = column.str.replace(',', '')
    column = pd.to_numeric(column, errors='coerce')
    return column

def convert_volume(volume):
    if isinstance(volume, str):
        factor = 1
        if volume.endswith('K'):
            factor = 10**3
        elif volume.endswith('M'):
            factor = 10**6
        elif volume.endswith('B'):
            factor = 10**9
        return float(volume[:-1]) * factor
    else:
        return volume

def percent(percent):
    return pd.to_numeric(percent.str.replace('%', '')) / 100

def date_filter(df, start_date_str, end_date_str):
    start_date = pd.to_datetime(start_date_str, dayfirst=True)
    end_date = pd.to_datetime(end_date_str, dayfirst=True)
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    return df.loc[mask]

def clean_dataset(mark):
    mark['Date'] = pd.to_datetime(mark['Date'])
    mark['Price'] = comma_form(mark['Price'])
    mark['Open'] = comma_form(mark['Open'])
    mark['High'] = comma_form(mark['High'])
    mark['Low'] = comma_form(mark['Low'])
    mark['Volume'] = mark['Vol.'].apply(convert_volume)
    mark['Change %'] = percent(mark['Change %'])
    mark['pct_change'] = mark['Change %']
    mark = mark.drop(['Vol.', 'Change %'], axis=1)
    return mark
