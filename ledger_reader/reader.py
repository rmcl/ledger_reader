"""A parser for the ledger file format."""
from re import match
from datetime import datetime
from decimal import Decimal
from rply import LexerGenerator, ParserGenerator
from rply.token import Token
from rply.errors import ParsingError

class Journal:
    def __init__(self, entries):
        self.entries = sorted(
            entries, key=lambda e: e.date)

    def __iter__(self):
        """Iterate over entries in the journal."""
        return iter(self.entries)

class Entry:
    def __init__(self, date, description, transactions):
        self.date = date
        self.description = description
        self.transactions = transactions

    def __repr__(self):
        result = f"{self.date}  {self.description}\n"
        for transaction in self.transactions:
            result += f"    {transaction}\n"
        return result

class Transaction:
    def __init__(self, account, currency = None, amount = None):
        self.account = account
        self.currency = currency
        self.amount = amount

    def __repr__(self):
        cur = self.currency if self.currency else ""
        amt = self.amount if self.amount else ""
        return f"{self.account} {cur}{amt}"

class LedgerReader:
    """A parser for the ledger file format."""

    entry_header_re = r"(\d+[/\-]\d+[/-]\d+)\ +(.*)"

    def get_lexer(self):
        lg = LexerGenerator()

        lg.add("ENTRY_HEADER", self.entry_header_re)

        lg.add("CURRENCY", r"EUR|\$")
        lg.add("NUMBER", r"-?\d+(,\d{3})*(\.\d+)?")

        lg.add("ACCOUNT", r"[a-zA-Z][\$\#\w\d\.\,\/\:\-]+")
        lg.add('NEWLINE', r'\n[\ \r\t]*')
        lg.add('WHITESPACE', r'[\ \t]+')

        # Comments - Ignore remainder of line starting with "#".
        lg.ignore(r"\;.*\n")

        lexer = lg.build()
        return lexer


    def get_parser(self):
        tokens = [
            "ENTRY_HEADER",
            "ACCOUNT",
            "CURRENCY",
            "NUMBER",
            "INDENT"

        ]
        pg = ParserGenerator(tokens, precedence=[])

        @pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected. %s" % (token.gettokentype(), token))

        @pg.production("Journal : Entries")
        def main(p):
            return Journal(p[0])


        @pg.production("Entries : Entries Entry")
        def entries(p):
            return p[0] + [p[1]]

        @pg.production("Entries : Entry")
        def entries_single(p):
            return [p[0]]

        @pg.production("Entry : Header Transactions")
        def entry(p):
            return Entry(p[0][0], p[0][1], p[1])

        @pg.production("Transactions : Transactions Transaction")
        def transactions(p):
            return p[0] + [p[1]]

        @pg.production("Transactions : Transaction")
        def transactions_single(p):
            return [p[0]]

        @pg.production("Transaction : INDENT ACCOUNT CURRENCY NUMBER")
        @pg.production("Transaction : INDENT ACCOUNT NUMBER")
        @pg.production("Transaction : INDENT ACCOUNT")
        def transaction(p):
            if len(p) == 4:
                amount = Decimal(p[3].value.replace(',', ''))
                return Transaction(
                    p[1].value.strip(),
                    p[2].value.strip(),
                    amount)
            if len(p) == 3:
                amount = Decimal(p[2].value.replace(',', ''))
                return Transaction(
                    p[1].value.strip(),
                    None,
                    amount)
            else:
                return Transaction(
                    p[1].value,
                    None,
                    None)

        @pg.production("Header : ENTRY_HEADER")
        def header(p):
            results = match(self.entry_header_re, p[0].value.strip())
            entry_date = datetime.strptime(results.group(1).strip(), "%Y-%m-%d")
            return (entry_date, results.group(2).strip())

        parser = pg.build()
        return parser

    def process_whitespace(self, tokens):
        """Given a stream of tokens convert whitespace to INDENT tokens."""

        for token in tokens:
            if token.name == 'WHITESPACE':
                continue
            elif token.name == 'NEWLINE':
                indent_len = len(token.value[1:])
                if indent_len > 0:
                    yield Token('INDENT', indent_len)
            else:
                yield token

    def parse(self, ledger_text : str):
        """Parse a ledger text and return a Journal object."""
        lexer = self.get_lexer()
        parser = self.get_parser()

        tokens = lexer.lex(ledger_text)
        new_tokens = self.process_whitespace(tokens)
        result = parser.parse(new_tokens)
        return result

    def parse_file(self, file_path):
        """Parse a ledger file and return a Journal object."""
        with open(file_path, "r") as fp:
            return self.parse(fp.read())
