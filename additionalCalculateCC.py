from iflang import *


settings = include_settings()
lang = changeLanguage(settings['language']['user_language'])

class Calculate:
    ToPercentCalculate = lambda num: num/100
    Year_To_Month_Rate_Calculate = lambda rate: rate/12
    Day_To_Month_Rate_Calculate = lambda rate: rate * 365 / 12
    Year_To_Month_Period_Calculate = lambda period: period*12


class Annuity:
    Annuity_Ratio_Calculate = lambda rate, period: (rate * (1 + rate) ** period) / ((1 + rate) ** period - 1)
    Annuity_Monthly_Payment_Calculate = lambda amount, annuity_ratio: amount*annuity_ratio 
    Is_Annuity_Total_Payment_Execute = lambda monthly_payment, period: monthly_payment * period
    Is_Annuity_Overpayment_Execute = lambda total_payment, amount: total_payment - amount


    def Is_Annuity_Monthly_Payment_Execute(amount, period, rate, down_payment=0, one_time_fee=0, monthly_fee=0):
        net_amount = amount - down_payment
        annuity_ratio = Annuity.Annuity_Ratio_Calculate(rate, period)
        monthly_payment = Annuity.Annuity_Monthly_Payment_Calculate(net_amount, annuity_ratio)
        monthly_payment += monthly_fee
        total_payment = Annuity.Is_Annuity_Total_Payment_Execute(monthly_payment, period) + one_time_fee
        overpayment = Annuity.Is_Annuity_Overpayment_Execute(total_payment, amount)
        overpayment_percentage = (overpayment / amount) * 100
        return monthly_payment, total_payment, overpayment, overpayment_percentage


class Differentiated:

    def Is_Differentiated_Monthly_Payment_Execute(amount, period, rate, down_payment=0, one_time_fee=0, monthly_fee=0):
        net_amount = amount - down_payment
        principal_payment = net_amount / period
        monthly_payments = []
        for m in range(1, int(period) + 1):
            interest_payment = net_amount * (1 - (m - 1) / period) * rate
            monthly_payment = principal_payment + interest_payment + monthly_fee
            monthly_payments.append(monthly_payment)
        first_month_payment = monthly_payments[0]
        last_month_payment = monthly_payments[-1]
        total_payment = sum(monthly_payments) + one_time_fee
        overpayment = total_payment - amount
        overpayment_percentage = (overpayment / amount) * 100
        monthly_payment_str = f"{lang['MainResults']['From']} {first_month_payment:.2f} {lang['MainResults']['To']} {last_month_payment:.2f}"
        return monthly_payment_str, total_payment, overpayment, overpayment_percentage