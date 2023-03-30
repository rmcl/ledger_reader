from unittest import TestCase
from datetime import datetime
from .reader import LedgerReader

class LedgerReaderTestCase(TestCase):

    def test_read_ledger(self):
        reader = LedgerReader()
        journal = reader.parse(JOURNAL_EX_1)

        self.assertEqual(len(journal.entries), 2)
        self.assertEqual(journal.entries[0].date, datetime(2020, 1, 2, 0, 0))
        self.assertEqual(journal.entries[0].description, "Investment in Equity Fund VI, LLC")
        self.assertEqual(len(journal.entries[0].transactions), 2)
        self.assertEqual(journal.entries[0].transactions[0].account, "assets:bank:boa:cashflow-123")
        self.assertEqual(journal.entries[0].transactions[0].amount, -5000)
        self.assertEqual(journal.entries[0].transactions[1].account, "assets:funds:cardone:awes123")
        self.assertEqual(journal.entries[0].transactions[1].amount, None)

        self.assertEqual(journal.entries[1].date, datetime(2022, 3, 16, 0, 0))
        self.assertEqual(journal.entries[1].description, "Investment in CC REIT")
        self.assertEqual(len(journal.entries[1].transactions), 2)
        self.assertEqual(journal.entries[1].transactions[0].account, "assets:capital-call:cardone")
        self.assertEqual(journal.entries[1].transactions[0].amount, -1000)
        self.assertEqual(journal.entries[1].transactions[1].account, "assets:funds:carbone:cc-reit-1")
        self.assertEqual(journal.entries[1].transactions[1].amount, None)



JOURNAL_EX_1 = """
;comment
2020-01-02 Investment in Equity Fund VI, LLC
    assets:bank:boa:cashflow-123   $-5,000
    assets:funds:cardone:awes123

; comment

2022-03-16 Investment in CC REIT
    assets:capital-call:cardone   $-1000
    assets:funds:carbone:cc-reit-1

"""
