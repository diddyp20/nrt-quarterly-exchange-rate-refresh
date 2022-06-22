import requests
import datapackage
import pandas as pd

'''
Script used to extract Exchange rate for the last five years From the Treasury
Website as well as the currency code and store them in  CSV files.
The file will be uploaded into the database
1. Assumption going forward will be to have a country dimension to map the country
to the Country currency code

Author: Didier Bouba Ndengue
Date: 6/20/21
'''


def get_currency_code(output_location):
    # currency code page
    output = f'{output_location}/currency_code.csv'
    data_url = 'https://datahub.io/core/currency-codes/datapackage.json'
    try:
        package = datapackage.Package(data_url)
        resources = package.resources
        for resource in resources:
            if resource.tabular:
                data = pd.read_csv(resource.descriptor['path'])
        # Remove currencies where removal date is not empty
        new_data = data[data['WithdrawalDate'].isna()]
        new_data = new_data[new_data['MinorUnit'] != '-']
        final_data = new_data[new_data['MinorUnit'].notna()]

        # remove all text after bracket
        final_data['country'] = final_data['Entity'].apply(lambda x: x.split('(')[0])
        # delete duplicate
        f = final_data.drop_duplicates(subset=['country'])
        f_data = f[['country', 'Currency', 'AlphabeticCode']]
        # Converting country to upper case
        f_data['country'] = f_data['country'].str.upper()
        f_data.to_csv(output)
    except Exception as ex:
        print(f"Couldn't retrieve the currency code", ex)
        return None


def scrape_treasury_website(year, share_drive):
    # Getting the data from the website
    endpoint = f'/v1/accounting/od/rates_of_exchange?filter=record_date:gt:{year}-01-01&page[number]=1&page[' \
               f'size]=5000'
    api_url = f'https://api.fiscaldata.treasury.gov/services/api/fiscal_service{endpoint}'

    try:

        output_file = f'{share_drive}/fiscal_data.csv'
        data = requests.get(api_url, timeout=3).json()
        data_df = pd.DataFrame(data['data'])
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
    get_currency_code(r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly-exchange'
                      r'-rate-refresh\exchange-rate-scraper\resources')
    scrape_treasury_website(2017, r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly'
                                  r'-exchange-rate-refresh\exchange-rate-scraper\resources')
