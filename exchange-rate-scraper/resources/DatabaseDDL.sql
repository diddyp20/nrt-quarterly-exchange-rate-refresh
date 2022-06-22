DROP TABLE EXCHANGE_RATE;
DROP TABLE currency_code;

DROP TABLE IF EXISTS currency_code;
create table currency_code(
ID INT NOT NULL,
COUNTRY VARCHAR(80) NOT NULL,
CURRENCY VARCHAR(40),
ALPHABETICCODE VARCHAR(5),
PRIMARY KEY(COUNTRY));

DROP TABLE IF EXISTS EXCHANGE_RATE;
CREATE TABLE EXCHANGE_RATE(
ID INT NOT NULL, record_date VARCHAR(15), COUNTRY VARCHAR(80),
 country_currency_desc VARCHAR(80), exchange_rate VARCHAR(30),
record_fiscal_year VARCHAR(10), record_fiscal_quarter VARCHAR(5), record_calendar_year VARCHAR(5), record_calendar_quarter VARCHAR(5), record_calendar_month VARCHAR(2), record_calendar_day VARCHAR(2), curr_source VARCHAR(20),currency VARCHAR(40), AlphabeticCode VARCHAR(10),
currencyPair VARCHAR(10),
PRIMARY KEY(ID));