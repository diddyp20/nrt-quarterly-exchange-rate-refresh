# nrt-quarterly-exchange-rate-refresh
## PROBLEM
Eastport Analytics has recently won a contract requiring the conversion of multiple foreign
currencies to the U.S. Dollar. Your task is to use opensource data to create a table of quarterly
conversion rates for as many currencies as possible for the past five years. This process must be
repeatable as the table will have to be updated each quarter with the most recent rates.
In order to ensure there is a conversion rate for each quarter and to obtain as many currencies as
possible, at least two different sources must be used. The client has specified that as the U.S.
governments authoritative source for exchange rates, the Treasuries Fiscal Data site must be one of the
sources. The client requires all rates to have an associated currency code (**Note: The treasury site
does not provide currency codes for its conversion rates**). The client has specified that the solution
must not use any paid subscriptions or APIs with associated costs and provided openexchangerates.org
as an example of a free API that may meet the project requirements.
A few additional web sites have been identified as possible sources to scrape rates from, however
you are not limited to these options.
- [Yahoo Finance](https://finance.yahoo.com/quote/EURUSD%3DX/history?period1=1645401600&period2=1653091200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true)
- [XE](https://www.xe.com/currencytables/?from=USD&date=2021-05-01#table-section)
- [Fxtop](https://fxtop.com/en/historical-exchange-rates.php?A=1&C1=USD&C2=EUR&TR=1&MA=1&DD1=01&MM1=01&YYYY1=2001&B=1&P=&I=1&DD2=31&MM2=12&YYYY2=2021&btnOK=Go%21)

The data sources and final conversion rates must be stored in a data repository of your choice. The
final conversion rate table should show at least the currency name, currency code, currency pair (ex:
USDEUR), country responsible for the currency, date of the rate, conversion rate, and the source of the
rate.
You will be presenting the final conversion rates table and an overview of your repository to
Eastport. This is an initial prototype, so you are not required to solve all of the data issues you may
encounter, however you should document the issues and share them in your presentation. Be ready to
discuss your process with the Eastport team.
Expect to spend around two to three hours on this exercise. If you are unable to provide a final
conversion rates table, be ready to discuss what you were able to complete along with your planned
process to complete the task. Please provide your code at least one day prior to the interview. Feel free
to reach out with any questions or clarification you may need.

## Conceptual Architecture
### I. On Premise
#### A. History Load
![image](https://user-images.githubusercontent.com/8740197/174685786-7984b277-2fde-41a4-b286-60c0c6a858e7.png)

