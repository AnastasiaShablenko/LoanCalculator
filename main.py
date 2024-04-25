import argparse
import math
import sys


def calculate_monthly_payment(principal, periods, interest_rate):
    monthly_interest_rate = interest_rate / 100 / 12
    import math
    monthly_payment = math.ceil(principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** periods) / (
            (1 + monthly_interest_rate) ** periods - 1))
    overpayment = int((monthly_payment * periods) - principal)
    return f'Your annuity payment = {monthly_payment}!\nOverpayment = {overpayment}'


def calculate_principal(payment, periods, interest):
    monthly_interest_rate = interest / 100 / 12
    loan_principal = math.floor(payment / (monthly_interest_rate * (1 + monthly_interest_rate) ** periods / (
            (1 + monthly_interest_rate) ** periods - 1)))
    overpayment = int((payment * periods) - loan_principal)
    return f'Your loan principal = {loan_principal}!\nOverpayment = {overpayment}'


def months_to_years_and_months(total_months):
    years = total_months // 12
    remaining_months = total_months % 12
    return years, remaining_months


def format_years_and_months(years, months):
    if years == 0:
        return f'{months} months' if months != 1 else f'{months} month'
    elif years == 1:
        return f'1 year' if months == 0 else f'1 year and {months} months'
    else:
        return f'{years} years' if months == 0 else f'{years} years and {months} months'


def calculate_number_month_pay(principal, payment, interest):
    nominal_interest_rate = interest / (12 * 100)
    number_of_months = math.ceil(
        math.log(payment / (payment - nominal_interest_rate * principal)) / math.log(1 + nominal_interest_rate))
    years, remaining_months = months_to_years_and_months(number_of_months)
    overpayment = int((payment * number_of_months) - principal)
    return f'It will take {format_years_and_months(years, remaining_months)} to repay this loan!\nOverpayment = {overpayment}'


def calculate_differentiated_payments(principal, periods, interest):
    total_payment = 0
    for month in range(1, periods + 1):
        nominal_interest_rate = interest / (12 * 100)
        payment = math.ceil(
            principal / periods + nominal_interest_rate * (principal - principal * (month - 1) / periods))
        total_payment += payment
        print(f"Month {month}: payment is {payment}")

    overpayment = int(total_payment - principal)
    return f'\nOverpayment = {overpayment}'


parser = argparse.ArgumentParser(description="Calculate monthly payment for a loan")

parser.add_argument("--principal", type=float, help="Loan principal amount", required=False)
parser.add_argument("--periods", type=int, help="Number of periods (months)", required=False)
parser.add_argument("--interest", type=float, help="Annual interest rate", required=False)
parser.add_argument("--payment", type=float, help="Monthly payment amount", required=False)
parser.add_argument("--type", type=str, help="Type of payment (annuity or diff)", required=False)

args_parser = parser.parse_args()


def main_func(args):
    if args.type != "diff" and args.type != "annuity" or len(sys.argv) < 4:
        return 'Incorrect parameters.'
    if args.type == "diff" and args.payment is not None:
        return 'Incorrect parameters.'
    if args.interest is None:
        return 'Incorrect parameters.'
    if args.principal is not None and args.principal < 0 or args.periods is not None and args.periods < 0 or args.interest is not None and args.interest < 0 or args.payment is not None and args.payment < 0:
        return 'Incorrect parameters.'
    elif args.type == "diff":
        return calculate_differentiated_payments(args.principal, args.periods, args.interest)
    elif args.periods is None and args.payment is not None:
        return calculate_number_month_pay(args.principal, args.payment, args.interest)
    elif args.payment is None:
        return calculate_monthly_payment(args.principal, args.periods, args.interest)
    elif args.principal is None and args.payment is not None:
        return calculate_principal(args.payment, args.periods, args.interest)


print(main_func(args_parser))