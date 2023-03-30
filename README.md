# Ledger Reader

A simple parser for hledger journal files. It's always fun to play with rply and use a simple grammar. PR's welcome :).

## Example usage


### Read a journal

```python

reader = LedgerReader()
journal = reader.parse_file('bank.journal')

for entry in journal:
    print(entry.date, entry.description)
    for transaction in entry.transactions:
        print(f'{transaction.account} {transaction.currency} {transaction.amount}')

    print()

```

### Append to a journal


```python
from datetime import date
from ledger_reader import Entry, Transaction

entry = Entry(
    date(2022, 3, 5),
    'Cash Transfer',
    transactions=[
        Transaction('assets:bank:boa:checking', '$', -5000),
        Transaction('assets:bank:boa:savings')
    ]
)

with open('bank.journal', 'a') as fp:
    fp.write(f'\n{entry}')
```
