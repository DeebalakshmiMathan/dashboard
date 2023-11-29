import pandas as pd
import pathlib
from datetime import date, datetime, timedelta


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


summary = pd.read_csv(DATA_PATH.joinpath("summary.csv"))
df = pd.read_csv(DATA_PATH.joinpath("performer.csv"))
earning = pd.read_csv(DATA_PATH.joinpath("Earning.csv"))
performer_analysis =(DATA_PATH.joinpath("performer.csv"))
pie = pd.read_csv(DATA_PATH.joinpath("pie.csv"))
emp_details = pd.read_csv(DATA_PATH.joinpath("emp_details_report.csv"))
time_distribution = pd.read_csv(DATA_PATH.joinpath("timing_distribution_report.csv"))
micro_activity_distribution = pd.read_csv(DATA_PATH.joinpath("microactivitydistribution.csv"))
activity_efficiency = pd.read_csv(DATA_PATH.joinpath("activity_efficiency.csv"))
insight_graph_data = pd.read_csv(DATA_PATH.joinpath("insight.csv"))



# Over View Page
def generate_table_data(date, max_rows):
    given_date = datetime.strptime(date, "%Y-%m-%d")
    l = []
    for i in range(len(df)):
        temp_date = str(df.iloc[i][df.columns[0]])
        temp_date = datetime.strptime(temp_date, "%d-%m-%y")
        if given_date == temp_date:
            l.append(df.iloc[i][1:])
            max_rows -= 1
            if max_rows == 0:
                break
    return l


def generate_table_week_data(date, max_rows):
    date = datetime.strptime(date, "%Y-%m-%d")
    time_reduce = timedelta(1)
    data = []
    for _ in range(7):
        data = generate_table_data(
            date.strftime("%Y-%m-%d"), max_rows)+data
        date -= time_reduce
    return data

def summaryCompilance( date, week):
    given_date = datetime.strptime(date, "%Y-%m-%d")
    summary_count = 0
    summary_total = 0
    if week:
        time_reduce = timedelta(1)
        for _ in range(7):
            for i in range(len(summary)):
                temp_date = summary.iloc[i][summary.columns[0]]
                temp_date = datetime.strptime(temp_date, "%d-%m-%y")
                if given_date == temp_date:
                    summary_count += 1
                    summary_total += float(summary.iloc[i]
                                           [summary.columns[1]].replace("%", ""))
            given_date -= time_reduce
    else:
        for i in range(len(summary)):
            temp_date = summary.iloc[i][summary.columns[0]]
            temp_date = datetime.strptime(temp_date, "%d-%m-%y")
            if given_date == temp_date:
                summary_count += 1
                summary_total += float(summary.iloc[i]
                                       [summary.columns[1]].replace("%", ""))
    ans = 0
    if summary_count:
        ans = summary_total/summary_count
    return ans


def summarySpeed(summary, date, week):
    given_date = datetime.strptime(date, "%Y-%m-%d")
    speed_total = 0
    speed_count = 0
    if week:
        time_reduce = timedelta(1)
        for _ in range(7):
            for i in range(len(summary)):
                temp_date = summary.iloc[i][summary.columns[0]]
                temp_date = datetime.strptime(temp_date, "%d-%m-%y")
                if given_date == temp_date:
                    speed_count += 1
                    speed_total += float(summary.iloc[i][summary.columns[2]])
            given_date -= time_reduce
    else:
        for i in range(len(summary)):
            temp_date = summary.iloc[i][summary.columns[0]]
            temp_date = datetime.strptime(temp_date, "%d-%m-%y")
            if given_date == temp_date:
                speed_count += 1
                speed_total += float(summary.iloc[i][summary.columns[2]])
    ans = 0
    if speed_count:
        ans = speed_total/speed_count
    return ans


