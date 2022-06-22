"""
1. Connect to the database to the database to get the quarter and year of the max value and max value
    a. if quarter is less than current quarter and year is equal to this year then true
    b. else false
2. if True, get currency code in a dataframe, merge by country, remove fields we dont need
3. append final dataset into table
"""
import pandas as pd
import mysql.connector
from datetime import datetime
from sqlalchemy import create_engine

files_location = r'C:\Users\user\Documents\BndNetworks\Projects\exchangeRate\nrt-quarterly-exchange-rate-refresh' \
                 r'\exchange-rate-scraper\resources'


def return_quarter(month):
    if month in (1, 2, 3):
        return 1
    elif month in (4, 5, 6):
        return 2
    elif month in (7, 8, 9):
        return 3
    else:
        return 4


def merge_exchange_rate_currency_code(df1, df2):
    new_df = df1.merge(df2, how="left", on="country")
    return new_df

def process_and_load_incremental_file(returned_max_id):
    """
    get the file stored in the drive
    call database to get currency code into a dataframe
    merge using country

    :return:
    """
    db_connection_str = 'mysql+pymysql://admin:root@localhost/exchange_rate'
    db_connection = create_engine(db_connection_str)
    inc_file_df = pd.read_csv(f"{files_location}\incremental_fiscal_data.csv")
    inc_file_df.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
    inc_file_df = inc_file_df.where((pd.notnull(inc_file_df)), None)

    exch_rt_df = pd.read_sql('SELECT * FROM currency_code', con=db_connection)
    exch_rt_df.rename(columns={'COUNTRY': 'country', 'ALPHABETICCODE': 'AlphabeticCode'}, inplace=True)
    merged_df = merge_exchange_rate_currency_code(inc_file_df, exch_rt_df)
    final_df = merged_df[merged_df.columns[~merged_df.columns.isin(['id_y', 'currency', 'src_line_nbr', \
                                                                    'effective_date', 'ID'])]]
    # Rename id_x
    final_df.rename(columns={'id_x': 'id'}, inplace=True)
    # Adding Currency Pair
    final_df['currencyPair'] = 'USD' + final_df['AlphabeticCode'].astype(str)
    final_df = final_df.where((pd.notnull(final_df)), None)
    new_id = returned_max_id + 1
    final_df['id'] = new_id + final_df['id'].astype(int)

    tups_exchange = [tuple(x) for x in final_df.to_numpy()]
    query_exchange = ('INSERT INTO EXCHANGE_RATE(ID, record_date,COUNTRY, country_currency_desc, exchange_rate, \
    				record_fiscal_year, record_fiscal_quarter, record_calendar_year, record_calendar_quarter, \
    				record_calendar_month, record_calendar_day, curr_source, CURRENCY, AlphabeticCode, currencyPair ) VALUES\
    				 (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)')
    cnx = mysql.connector.connect(user='admin', password='root', host='localhost', database='exchange_rate',
                                  auth_plugin='mysql_native_password')
    mycur = cnx.cursor()
    mycur.executemany(query_exchange, tups_exchange)
    cnx.commit()
    print('Successfully loaded data in Exchange Rate Table')


# get previous quarter and year
def return_previous_quarter_and_current_year():
    now = datetime.now()
    year = now.strftime("%Y")
    quarter = return_quarter(int(now.strftime("%m")))

    return quarter, year





def get_quarter_from_db(user, password, database):
    cnx = mysql.connector.connect(user=f'{user}', password=f'{password}', host='localhost', database=f'{database}',
                                  auth_plugin='mysql_native_password')

    this_quarter, this_year = return_previous_quarter_and_current_year()
    mycur = cnx.cursor()
    query = "select id, record_calendar_quarter, record_calendar_year from exchange_rate where id = (select max(id) from exchange_rate);"
    mycur.execute(query)
    record = mycur.fetchall()
    cnx.close()

    returned_max_id = record[0][0]
    returned_quarter = record[0][1]
    returned_year = record[0][2]
    print(returned_quarter, returned_year)
    if (int(returned_quarter) < int(this_quarter)) & (int(returned_year) == int(this_year)):
        # process and save dataset
        print('Processing incremental load... Please wait.')
        process_and_load_incremental_file(returned_max_id)
    else:
        print("Quarterly data not available to load!")


get_quarter_from_db('admin', 'root', 'exchange_rate')
