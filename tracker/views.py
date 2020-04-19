from django.shortcuts import render
from . import virus_data

virus_data.download_data()


def home(request):
    data = virus_data.pull_data()
    cases_projections = []
    realistic_new_dates = 0
    realistic_cases_growth_rate = []
    new_projected_cases = []
    user_num = 30
    user_growth_num = .91
    checky = ""
    total_dates = len(data[0])
    dates_to_show = len(data[0])
    newdata_dates = data[0][-dates_to_show:]
    newdata_cases = data[1][-dates_to_show:]
    newdata_new_cases = data[6][-dates_to_show:]
    newdata_cases_growth_rate = data[8][-dates_to_show:]
    newdata_deaths = data[2][-dates_to_show:]
    newdata_new_deaths = data[7][-dates_to_show:]
    newdata_deaths_change = data[9][-dates_to_show:]
    curr_new_cases = "{:,}".format(data[4] - data[1][-1])
    curr_new_deaths = "{:,}".format(data[5] - data[2][-1])
    tests_positive = data[11][-dates_to_show:]
    tests_negative = data[12][-dates_to_show:]
    tests_total = data[13][-dates_to_show:]
    curr_case_fatality_ratio = round(data[10][-1], 2)
    curr_tests_total = "{:,}".format(data[13][-1])

    if request.method == "POST":
        dates_to_show = int(request.POST.get('daysDisplayNumber'))
        newdata_dates = data[0][-dates_to_show:]
        newdata_cases = data[1][-dates_to_show:]
        newdata_new_cases = data[6][-dates_to_show:]
        newdata_cases_growth_rate = data[8][-dates_to_show:]
        newdata_deaths = data[2][-dates_to_show:]
        newdata_new_deaths = data[7][-dates_to_show:]
        newdata_deaths_change = data[9][-dates_to_show:]
        tests_positive = data[11][-dates_to_show:]
        tests_negative = data[12][-dates_to_show:]
        tests_total = data[13][-dates_to_show:]

        checky = request.POST.get('onOffCheckbox')
        if checky:
            user_num = int(request.POST.get('Number'))
            user_growth_num = float(request.POST.get('growthNumber'))
            subtract_dates = total_dates - dates_to_show
            v_data = virus_data.make_projections(user_num, user_growth_num, subtract_dates)
            cases_projections = v_data[1]
            realistic_new_dates = v_data[0]
            realistic_cases_growth_rate = v_data[2]
            new_projected_cases = v_data[3]
        else:
            realistic_new_dates = 0

    context = {
        'cases': data[1],
        'deaths': newdata_deaths,
        'dates': data[0],
        'new_cases': data[6],
        'new_deaths': newdata_new_deaths,
        'cases_growth_rate': data[8],
        'change_new_deaths': newdata_deaths_change,
        'curr_date': data[3],
        'curr_cases': "{:,}".format(data[4]),
        'curr_deaths': "{:,}".format(data[5]),
        'curr_new_cases': curr_new_cases,
        'curr_new_deaths': curr_new_deaths,
        'curr_cases_growth_rate': data[8][-1],
        'realistic_new_dates': realistic_new_dates,
        'realistic_cases_growth_rate': realistic_cases_growth_rate,
        'cases_projections': cases_projections,
        'new_projected_cases': new_projected_cases,
        'user_num': user_num,
        'user_growth_num': user_growth_num,
        'checky': checky,
        'newdata_dates': newdata_dates,
        'newdata_cases': newdata_cases,
        'newdata_new_cases': newdata_new_cases,
        'newdata_cases_growth_rate': newdata_cases_growth_rate,
        'total_dates': total_dates,
        'dates_to_show': dates_to_show,
        'case_fatality_ratio': data[10],
        'tests_positive': tests_positive,
        'tests_negative': tests_negative,
        'tests_total': tests_total,
        'curr_case_fatality_ratio': curr_case_fatality_ratio,
        'curr_tests_total': curr_tests_total,
               }
    return render(request, 'tracker/base.html', context)