def display_Earning(date, week):
    earning_total = 0
    earning_count = 0
    given_date = datetime.strptime(date, "%Y-%m-%d")
    date_reduce_count = 1
    if week:
        date_reduce_count = 7
    time_reduce = timedelta(1)
    for _ in range(date_reduce_count):
        flag = 0
        for i in range(len(earning)):
            temp_date = earning.iloc[i][earning.columns[1]]
            temp_date = datetime.strptime(temp_date, "%d-%m-%y")
            if given_date == temp_date:
                earning_total += (earning.iloc[i][earning.columns[3]] -
                                  earning.iloc[i][earning.columns[2]])*650
                flag = 1
        if flag:
            earning_count += 1
        given_date -= time_reduce
    ans = 0
    if earning_count:
        ans = earning_total/earning_count
    return "₹ {:.02f}".format(ans)


def displayActivityDistribution_Data(date, week):
    activity = []
    cost = []
    d = {}
    given_date = datetime.strptime(date, "%Y-%m-%d")
    date_reduce_count = 1
    if week:
        date_reduce_count = 7
    time_reduce = timedelta(1)
    for _ in range(date_reduce_count):
        for i in range(len(pie)):
            temp_date = pie.iloc[i][pie.columns[0]]
            temp_date = datetime.strptime(temp_date, "%d-%m-%y")
            if given_date == temp_date:
                d[str(pie.iloc[i][pie.columns[1]])] = d.get(
                    str(pie.iloc[i][pie.columns[1]]), 0)+int(pie.iloc[i][pie.columns[2]])
                # * d[i]=d.get(i,0)+1
        given_date -= time_reduce
    for i in d:
        activity.append(i)
        cost.append(d[i])
    return [activity, cost]


# Report Page
def get_emp_data(emp_name, emp_details):
    # .iloc[i][1:]
    for i in range(len(emp_details)):
        temp_name = str(emp_details.iloc[i][emp_details.columns[0]])
        if temp_name == emp_name:
            d = {}
            for col in emp_details.columns[1:]:
                d[str(col)] = str(emp_details.iloc[i][col])
            return d


def get_emp_activity(emp_name):
    activities = set()
    for i in range(len(time_distribution)):
        temp_name = str(
            time_distribution.iloc[i][time_distribution.columns[0]])
        if temp_name == emp_name:
            activities.add(
                str(time_distribution.iloc[i][time_distribution.columns[1]]))
    return sorted(activities)


def get_emp_activity2(emp_name):
    activities = set()
    for i in range(len(time_distribution)):
        temp_name = str(
            time_distribution.iloc[i][time_distribution.columns[0]])
        if temp_name == emp_name:
            activities.add(
                str(time_distribution.iloc[i][time_distribution.columns[2]]))
    return sorted(activities)


def get_emp_activity_graph(emp_name, ac_type, w_time):
    for i in range(len(time_distribution)):
        temp_name = str(
            time_distribution.iloc[i][time_distribution.columns[0]])
        if temp_name == emp_name and ac_type == str(time_distribution.iloc[i][time_distribution.columns[1]]) and w_time == str(time_distribution.iloc[i][time_distribution.columns[2]]):
            return [float(time_distribution.iloc[i][time_distribution.columns[3]]), float(time_distribution.iloc[i][time_distribution.columns[4]])]
    return [0, 0]


def check_complaints(data):
    if int(data) < 50:
        return "Not Complaint(%d%%)" % (data)
    return "Complaint(%d%%)" % (data)


def get_micro_activities(emp_name, ac_type, w_time):
    result = []
    for i in range(len(micro_activity_distribution)):
        temp_name = str(
            micro_activity_distribution.iloc[i][micro_activity_distribution.columns[0]])
        temp_ac_type = str(
            micro_activity_distribution.iloc[i][micro_activity_distribution.columns[1]])
        temp_w_time = str(
            micro_activity_distribution.iloc[i][micro_activity_distribution.columns[2]])
        if emp_name == temp_name and ac_type == temp_ac_type and w_time == temp_w_time:
            row_data = [str(
                micro_activity_distribution.iloc[i][micro_activity_distribution.columns[3]]), check_complaints(micro_activity_distribution.iloc[i][micro_activity_distribution.columns[4]]), str(micro_activity_distribution.iloc[i][micro_activity_distribution.columns[5]])+" Seconds"]
            result.append(row_data)
    return result


