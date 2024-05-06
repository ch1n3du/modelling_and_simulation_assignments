from enum import Enum
from typing import Any, Tuple, List
import numpy as np
import termplotlib as tpl

next_payment_id = 0
repl_output_padding = "    "

header =  """
================================================
 Welcome to Riba (v0.1)?
================================================
 Welcome to Riba (v0.1)?
 Type 'q' or 'quit' to exit.
 Type '?' or 'help' to list the commands.
================================================
    """

commands = """
 Commands
================================================
 [0] - ⏩ Fast forward a month
 [1] - 🐥 Create a user
 [2] - 📜 List all users
 [3] - 📃 Create a loan
 [4] - 📜 List all loans
 [5] - 💵 Make a loan payment
 [6] - 📜 List all loan payments
 [7] - 📊 List all loan balances
 [8] - 🔮 Predict monthly payments"""

exit_message = " Goodbye and thanks for all the fish :) ><> ><> ><>"

   

class Command(Enum):
    IncrementMonth         = 0
    CreateUser             = 1
    ListUsers              = 2
    CreateLoan             = 3
    ListLoans              = 4
    MakeLoanPayment        = 5
    ListLoanPayments       = 6
    ListLoanBalances       = 7
    PredictMonthlyPayments = 8

class Loan:
    name: str 
    amount: float
    interest_rate: float
    creator: str
    month_created: int
    is_fixed_interest: bool
    is_finished: bool

    def __init__(self, name: str, amount: float, interest_rate: float, creator: str, month_created: int, is_fixed_interest: bool):
        self.name = name
        self.amount = amount
        self.interest_rate = interest_rate
        self.creator = creator
        self.month_created = month_created
        self.is_fixed_interest = is_fixed_interest

class LoanPayment:
    id: int
    loan_name: int
    amount: float
    creator: str
    month_created: int

    def __init__(self, id: int, amount: float, loan_name: int, user_id: str, month_created: int):
        self.id = id
        self.loan_name = loan_name
        self.amount = amount
        self.user_id = user_id
        self.month_created = month_created

def format_text(text: str, width: int) -> str:
    text_len = len(text)
    if text_len > width:
        return text[:width-3] + "..."
    elif text_len < width:
        return text + (" " * (width - text_len))
    else:
        return text

