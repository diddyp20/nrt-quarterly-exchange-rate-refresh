import mysql.connector
import pandas as pd


def read_data_from_share(drive_location, file_name):
    curr_cd_df = pd.read_csv(f'{drive_location}/{file_name}.csv')
    # exch_rt_df = pd.read_csv(f'{drive_location}/fiscal_data.csv')
    curr_cd_df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    # exch_rt_df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    return curr_cd_df


def load_data_db(user, password, database):
    files_location = r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly-exchange-rate-refresh' \
                     r'\exchange-rate-scraper\resources'
    cnx = mysql.connector.connect(user=f'{user}', password=f'{password}', host='localhost', database=f'{database}',
                                  auth_plugin='mysql_native_password')
    mycur = cnx.cursor()

    # Loading data from Currency Table
    curr_cd_df = read_data_from_share(files_location, 'currency_code')
    tups = [tuple(x) for x in curr_cd_df.to_numpy()]
    print(tups)
    query_curr_cd = ('INSERT INTO CURRENCY_CODE(ID, COUNTRY, CURRENCY, ALPHABETICCODE) VALUES (%s, %s, %s, %s)')

    # History load for exchange Rate
    exch_rate_df = read_data_from_share(files_location, 'fiscal_data')
    exch_rate_df = exch_rate_df.where((pd.notnull(exch_rate_df)), None)
    tups_exchange = [tuple(x) for x in exch_rate_df.to_numpy()]
    query_exchange = ('INSERT INTO EXCHANGE_RATE(ID, record_date,COUNTRY, CURRENCY, country_currency_desc, exchange_rate, effective_date, \
    				src_line_nbr,record_fiscal_year, record_fiscal_quarter, record_calendar_year, record_calendar_quarter, record_calendar_month,\
    				 record_calendar_day, curr_source ) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s )')
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
