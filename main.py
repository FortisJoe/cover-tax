import argparse
import decimal
import logging

from decimal import Decimal, ROUND_DOWN, ROUND_UP


class CLI:
    def __init__(self):

        self.args = None
        self.requirement = None
        self.tax_rate = None
        self.tolerance = None

        logging.basicConfig(level=logging.INFO)
        self.init_argparse()

    def init_argparse(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--money_required',
            dest='requirement',
            required=True,
            help='The value required to be raised before taxes, in decimal '
                 'format with 2 decimal places',
        )

        parser.add_argument(
            '--tax_rate',
            dest="tax_rate",
            required=True,
            help='The tax rate in decimal format',
        )

        parser.add_argument(
            '--tolerance',
            dest='tolerance',
            required=False,
            help='The tolerance of how much extra tax you are willing to pay',
        )

        self.args = parser.parse_args()

        try:
            self.requirement = Decimal(self.args.requirement).quantize(
                Decimal('.01'), rounding=ROUND_DOWN
            )
        except decimal.InvalidOperation:
            parser.error("The input value for money required is not a number.")

        try:
            self.tax_rate = Decimal(self.args.tax_rate)
        except decimal.InvalidOperation:
            parser.error("The input value for tax rate is not a number.")

        if self.args.tolerance:
            try:
                self.tolerance = Decimal(self.args.tolerance)
            except decimal.InvalidOperation:
                parser.error("The input value for tolerance is not a number.")
        else:
            self.tolerance = Decimal(0.01)

    def process(self):
        initial_tax = self.requirement * (self.tax_rate/100)
        total = self.calculate(self.requirement + initial_tax, initial_tax)
        total.quantize(
                Decimal('.01'), rounding=ROUND_UP
            )
        logging.info(f"You need to take out {'{:.2f}'.format(total)} to have "
                     f"{self.requirement} to cover {self.tax_rate}% tax rate "
                     f"and pay less than {'{:.2f}'.format(self.tolerance)} "
                     f"yourself.")

    def calculate(self, total, last_tax):
        tax = last_tax * (self.tax_rate/100)
        total += tax
        if tax > self.tolerance:
            return self.calculate(total, tax)
        return total


if __name__ == '__main__':
    cli = CLI()
    cli.process()
