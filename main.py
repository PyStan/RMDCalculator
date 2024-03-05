import flet as ft
from rmd import RMD
from datetime import datetime, date, timedelta
#
rmd = RMD()

def main(page: ft.Page):

    def clear_values(e):
        date_of_birth.value = ""
        account_value.value = ""
        spouse_date_of_birth.value = ""
        beneficiary_date_of_birth.value = ""
        date_of_death_original_account_owner.value = ""
        date_of_birth_original_account_owner.value = ""
        beneficiary_type.value = ""
        status.value = ""
        rmd_field.value = ""
        sole_beneficiary.value = ""

    def validation(e):
        if page.route == "/ira":
            if date_of_birth.value == "":
                date_of_birth.error_text = "The Account Owners Date of Birth is Required"
                page.update()
            else:
                date_of_birth.error_text = ""
                page.update()
            if len(date_of_birth.value) != 10:
                date_of_birth.error_text = "You have entered an invalid date or incorrectly formated date please use format MM/DD/YYYY"
                page.update()
            else:
                date_of_birth.error_text = ""
                page.update()
            if status.value == "Married":
                if spouse_date_of_birth.value == "":
                    spouse_date_of_birth.error_text = "The Account Owners Date of Birth is Required"
                    page.update()
                else:
                    spouse_date_of_birth.error_text = ""
                    page.update()
                if len(spouse_date_of_birth.value) != 10:
                    spouse_date_of_birth.error_text = "You have entered an invalid date or incorrectly formated date please use format MM/DD/YYYY"
                    page.update()
                else:
                    spouse_date_of_birth.error_text = ""
                    page.update()
            if status.value == "":
                # print("None")
                marital_status_container.border = ft.border.all(1, ft.colors.RED)
                marital_status_label.value = "Marital Status is required, please select an option below: "
                marital_status_label.color = ft.colors.RED
                single.fill_color = ft.colors.RED
                married.fill_color = ft.colors.RED
                divorced.fill_color = ft.colors.RED
                widowed.fill_color = ft.colors.RED
                single_text.color = ft.colors.RED
                married_text.color = ft.colors.RED
                divorced_text.color = ft.colors.RED
                widowed_text.color = ft.colors.RED
                page.update()
            else:
                # print(status.value)
                # print("status.value is showing something other than None")
                marital_status_container.border = ft.border.all(1, ft.colors.BLACK)
                marital_status_label.value = "Marital Status"
                marital_status_label.color = ft.colors.BLACK
                single.fill_color = ft.colors.BLACK
                married.fill_color = ft.colors.BLACK
                divorced.fill_color = ft.colors.BLACK
                widowed.fill_color = ft.colors.BLACK
                single_text.color = ft.colors.BLACK
                married_text.color = ft.colors.BLACK
                divorced_text.color = ft.colors.BLACK
                widowed_text.color = ft.colors.BLACK
                page.update()

            if account_value.value == "":
                account_value.error_text = "This field is required"
                page.update()
            else:
                account_value.error_text = ""
                page.update()
            if account_value.value.isnumeric():
                account_value.error_text = ""
                page.update()
            else:
                account_value.error_text = "You have entered a invalid input, please enter a numeric amount dumbass."
                page.update()
            calculate(e)
        else:
            if account_value.value == "":
                account_value.error_text = "This field is required"
                page.update()
            else:
                account_value.error_text = ""
                page.update()
            if account_value.value.isnumeric():
                account_value.error_text = ""
                page.update()
            else:
                account_value.error_text = "You have entered a invalid input, please enter a numeric amount dumbass."
                page.update()
            if beneficiary_date_of_birth.value == "":
                beneficiary_date_of_birth.error_text = "This field is required"
                page.update()
            if date_of_birth_original_account_owner.value == "":
                date_of_birth_original_account_owner.error_text = "This field is required"
                page.update()
            if date_of_death_original_account_owner.value == "":
                date_of_death_original_account_owner.error_text = "This field is required"
                page.update()
            if beneficiary_type.value == "":
                beneficiary_type.error_text = "This field is required"
                page.update()

            calculate(e)

    def calculate(e):
        try:
            if page.route == "/inherited_ira":
                rmd_result = rmd.calculate_inherited_ira_rmd(beneficiary_date_of_birth=beneficiary_date_of_birth.value,
                                                             prior_year_account_value=account_value.value,
                                                             date_of_death=date_of_death_original_account_owner.value,
                                                             date_of_birth_of_deceased=date_of_birth_original_account_owner.value,
                                                             beneficiary_type=beneficiary_type.value,)

                rmd_field.value = rmd_result
                page.update()

            elif page.route == "/inherited_roth":
                rmd_result = rmd.calculate_inherited_roth(account_value.value,
                                                          beneficiary_date_of_birth.value,
                                                          date_of_birth_original_account_owner.value,
                                                          date_of_death_original_account_owner.value,
                                                          beneficiary_type.value)
                rmd_field.value = rmd_result
                page.update()

            elif page.route == "/ira":
                rmd_result = rmd.calculate_traditional_ira_rmd(date_of_birth=date_of_birth.value,
                                                               prior_year_account_value=account_value.value,
                                                               spouse_date_of_birth=spouse_date_of_birth.value,
                                                               marital_status=status.value,
                                                               sole_beneficiary=sole_beneficiary.value)

                rmd_field.value = rmd_result
                page.update()


            else:
                print("ELSE?")

        except:
            print("Someone fucked up", Exception)



    def route_change(e):
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Select Account Type:"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                    ft.FilledButton(text="Traditional IRA or SEP IRA", on_click=lambda  _: page.go("/ira")),
                    ft.FilledButton(text="Roth IRA", on_click=lambda _: page.go("/roth")),
                    ft.FilledButton(text="Inherited Traditional IRA", on_click=lambda _: page.go("/inherited_ira")),
                    ft.FilledButton(text="Inherited Roth IRA", on_click=lambda _: page.go("/inherited_roth"))
                ], horizontal_alignment="CENTER"
            )
        )

        if page.route == "/ira":
            clear_values(e)
            page.views.append(
                ft.View(
                    "/ira",
                    [
                        ft.AppBar(title=ft.Text("Traditional IRA or SEP IRA"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                        account_value,
                        date_of_birth,
                        marital_status_label,
                        marital_status_container,
                        spouse_date_of_birth,
                        sole_beneficiary_label,
                        sole_beneficiary,
                        calculate_button,
                        rmd_field,
            ], horizontal_alignment="CENTER")
            )

        if page.route == "/roth":
            page.views.append(
                ft.View(
                    "/roth",
                    [
                        ft.AppBar(title=ft.Text("Roth IRA"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                        ft.Text("Roth IRA's do not have a required minimum distribution."),
                    ], horizontal_alignment="CENTER")
            )
        if page.route == "/inherited_ira":
            clear_values(e)
            page.views.append(
                ft.View(
                    "/inherited_ira",
                    [
                        ft.AppBar(title=ft.Text("Inherited Traditional IRA"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                        successor_radio_label,
                        ft.Radio(value="Yes", label="Yes"),
                        account_value,
                        beneficiary_date_of_birth,
                        date_of_birth_original_account_owner,
                        date_of_death_original_account_owner,
                        beneficiary_type_label,
                        beneficiary_type,
                        calculate_button,
                        rmd_field
                    ], horizontal_alignment="CENTER")
            )
        if page.route == "/inherited_roth":
            clear_values(e)
            page.views.append(
                ft.View(
                    "/inherited_roth",
                    [
                        ft.AppBar(title=ft.Text("Inherited Roth IRA"), bgcolor=ft.colors.SURFACE_VARIANT, center_title=True),
                        account_value,
                        beneficiary_date_of_birth,
                        date_of_birth_original_account_owner,
                        date_of_death_original_account_owner,
                        beneficiary_type_label,
                        beneficiary_type,
                        calculate_button,
                        rmd_field,
                    ], horizontal_alignment="CENTER")
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    single_text = ft.Text("Single")
    married_text = ft.Text("Married")
    divorced_text = ft.Text("Divorced")
    widowed_text = ft.Text("Widowed")
    page.title = "RMD Calculator"
    marital_status_label = ft.Text("Marital Status")
    sole_beneficiary = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("Yes"),
            ft.dropdown.Option("No")
        ]
    )
    sole_beneficiary_label = ft.Text("If married, Is the Spouse, the Sole Beneficiary of the IRA Account")
    single = ft.Radio(value="Single", label="")
    married = ft.Radio(value="Married", label="")
    divorced = ft.Radio(value="Divorced", label="")
    widowed = ft.Radio(value="Widowed", label="")

    status = ft.RadioGroup(content=ft.Row([
        single,
        single_text,
        married,
        married_text,
        divorced,
        divorced_text,
        widowed,
        widowed_text
    ], alignment="CENTER"))
    marital_status_container = ft.Container(
        content=status,
        padding=5,
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(1, ft.colors.BLACK),
        border_radius=ft.border_radius.all(10),
        height=55
    )

    date_of_birth = ft.TextField(label="Account Owner date of birth", hint_text="MM/DD/YYYY", border_radius=10,
                                 text_align="CENTER")
    account_value = ft.TextField(label="Account Value as of end of year from prior year", border_radius=10,
                                 text_align="CENTER")
    spouse_date_of_birth = ft.TextField(label="If Married, Spouses date of birth", hint_text="MM/DD/YYYY",
                                        border_radius=10, text_align="CENTER")
    beneficiary_date_of_birth = ft.TextField(label="Beneficiary date of birth", hint_text="MM/DD/YYYY",
                                             border_radius=10, text_align="CENTER")
    date_of_death_original_account_owner = ft.TextField(label="Date of death of Original Account Owner",
                                                        hint_text="MM/DD/YYYY", text_align="CENTER")
    date_of_birth_original_account_owner = ft.TextField(label="Date of birth of Original Account Owner",
                                                        hint_text="MM/DD/YYY", text_align="CENTER")
    beneficiary_type_label = ft.Text("Beneficiary Type")
    successor_radio_label = ft.Text("Is this a successor Inherited IRA?")
    successor_radio_btn = ft.RadioGroup(content=[
        ft.Radio(value="Yes", label="Yes"),
        ft.Radio(value="No", label="No")
    ]),
    beneficiary_type = ft.Dropdown(
        options=[
            ft.dropdown.Option("Spouse"),
            ft.dropdown.Option("Minor Child of deceased account holder"),
            ft.dropdown.Option("Disabled or chronically ill individual"),
            ft.dropdown.Option("Any other individual designated beneficiary of IRA account"),
            ft.dropdown.Option("Estate named the Beneficiary")

        ],

    )
    calculate_button = ft.FilledButton(text="Calculate", on_click=validation)
    rmd_field = ft.Text("", text_align="CENTER")
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



ft.app(target=main, view=ft.FLET_APP)