class Interpreter:
    month_counter: int
    users: List[str]
    loans: List[Loan]
    loan_payments: [LoanPayment]

    def __init__(self):
        self.month_counter  = 0
        self.users          = []
        self.loans          = []
        self.loan_payments  = []

    def increment_month_counter(self):
        self.month_counter += 1

    def create_user(self, username: str):
        self.users.append(username)

    def create_loan(self, name: str, creator: str, amount: float, interest_rate: float, is_fixed_interest: bool):
        loan = Loan(
            name,
            creator,
            amount,
            interest_rate,
            self.month_counter,
            is_fixed_interest,
        )
        self.loans.append(loan)
    
    def make_loan_payment(self, loan_name: str, username: str, amount: float):
        payment = LoanPayment(
            id=len(self.loan_payments), 
            amount=amount, 
            loan_name=loan_name,
            user_id=username,
            month_created=self.month_counter
        )
        self.loan_payments.append(payment)

    def check_finished_loans(self):
        for index, loan in enumerate(self.loans):
            if loan.is_finished: continue

            loan_balance = self.check_loan_balance(loan)
            if loan_balance >= 0:
                loan.is_finished = True 

    def check_monthly_totals(self) -> [float]:
        number_of_months: int = self.month_counter
        monthly_totals: int = [0] * (number_of_months+1)

        print(f"{monthly_totals}")
        
        for payment in self.loan_payments:
            print(f"{payment.month_created}")
            monthly_totals[payment.month_created] += payment.amount

        print(f"{monthly_totals}")

        return monthly_totals



    def check_loan_balance(self, loan: Loan) -> float:
        payments = list(filter(
            lambda payment: payment.loan_name == loan.name,
            self.loan_payments
        ))

        number_of_months: int = self.month_counter - loan.month_created
        monthly_totals: int = [0] * number_of_months
        
        for payment in payments:
            monthly_totals[payment.month_created] += payment.amount

        if loan.is_fixed_interest:
            # Checking fof fixed interest loans

            monthly_interest = loan.amount * loan.interest_rate
            total_interest = last_month * number_of_months

            amount_to_be_paid = loan.amount + total_interest
            amount_paid = sum(monthly_totals)
            balance = amount_paid - amount_to_be_paid
            if balance < 0:
                # If the loan isn't yet complete return the amount left
                return (False, balance)
            else:
                # If the loan is complete return the amount carried over
                return (True, balance)
        else:
            growth_rate = 1 + (loan.interest_rate / 100)

            total_amount_paid = sum(monthly_totals)
            valid_amount_paid = 0
            amount_to_be_paid = loan.amount * growth_rate

            for month in range(number_of_months):
                monthly_total = monthly_totals[month]

                valid_amount_paid += monthly_total
                amount_to_be_paid -= monthly_total

                if amount_to_be_paid <= 0:
                    extra_paid = abs(amount_to_be_paid)
                    valid_amount_paid -= extra_paid
                    return (True, total_amount_paid - valid_amount_paid)
            return total_amount_paid - amount_to_be_paid
        
    def loan_is_finished(self, loan: Loan) -> bool:
        if self.check_loan_balance(loan) >= 0:
            return True
        
    def interpret_command(self, command: Command):
        match command:
            case Command.IncrementMonth:
                self.increment_month_counter()
                print(f"{repl_output_padding}Month Counter: {self.month_counter}")

            case Command.CreateUser:
                username = input(f"{repl_output_padding}Enter a username: ")
                self.create_user(username)

            case Command.ListUsers:
                print(f"{repl_output_padding}| S/N | Username |")

                for (i, username) in enumerate(self.users):
                    username = format_text(username, len("Username"))
                    print(f"{repl_output_padding}| {i:03d} | {username} |")

            case Command.CreateLoan:
                loan_name         = input(f"{repl_output_padding}What is the name of the loan? ")
                creator           = input(f"{repl_output_padding}Who is the loan creator? ")
                amount            = float(input(f"{repl_output_padding}What is the loan amount? "))
                interest_rate     = float(input(f"{repl_output_padding}What is the interest rate? "))
                is_fixed_interest = input(f"{repl_output_padding}Is the interest rate fixed? ").lower().strip() == "yes"

                self.create_loan(
                    name=loan_name,
                    creator=creator,
                    amount=amount,
                    interest_rate=interest_rate,
                    is_fixed_interest=is_fixed_interest
                )

            case Command.ListLoans:
                print(f"{repl_output_padding}| S/N | Loan Name            |")
                for (i, loan) in enumerate(self.loans):
                    loan_name = format_text(loan.name, len("Loan Name          "))
                    print(f"{repl_output_padding}| {i:03d} | {loan_name} |")

            case Command.MakeLoanPayment:
                loan_name         = input(f"{repl_output_padding}What is the name of the loan? ")
                creator           = input(f"{repl_output_padding}Who is making the payment? ")
                amount            = float(input(f"{repl_output_padding}How much do you wish to pay? "))

                self.make_loan_payment(
                    loan_name=loan_name,
                    username=creator,
                    amount=amount
                )

            case Command.ListLoanPayments:
                print(f"{repl_output_padding}| S/N | Loan Name | Payment Amount |")
                for payment in self.loan_payments:
                    loan_name = format_text(payment.loan_name, len("Loan Name"))
                    amount = payment.amount
                    print(f"{repl_output_padding}| {payment.id:03d} | {loan_name} | {amount:014d}")

            case Command.ListLoanBalances:
                print(f"{repl_output_padding}| S/N | Loan Name | Loan Balance |")
                for (i, loan) in enumerate(self.loans):
                    loan_name = format_text(loan.name, len("Loan Name"))
                    balance = self.check_loan_balance(loan)
                    print(f"{repl_output_padding}| {i:03d} | {loan_name} | {balance:012d}")

            case Command.PredictMonthlyPayments:
                duration = int(input(f"{repl_output_padding}How many months do you wish to predict?"))
                monthly_totals = self.check_monthly_totals()
                number_of_months = len(monthly_totals)

                # Simple linear regression
                regression = np.polynomial.Polynomial.fit(
                    [x for x in range(number_of_months)],
                    monthly_totals,
                    1
                )

                monthly_totals += [regression(x) for x in range(number_of_months, number_of_months+duration)]

                figure = tpl.figure()

                figure.plot(
                    list(range(len(monthly_totals))),
                    monthly_totals,
                )
                figure.show()


def main():
    interpreter = Interpreter()

    print(header)
    print(commands)

    figure = tpl.figure()
    figure.plot([1, 2, 3], [2, 4, 8])
    figure.show()

    while True:
        user_input = input("riba> ").strip().lower()
        if user_input == 'q' or user_input == 'quit':
            print(exit_message)
            return

        if user_input == '?' or user_input == 'help':
            print(commands)
            continue

        command_code = int(user_input)
        command = Command(command_code)

        interpreter.interpret_command(command)

