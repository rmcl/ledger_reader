# Ledger Reader

A simple parser for hledger journal files. It's always fun to play with rply and use a simple grammar. PR's welcome :).

## Example usage

```python

reader = LedgerReader()
journal = reader.parse_file('bank.journal')

for entry in journal:
    print(entry.date, entry.description)
    for transaction in entry.transactions:
        print(f'{transaction.account} {transaction.currency} {transaction.amount}')

    print()

```
