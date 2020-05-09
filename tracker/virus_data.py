import threading
import json
import wget
import os
from os import path
from _datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dir_folder = r"C:\Users\thepu\PycharmProjects\coronavirustracker\tracker"
dir_folder = os.path.join(BASE_DIR, 'tracker')
url = r"https://infection2020.com/"
url_json = r"https://infection2020.netlify.com/z.json"
tests_url_json = r"https://covidtracking.com/api/v1/us/daily.json"


# TODO: save json file every 15 min
def download_data():
    if path.exists(dir_folder + "\\data.json"):
        os.remove(dir_folder + "\\data.json")
    if path.exists(dir_folder + "\\tests_data.json"):
        os.remove(dir_folder + "\\tests_data.json")

    try:
        wget.download(url_json, dir_folder + "\\data.json")

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print("downloaded at:", current_time)
    except:
        print("unable to download")

    try:
        wget.download(tests_url_json, dir_folder + "\\tests_data.json")
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print("downloaded tests data at:", current_time)
    except:
        print("unable to download tests data")

    threading.Timer(900.0, download_data).start()


def pull_data():
    # TODO: pull data from json file
    with open(dir_folder + "\\data.json") as f:
        data = json.load(f)
    with open(dir_folder + "\\tests_data.json") as d:
        tests_data = json.load(d)
    # print(data)

    # TODO: pull dates, cases, deaths
    cases = []
    deaths = []
    dates = []
    for i in range(len(data['ts'])):
        date_data = data['ts'][i]['date']
        dates.append(date_data)
        cases_data = data['ts'][i]['totalConfirmed']
        cases.append(cases_data)
        deaths_data = data['ts'][i]['totalDeaths']
        deaths.append(deaths_data)

    now = datetime.now()
    curr_date = now.strftime("%m/%d")
    curr_cases = data["totalConfirmed"]
    curr_deaths = data["totalDeaths"]

    # add today's data to list
    # deaths.append(curr_deaths)
    # cases.append(curr_cases)
    # dates.append(curr_date)

    # print(dates)
    # print(len(dates))
    # print(deaths)
    # print(len(deaths))
    # print(cases)
    # print(len(cases))

    # TODO: calc new cases, new deaths
    new_cases = [0]
    for i in range(1, len(dates)):
        new_cases_calc = cases[i] - cases[i-1]
        new_cases.append(new_cases_calc)
    # print(new_cases)
    # print(len(new_cases))

    new_deaths = [0]
    for i in range(1, len(dates)):
        new_deaths_calc = deaths[i] - deaths[i-1]
        new_deaths.append(new_deaths_calc)
    # print(new_deaths)
    # print(len(new_deaths))

    # TODO: calc case growth rate
    cases_growth_rate = [1]
    for i in range(1, len(dates)):
        growth_rate = new_cases[i] / cases[i-1] + 1
        growth_rate = str(round(growth_rate, 3))
        cases_growth_rate.append(growth_rate)
    # print(cases_growth_rate)

    # TODO: calc change in deaths per day
    change_new_deaths = [0, 0]
    for i in range(2, len(dates)):
        change_new_deaths.append(round(((new_deaths[i] - new_deaths[i-1])/new_deaths[i-1]), 4))

    # TODO: calc Case-Fatality Ratio
    case_fatality_ratio = []
    for i in range(len(dates)):
        case_fatality_ratio.append(round((deaths[i]/cases[i]*100), 4))

    # TODO: pull positive tests, negative tests, total tests
    tests_positive = []
    tests_negative = []
    tests_total = []
    tests_dates = []
    for i in range(len(tests_data)-36):
        # print(tests_data[i])
        month = str(int((tests_data[i]['date'] % 1000 - tests_data[i]['date'] % 100)/100))
        day = str(int(tests_data[i]['date'] % 100))
        full = month + "/" + day
        tests_dates.insert(0, full)
        tests_positive.insert(0, tests_data[i]['positive'])
        if i >= len(tests_data)-4:
            tests_negative.insert(0, 0)
        else:
            try:
                tests_negative.insert(0, tests_data[i]['negative'])
            except:
                print("error at " + str(i))
                pass
        tests_total.insert(0, tests_data[i]['totalTestResults'])

    x = tests_dates.index('3/1')
    tests_dates = tests_dates[x:]
    tests_positive = tests_positive[x:]
    tests_negative = tests_negative[x:]
    tests_total = tests_total[x:]

    print("ran pulled_data")
    return dates, cases, deaths, curr_date, curr_cases, curr_deaths, new_cases, new_deaths, cases_growth_rate,\
           change_new_deaths, case_fatality_ratio, tests_positive, tests_negative, tests_total


