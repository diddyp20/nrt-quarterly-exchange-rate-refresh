import mysql.connector
import pandas as pd

files_location = r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly-exchange-rate-refresh' \
                 r'\exchange-rate-scraper\resources'

''' 
Function used to read the files from the shareDrive
'''


def read_data_from_share(drive_location, file_name):
    curr_cd_df = pd.read_csv(f'{drive_location}/{file_name}.csv')
    curr_cd_df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    return curr_cd_df


''' Function used to merge exchange rate with currency code
in order to have currency code and currency pair'''


def merge_exchange_rate_currency_code(df1, df2):
    new_df = df1.merge(df2, how="left", on="country")
    return new_df


def load_data_db(user, password, database):
    cnx = mysql.connector.connect(user=f'{user}', password=f'{password}', host='localhost', database=f'{database}',
                                  auth_plugin='mysql_native_password')
    mycur = cnx.cursor()

    # Loading data from Currency Table
    curr_cd_df = read_data_from_share(files_location, 'currency_code')
    tups = [tuple(x) for x in curr_cd_df.to_numpy()]

    query_curr_cd = ('INSERT INTO CURRENCY_CODE(ID, COUNTRY, CURRENCY, ALPHABETICCODE) VALUES (%s, %s, %s, %s)')

    # History load for exchange Rate
    exch_rate_df = read_data_from_share(files_location, 'fiscal_data')
    exch_rate_df = exch_rate_df.where((pd.notnull(exch_rate_df)), None)
    merged_df = merge_exchange_rate_currency_code(exch_rate_df, curr_cd_df)
    final_df = merged_df[merged_df.columns[~merged_df.columns.isin(['id_y', 'currency', 'src_line_nbr', \
                                                                    'effective_date'])]]
    # Rename id_x
    final_df.rename(columns={'id_x': 'id'}, inplace=True)
    # Adding Currency Pair
    final_df['currencyPair'] = 'USD' + final_df['AlphabeticCode'].astype(str)
    final_df = final_df.where((pd.notnull(final_df)), None)

    tups_exchange = [tuple(x) for x in final_df.to_numpy()]
    # print(tups_exchange)
    query_exchange = ('INSERT INTO EXCHANGE_RATE(ID, record_date,COUNTRY, country_currency_desc, exchange_rate, \
				record_fiscal_year, record_fiscal_quarter, record_calendar_year, record_calendar_quarter, \
				record_calendar_month, record_calendar_day, curr_source, CURRENCY, AlphabeticCode, currencyPair ) VALUES\
				 (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)')
    try:
        mycur.executemany(query_curr_cd, tups)
        cnx.commit()
        print('Successfully loaded data in Currency Rate Table')
        mycur.executemany(query_exchange, tups_exchange)
        cnx.commit()
        print('Successfully loaded data in Exchange Rate Table')
    except Exception as e:
        print('Error while inserting to MySql', e)
        cnx.close()


if __name__ == "__main__":
    load_data_db('admin', 'root', 'exchange_rate')