def report_potential_earning(emp_name):
    for i in range(len(earning)):
        temp_name = str(earning.iloc[i][earning.columns[0]])
        if temp_name == emp_name:
            return "%.02f" % ((float(earning.iloc[i][earning.columns[3]])-float(earning.iloc[i][earning.columns[2]]))*650)


def get_activity_efficiency(emp_name):
    for i in range(len(activity_efficiency)):
        temp_name = str(
            activity_efficiency.iloc[i][activity_efficiency.columns[0]])
        if temp_name == emp_name:
            return [str(activity_efficiency.iloc[i][activity_efficiency.columns[1]]), int(activity_efficiency.iloc[i][activity_efficiency.columns[2]])]



# Over All Page

def get_overall_activities(activity):
    result = {"PerformanceDuration": [], "AverageDuration": [], "name": []}
    for i in range(len(time_distribution)):
        if str(time_distribution.iloc[i][time_distribution.columns[1]]) == activity and str(time_distribution.iloc[i][time_distribution.columns[0]]) not in result["name"]:
            result["PerformanceDuration"].append(
                float(time_distribution.iloc[i][-2]))
            result["AverageDuration"].append(
                float(time_distribution.iloc[i][-1]))
            result["name"].append(
                str(time_distribution.iloc[i][time_distribution.columns[0]]))
    return result


def get_overall_properties(prop):
    names = {}
    for k in range(len(emp_details)):
        names[emp_details.iloc[k]["Name"]] = [
            float(emp_details.iloc[k][prop]), 0, 0]
    temp = []
    for i in range(len(time_distribution)):
        if time_distribution.iloc[i]["Name"] in temp:
            continue
        temp.append(time_distribution.iloc[i]["Name"])
        names[time_distribution.iloc[i]["Name"]
              ][1] = time_distribution.iloc[i][time_distribution.columns[-2]]
        names[time_distribution.iloc[i]["Name"]
              ][2] = time_distribution.iloc[i][time_distribution.columns[-1]]
    res = list(zip(*names.values()))
    result = {"PerformanceDuration": res[1],
              "AverageDuration": res[2], "prop": res[0]}
    return result


def get_leaderboard():
    result = {}
    for i in range(len(emp_details)):
        for j in range(1, len(emp_details.columns)-3):
            key = str(emp_details.columns[j])
            value = float(emp_details.iloc[i][key])
            result[key] = result.get(key, [])+[value]
            if len(result[key]) > 1:
                temp = sorted(result[key])
                result[key] = [temp[-1], temp[0]]
    return result


# Insight
def get_insight_data(emp_name):
    day = {'Pre-lunch': [0, 0],
           'Post-Lunch': [0, 0]}
    for i in range(len(insight_graph_data)):
        temp_name = str(insight_graph_data.iloc[i][0])
        if emp_name == temp_name or emp_name == 'Overall':
            temp = str(insight_graph_data.iloc[i][1])
            day[temp][0] += float(insight_graph_data.iloc[i][2])
            day[temp][1] += float(insight_graph_data.iloc[i][3])
    return day

def convert_mins(mint):
    hr = mint//60
    mint -= hr*60   
    sec = (mint % 1)*60
    if int(hr) == 0 and int(mint) == 0:
        return "%d min. %d sec." % (mint, sec)
    return "%d hr. %d min. %d sec." % (hr, mint, sec)


def mins_to_perst(mins):
    return "%.02f" % (mins/4.8)


def potential_loss(data):  
           
    return "%.02f"%((sum(data["Pre-lunch"])+sum(data["Post-Lunch"]))*10.83333)


def overall_unprod_half(data):
    data = data.items()
    key, value = "", 0
    for i in data:
        if sum(i[1]) > value:
            value = sum(i[1])
            key = i[0]
    return key