import locale
from datetime import datetime, date
import re
from factor import Factor
#
locale.setlocale(locale.LC_ALL, '')

class RMD():
    def __init__(self):
        self.format_date = "%m/%d/%Y"
        self.today = date.today()

    def create_date_object(self, unformated_date):
        return datetime.strptime(unformated_date, self.format_date).date()

    def format_account_value(self, value):
        return re.sub("[^0-9]", "", value)

    def age_calculator(self, date_of_birth):
        date_of_birth_object = self.create_date_object(date_of_birth)
        age = self.today.year - date_of_birth_object.year - ((self.today.month, self.today.day) < (date_of_birth_object.month, date_of_birth_object.day))
        return age

    def age_at_time_of_death(self, date_of_birth, date_of_death):
        date_of_birth_object = self.create_date_object(date_of_birth)
        date_of_death_object = self.create_date_object(date_of_death)
        age = date_of_death_object.year - date_of_birth_object.year - ((date_of_death_object.month, date_of_death_object.day) < (date_of_birth_object.month, date_of_birth_object.day))
        return age

    def rmd_dist_owner_vs_bene(self, bene_date_of_birth_object, date_of_birth_of_deceased_object, bene_age_year_after_death, prior_year_account_value, factor_adjustment):
        print(bene_date_of_birth_object, date_of_birth_of_deceased_object, bene_age_year_after_death)
        if bene_date_of_birth_object > date_of_birth_of_deceased_object:
            factor = (Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")) - factor_adjustment
            required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                            grouping=True)
            return f"The required minimum distribution is {required_minimum_distribution} using the factor of {factor}"
        else:
            factor = (Factor.all_tables(self, age=0, table="TableI")) - factor_adjustment
            required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                            grouping=True)
            return f"The required minimum distribution is {required_minimum_distribution} using the factor of {factor}"

    def calculate_traditional_ira_rmd(self, date_of_birth, prior_year_account_value, spouse_date_of_birth=None, marital_status=None, sole_beneficiary=None):
        try:
            age = self.age_calculator(date_of_birth)
            rmd_age = 73 if self.today.year > 2022 and self.today.year < 2033 else 75
            account_value = self.format_account_value(prior_year_account_value)
            if age < rmd_age:
                return f"RMD's aren't required until the year you turn {rmd_age}."

            if spouse_date_of_birth:
                spouse_age = self.age_calculator(spouse_date_of_birth)
                age_difference = age - spouse_age

            if marital_status == "Married" and sole_beneficiary == "Yes" and age_difference >= 10:
                factor = Factor.all_tables(self, age=str(age), spouse_age=int(spouse_age), table="TableII")
                required_minimum_distribution = locale.currency(float(account_value) / float(factor), grouping=True)
                return (f"The required minimum distribution is {required_minimum_distribution} using the factor of {factor}\n"
                    f"Based on the Table II for use by owners whose spouses are more than 10 years younger and are the \n"
                    f"sole beneficiaies of their IRAs.")

            elif marital_status != "Married" or marital_status == "Married" and age_difference < 10 or marital_status == "Married" and sole_beneficiary == "No":
                factor = Factor.all_tables(self, age=str(age), table="TableIII")
                required_minimum_distribution = locale.currency(float(account_value) / float(factor), grouping=True)
                return (f"The required minimum distribution is {required_minimum_distribution} using the factor of {factor} \n"
                        f"Using the Table III Uniform Lifetime table for Unmarried owners, married owners whose spouses aren't more than 10 years younger,\n and"
                        f"Married owners whose spouses aren't the sole beneficiaries of the their IRA.")

            else:
                return "-----ERROR SOMETHING WENT WRONG-----"
        except:
            return exception
        # TODO Need to add Successor Bene situation as well
    def calculate_inherited_ira_rmd(self, beneficiary_date_of_birth, prior_year_account_value, date_of_death, date_of_birth_of_deceased, beneficiary_type):
        prior_year_account_value = self.format_account_value(prior_year_account_value)
        bene_date_of_birth_object = self.create_date_object(beneficiary_date_of_birth)
        date_of_death_object = self.create_date_object(date_of_death)
        age_of_deceased_at_death = self.age_at_time_of_death(date_of_birth_of_deceased, date_of_death)
        bene_age_year_after_death = (self.age_at_time_of_death(beneficiary_date_of_birth, date_of_death)) + 1
        factor_adjustment = self.today.year - (date_of_death_object.year + 1)
        date_of_birth_of_deceased_object = self.create_date_object(date_of_birth_of_deceased)

        if date_of_death_object.year < 2020:
            rmd_age = True if age_of_deceased_at_death >= 70.5 else False
            if rmd_age:
                if beneficiary_type == "Spouse":
                    factor = Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                                    grouping=True)
                    return f"Take annual distributions based on their own life expectancy which would be {required_minimum_distribution} using the factor of {factor}."

                elif beneficiary_type != "Spouse" and beneficiary_type != "Estate named the Beneficiary":
                    factor = (Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")) - factor_adjustment
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor, grouping=True)
                    return f"Take annual distributions based on their own life expectancy which would be {required_minimum_distribution} using the factor of {factor}, or Follow the 5-year rule."

                elif beneficiary_type == "Estate named the Beneficiary":
                    return f"Annual RMD's aren't required but you will need to empty the account by the end of the year {date_of_death_object.year + 5} under the 5 year rule since the Estate was named the Beneficiary."

                else:
                    return "----ERROR: INVALID BENEFICIARY TYPE----"

            elif not rmd_age:
                if beneficiary_type == "Spouse":
                    factor = Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor, grouping=True)
                    # If you are the owner's surviving spouse and sole designated beneficiary, you will also use Table I for your required minimum distributions.
                    # However, if the owner hadn't reached age 72 when he or she died, and you don't elect to be treated as the owner of the IRA,
                    # you don't have to take distributions until the year in which the owner would have reached age 72.
                    return f"Spouse can keep as an inherited account and Take distributions based on their own life expectancy which would be {required_minimum_distribution} using the factor of {factor},\n or Follow the 5-year rule or Rollover the account into their own IRA"
                elif beneficiary_type != "Spouse" and beneficiary_type != "Estate named the Beneficiary":
                    factor = (Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")) - factor_adjustment
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                                    grouping=True)
                    return f"Take distributions based on their own life expectancy which would be {required_minimum_distribution} using the factor of {factor}, or Follow the 5-year rule."
                elif beneficiary_type == "Estate named the Beneficiary":
                    return f"Annual RMD's aren't required but you will need to empty the account by the end of the year {date_of_death_object.year + 5} under the 5 year rule since the Estate was named the Beneficiary."
                else:
                    return "----ERROR: INVALID BENEFICIARY TYPE----"

        elif date_of_death_object.year >= 2020:
            if abs(age_of_deceased_at_death - (bene_age_year_after_death - 1)) <= 10:
                beneficiary_type = "Individual who is not more than 10 years younger than the IRA owner or plan participant"
            eligible_designated_beneficiary = ["Spouse",
                                               "Disabled or chronically ill individual",
                                               "Minor Child of deceased account holder",
                                               "Individual who is not more than 10 years younger than the IRA owner or plan participant"]
            rmd_age = 73 if self.today.year > 2022 and self.today.year < 2033 else 75
            if beneficiary_type in eligible_designated_beneficiary:
                factor = (Factor.all_tables(self, age=(bene_age_year_after_death), table="TableI"))  - factor_adjustment
                required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor, grouping=True)
                #  if deceased wasn't rmd age Spousal inherited IRA can postpone RMDs until the year the deceased would have turned 73.
                # RMD single life expectancy factor is used. reevaulted each year((which means life expectancy looked up
                # each year for age of bene vs noreevaulted minusing one each year from the factor) or the spouse can do 10year with no annual RMDs.
                # else if deacesed was rmd age You must begin taking an annual RMD over your life expectancy beginning
                # no later than 12/31 of the year following the original account holder's death
                # Your annual distributions are spread over your single life expectancy (determined by your age in the
                # calendar year following the year of death and reevaluated each year) or the deceased account holder's
                # remaining life expectancy, whichever is longer.
                # disbabled or chronically ill individual can use the single life expectancy factor from either younger of them or deceased
                # minor child (Only Eligibale bene if child of deceased can use the single life expectancy factor from either younger of them or deceased. No RMDs until they are 21 then 10 year kicks in
                return f"{required_minimum_distribution}, or\n{'or Follow the 10-year rule, if the account owner died before that owners required beginning date' if age_of_deceased_at_death < rmd_age else ''}"

            elif  beneficiary_type == "Estate named the Beneficiary":
                return f"Annual RMD's aren't required but you will need to empty the account by the end of the year {date_of_death_object.year + 5} under the 5 year rule since the Estate was named the Beneficiary."

            elif beneficiary_type == "Any other individual designated beneficiary of IRA account":
                factor = (Factor.all_tables(self, age=bene_age_year_after_death, table="TableI")) - (self.today.year - (date_of_death_object.year + 1))
                required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                                grouping=True)
                if age_of_deceased_at_death >= rmd_age:
                    return (f"Annual RMDs are required due to the deceased being RMD age and the RMD is {required_minimum_distribution} using the factor of {factor} and\n"
                            f"the account must be liquidated by the end of the year {date_of_death_object.year + 10} under the 10 year rule")
                else:
                    return f"Annual RMD's aren't required since the deceased was not RMD age but you will need to empty the account by the end of the year {date_of_death_object.year + 10} under the 10 year rule."

            else:
                return "----ERROR: INVALID BENEFICIARY TYPE----"
    def calculate_inherited_roth(self, account_value, beneficiary_date_of_birth, date_of_birth_original_account_owner, date_of_death_original_account_owner, beneficiary_type):
        prior_year_account_value = self.format_account_value(account_value)
        deceased_date_of_death_object = self.create_date_object(date_of_death_original_account_owner)
        beneficiary_date_of_birth_object = self.create_date_object(beneficiary_date_of_birth)
        date_of_birth_original_account_owner_object = self.create_date_object(date_of_birth_original_account_owner)
        date_of_death_object = self.create_date_object(date_of_death_original_account_owner)
        factor_adjustment = self.today.year - (date_of_death_object.year + 1)
        if deceased_date_of_death_object.year >= 2020:
            if beneficiary_type == "Spouse":
                return "There is no RMDs for the Spouse and they can treat the Roth IRA as their own."
            elif beneficiary_type == "Any other individual designated beneficiary of IRA account":
                return (f"There is no annual RMD but the account must be liquidation by the end of {deceased_date_of_death_object.year + 10}.")
            elif beneficiary_type == "Estate named the Beneficiary":
                return f"Due to the Estate being named the beneficiary there is no annual RMDs but the account will need to be liquidated by {deceased_date_of_death_object.year + 5} under the 5 year rule."
            elif beneficiary_type == "Minor Child of deceased account holder":
                return "Take distributions over the longer of their own life expectancy and the employee's remaining life expectancy, or follow 10 year rule (if the account owner died before thats owner's required beginning date."
            elif beneficiary_type == "Disabled or chronically ill individual":
                original_account_owner_older_than_bene = True if date_of_birth_original_account_owner_object < beneficiary_date_of_birth_object else False
                if original_account_owner_older_than_bene == False:
                    age = self.age_calculator(date_of_birth_original_account_owner)
                    factor = (Factor.all_tables(self, age=age, table="TableI")) - factor_adjustment
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor, grouping=True)
                    return (f"Take distributions over the longer of the beneficiaries life expectancy or the original account holder's remaining life expectancy which would be {required_minimum_distribution},\n "
                            f"using the factor of {factor} due to the original account owner being younger or you can follow 10 year rule which there would be no annual RMDs but the account\n"
                            f"must be liquidated by the end of {deceased_date_of_death_object.year + 10}")
                elif original_account_owner_older_than_bene == True:
                    age = self.age_calculator(beneficiary_date_of_birth)
                    factor = (Factor.all_tables(self, age=age, table="TableI")) - factor_adjustment
                    required_minimum_distribution = locale.currency(int(prior_year_account_value) / factor,
                                                                    grouping=True)
                    return f"Take distributions over the longer of their own life expectancy and the employee's remaining life expectancy which would be {required_minimum_distribution}, or follow 10 year rule (if the account owner died before thats owner's required beginning date."
                else:
                    return "ERROR: ERROR IN COMPARING AGE OF BENE VS AGE OF ORIGINAL ACCOUNT OWNER"
            else:
                return "-----ERROR SOMETHING WENT WRONG-----"

        if deceased_date_of_death_object.year < 2020:
            if beneficiary_type == "Spouse":
                return "There is no RMDs for the Spouse and they can treat the Roth IRA as their own."
            elif beneficiary_type == "Any other individual designated beneficiary of IRA account":
                factor = Factor.all_tables(self, (deceased_date_of_death_object.year - beneficiary_date_of_birth_object.year) + 1, table="TableI")
                adjusted_factor = factor - (self.today.year - (deceased_date_of_death_object.year + 1))
                required_minimum_distribution = locale.currency(int(account_value) / adjusted_factor, grouping=True)
                return  f"Based on the Beneficiary Life Expectancy your RMD is {required_minimum_distribution} using the factor of {adjusted_factor} or 5-year rule (No annual RMDs but account must be liquidated by the end of the 5th year following year of account holder death which is {deceased_date_of_death_object.year + 6} (2020 doesn't count)"
            elif beneficiary_type == "Minor Child of deceased account holder":
                return "Researching"
            elif beneficiary_type == "Disabled or chornically ill individual":
                return "Researching"
            elif beneficiary_type == "Estate named the Beneficiary":
                return f"Your under the 5 year rule, which there is no annual RMD but the account must be liquidated by the end of {deceased_date_of_death_object.year + 6}?"
            else:
                return "-----ERROR SOMETHING WENT WRONG-----"
        else:
            return "----ERROR SOMETHING WENT WRONG-----"
