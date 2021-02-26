# Just imports the neccesary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fetches data; souce: https://evictionlab.org/eviction-tracking/get-the-data/
# IMPORTANT: Baseline data for this is 2015-2016
# IMPORTANT VIEWER NOTE: The following lines of code only works on my laptop because it's where the pathway is stored.
# Change the following line to where the you download the file 
evictiondata = pd.read_csv(r"C:\Users\alexz\OneDrive\Documents\College\Freshman year\Sidegigs\Houston_evictions.csv")

# Gives quick preview
evictiondata.head(3)
evictiondata.shape


def total(evictiondata):
    """
    Computes the total evictions filed
    :param evictiondata: the csv file of evictions filed
    :return: An int repersenting the total
    """
    total = 0
    for index, row in evictiondata.iterrows():
        total += row['filings_2020']


def weekly(evictiondata):
    """
    Eviction filings broken down into a week-by-week basis
    :param evictiondata: the csv file of evictions filed
    :return: a dictionary with the keys being the week, and the values being the evictions filed within that week
    """
    evictions_per_week = {}
    for index, row in evictiondata.iterrows():
        if row['week_date'] not in evictions_per_week.keys():
            evictions_per_week[row['week_date']] = row['filings_2020']
        else:
            evictions_per_week[row['week_date']] += row['filings_2020']
    return evictions_per_week


def graphify(evictions_per_week):
    """
    Visualizes the week by week eviction data into a graph
    :param evictions_per_week: dictionary with the keys being the week, and the values being the evictions filed within that week
    :return: displays a graph: x values is time by week, y value is evictions filed
    """
    weeks = []
    for week in evictions_per_week.keys():
        if '2020' in week:
            weeks.append(week)
    evictions_filed = []
    for week in weeks:
        evictions_filed.append(evictions_per_week[week])
    plt.figure(figsize=(50, 10))
    plt.plot(weeks, evictions_filed)
    plt.xlabel('Date')
    plt.ylabel('Evictions filed')
    plt.title('Evictions filed by the week')
    plt.show()
    return weeks, evictions_filed


def graph_baseline(evictiondata, weeks):
    """
    Graphs the baseline eviction data of 2015-2016 in the same format
    :param evictiondata: csv file of evictions filed
    :return: displays a graph: x values being time by week, y values being evictioned filed in 2015-2016
    """
    base_evictions_per_week = {}
    for index, row in evictiondata.iterrows():
        if row['week_date'] not in base_evictions_per_week.keys():
            base_evictions_per_week[row['week_date']] = row['filings_avg']
        elif row['GEOID'] != 'sealed':
            base_evictions_per_week[row['week_date']] += row['filings_avg']
    base_evictions_filed = []
    for week in weeks:
        base_evictions_filed.append(base_evictions_per_week[week])

    plt.figure(figsize=(50, 10))
    plt.plot(weeks, base_evictions_filed, color='orange')
    plt.title('Base Evictions filed by the week')
    plt.xlabel('Date')
    plt.ylabel('Evictions filed')
    plt.show()
    return base_evictions_filed


def cross_analyze(evictions_filed, base_evictions_filed, weeks):
    """
    Cross analyzes the baseline with 2020's eviction data. NOTE* Requires you to run the above functions
    :param evictiondata: csv file of eviction data
    :return: a compiled graph that also notes when the Texas supreme court put a temporary stay on evictions
    """
    plt.figure(figsize=(50, 10))
    plt.plot(weeks, evictions_filed, label = '2020')
    plt.plot(weeks, base_evictions_filed, label = '2015-2016')
    plt.xlabel('Date', fontsize = 25)
    plt.ylabel('Evictions filed', fontsize = 25)
    plt.title('Evictions filed by the week', fontsize = 40)
    plt.legend()
    plt.annotate('Texas Supreme Court puts a temporary \n stay on eviction proceedings.', xy = ('3/8/2020', 1551), fontsize = 15)
    plt.show()


# Implementation
print(total(evictiondata))
evictions_per_week = weekly(evictiondata)
weeks = graphify(evictions_per_week)[0]
evictions_filed = graphify(evictions_per_week)[1]
base_evictions_filed = graph_baseline(evictiondata, weeks)
cross_analyze(evictions_filed, base_evictions_filed, weeks)

