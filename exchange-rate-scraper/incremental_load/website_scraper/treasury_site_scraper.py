import requests
import pandas as pd
from datetime import datetime


def return_quarter(month):
    if month in (1, 2, 3):
        return 1
    elif month in (4, 5, 6):
        return 2
    elif month in (7, 8, 9):
        return 3
    else:
        return 4


# get previous quarter and year
def return_previous_quarter_and_current_year():
    now = datetime.now()
    year = now.strftime("%Y")
    quarter = return_quarter(int(now.strftime("%m")))

    return quarter, year


def scrape_treasury_website(share_drive):
    # Getting the year and the quarter
    quarter, year = return_previous_quarter_and_current_year()
    previous_quarter = quarter - 1
    # Getting the data from the website
    endpoint = f'/v1/accounting/od/rates_of_exchange?filter=record_calendar_quarter:eq:{previous_quarter},record_calendar_year:eq:{year}&page[number]=1&page[size]=5000'
    api_url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service{endpoint}'

    try:

        output_file = f'{share_drive}/incremental_fiscal_data.csv'
        data = requests.get(api_url, timeout=3).json()

        data_df = pd.DataFrame(data['data'])
        print(len(data_df))
        # print(len(data_df))
        # Adding source column
        data_df['curr_source'] = 'Fiscal_Data'
        # Convert country lo upper case
        data_df['country'] = data_df['country'].str.upper()
        # Write exchange rate in the disk
        data_df.to_csv(output_file)

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


if __name__ == "__main__":
    scrape_treasury_website( r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly'
                                  r'-exchange-rate-refresh\exchange-rate-scraper\resources')
