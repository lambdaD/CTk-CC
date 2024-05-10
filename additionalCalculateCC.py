class Calculate:
    ToPercentCalculate = lambda num: num/100
    Year_To_Month_Rate_Calculate = lambda rate: rate/12
    Day_To_Month_Rate_Calculate = lambda rate: rate * 365 / 12
    Year_To_Month_Period_Calculate = lambda period: period*12


class Annuity:
    Annuity_Ratio_Calculate = lambda month_rate, period: month_rate/(1-1/((1+month_rate)**period))
    Annuity_Monthly_Payment_Calculate = lambda amount, annuity_ratio: amount*annuity_ratio 
    Is_Annuity_Total_Payment_Execute = lambda monthly_payment, period: monthly_payment * period
    Is_Annuity_Overpayment_Execute = lambda total_payment, amount: total_payment - amount


    def Is_Annuity_Monthly_Payment_Execute(amount, period, rate):
        annuity_ratio = Annuity.Annuity_Ratio_Calculate(rate, period)
        monthly_payment = Annuity.Annuity_Monthly_Payment_Calculate(amount,annuity_ratio)
        total_payment = Annuity.Is_Annuity_Total_Payment_Execute(monthly_payment, period)
        overpayment = Annuity.Is_Annuity_Overpayment_Execute(total_payment, amount)
        return monthly_payment, total_payment, overpayment


class Differentiated:

    def Is_Differentiated_Monthly_Payment_Execute(amount, period, rate):
        monthly_payment = 0
        total_payment = 0
        overpayment = 0
        return monthly_payment, total_payment, overpayment