# dates pull_data()[0]
# cases pull_data()[1]
# deaths pull_data()[2]
# curr_date pull_data()[3]
# curr_cases pull_data()[4]
# curr_deaths pull_data()[5]
# new_cases pull_data()[6]
# new_deaths pull_data()[7]
# cases_growth_rate pull_data()[8]
# change_new_deaths pull_data()[9]
# case_fatality_ratio pull_data()[10]
# tests_positive pull_data()[11]
# tests_negative pull_data()[12]
# tests_total pull_data()[13]


def make_projections(num, num2, num3):
    # TODO: realistic projections
    pulled_data = pull_data()
    realistic_new_data_points = num
    realistic_new_dates = []
    realistic_cases_growth_rate = []

    growth_rate_multiplier = num2

    last_gr = float(pulled_data[8][-1])-1
    last_gr *= growth_rate_multiplier
    last_gr = round(last_gr, 4)
    realistic_cases_growth_rate.append(last_gr)
    for i in range(1, realistic_new_data_points):
        x_point = i
        y_point = float(realistic_cases_growth_rate[i-1]) * growth_rate_multiplier
        y_point = round(y_point, 4)
        realistic_cases_growth_rate.append(y_point)
    # print(realistic_cases_growth_rate)
    now = datetime.now()
    for i in range(len(realistic_cases_growth_rate)):
        realistic_cases_growth_rate[i] += 1
        future_date = now + timedelta(days=i)
        future_date_str = future_date.strftime("%m/%d")
        # print(future_date_str)
        realistic_new_dates.append(future_date_str)
    # print(realistic_cases_growth_rate)
    # print(realistic_new_dates)

    # TODO: project cases based on realistic projections
    last_case_number = int(pulled_data[1][-1] * realistic_cases_growth_rate[0])
    cases_projections = [last_case_number]
    for i in range(len(realistic_cases_growth_rate)-1):
        new_projection = cases_projections[i] * realistic_cases_growth_rate[i+1]
        cases_projections.append(int(new_projection))

    # TODO: calc new cases, new deaths
    new_projected_cases = [cases_projections[0] - pulled_data[1][-1]]
    for i in range(1, realistic_new_data_points):
        new_projected_cases_calc = cases_projections[i] - cases_projections[i-1]
        new_projected_cases.append(new_projected_cases_calc)
    # print(new_cases)
    # print(len(new_cases))

    # new_deaths = [0]
    # for i in range(1, len(dates)):
    #     new_deaths_calc = deaths[i] - deaths[i-1]
    #     new_deaths.append(new_deaths_calc)
    # print(new_deaths)
    # print(len(new_deaths))

    # TODO: extend data for graph
    for i in range(len(pulled_data[0])-num3):
        cases_projections.insert(0, " ")
    for i in range(len(pulled_data[0])-num3):
        realistic_cases_growth_rate.insert(0, " ")
    for i in range(len(pulled_data[0])-num3):
        new_projected_cases.insert(0, " ")
    print("ran make_projections")
    return realistic_new_dates, cases_projections, realistic_cases_growth_rate, new_projected_cases

# realistic_new_dates               make_projections(num)[0]
# cases_projections                 make_projections(num)[1]
# realistic_cases_growth_rate       make_projections(num)[2]
# new_projected_cases               make_projections(num)[3]

