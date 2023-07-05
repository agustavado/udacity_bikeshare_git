# Imports section
import time
import pandas as pd
import numpy as np
import math as math

# pandas options configuration to control print of raw data table
pd.set_option('display.max_columns', 20)
pd.set_option('max_colwidth', 100)

# dictionary to list available cities and data sources
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(city='washington', month='all', day='all'):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_cities = ('chicago', 'new york city', 'washington')
    valid_months = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'all')
    valid_days = ('monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    while city not in valid_cities:
        print('You have to select one of the following cities: ' + str(valid_cities))
        city = input('Please enter a city name you want to consult: ').lower()
    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in valid_months:
        print('You have to select one of the following month values: ' + str(valid_months))
        month = input('Please enter a month you want to consult, or all for unfiltered data: ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    while day not in valid_days:
        print('You have to select one of the following day values: ' + str(valid_days))
        day = input('Please enter a day of week you want to consult, or all for unfiltered data: ').lower()

    print('-'*40)
    print('Your chosen data filters are : City ' + city + ', month: ' + month + ', day: ' + day)
    print('-'*40)
    return city, month, day

def load_data(city='washington', month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['start_time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['start_time'].dt.month_name().str.lower()
    df['day_of_week'] = df['start_time'].dt.weekday_name.str.lower()
    df['hour'] = df['start_time'].dt.hour

    if (month != 'all' and day != 'all'):
        print('\n--- Filtering ' + city + ' data by month: ' +  month + ' and by day of week: ' + day + ' ---\n')
        df = df.loc[df['month'] == month]
        df = df.loc[df['day_of_week'] == day]
    elif (month !='all' and day=='all'):
        print('\n--- Filtering ' + city + ' data by month: ' +  month + ' and considering all days of week ---\n')
        df = df.loc[df['month'] == month]
    elif (month =='all' and day!='all'):
        print('\n--- Filtering ' + city + ' data by day of week: ' +  day + ' and considering all months ---\n')
        df = df.loc[df['day_of_week'] == day]
    else:
        print('\nAll days of the week on all months are considered for calculations\n')

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (df) df - source data for calculating the time stats
    Returns:
        nothing
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df.month.nunique() >= 2:
        most_common_month = df['month'].mode()[0].title()
    else:
        most_common_month = 'Most common month does not make sense with your selection'

    # display the most common day of week
    if df.day_of_week.nunique() >= 2:
        most_common_day = df['day_of_week'].mode()[0].title()
    else:
        most_common_day = 'Most common day of the week does not make sense with your selection'

    # display the most common start hour
    if df.hour.nunique() >=2:
        most_common_start_hour = df['hour'].mode()[0]
    else:
        most_common_start_hour= 'Looks like there is no data to display'

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print("\nMost common month of travel is: " + most_common_month)
    print("\nMost common day of travel is: " + most_common_day)
    print("\nMost common hour for starting travel is: " + str(most_common_start_hour))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (df) df - source data for calculating the time stats
    Returns:
        nothing
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['start_end_combination'] = 'from ' + df['Start Station']+ ' to ' + df['End Station']
    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    most_common_start_end = df['start_end_combination'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print("\nMost common start station is: " + most_common_start_station)
    print("\nMost common end station is: " + most_common_end_station)
    print("\nMost common trip is: " + most_common_start_end)
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (df) df - source data for calculating the time stats
    Returns:
        nothing
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum()/60/60, 2)
    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()/60, 2)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('\nTotal travel time is: ' + str(total_travel_time) + ' hours')
    print("\nAverage travel time is: " + str(mean_travel_time) + ' minutes')
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (df) df - source data for calculating the time stats
    Returns:
        nothing
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts().rename_axis('User Type').reset_index(name='Count')
    print('-'*40)
    print(user_types)
    print('-'*40)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts().rename_axis('Gender').reset_index(name='Count')
    else:
        gender_counts = '\nNo gender data available for this city\n'
    print('-'*40)
    print(gender_counts)
    print('-'*40)

   # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        eldest_user_byear = math.trunc(df['Birth Year'].min())
        youngest_user_byear = math.trunc(df['Birth Year'].max())
        most_common_user_byear = math.trunc(df['Birth Year'].mode()[0])
        birth_year_info = '\nEarliest date of birth is ' + str(eldest_user_byear) + ', latest date of birth is ' + str(youngest_user_byear) + ', most common birthday year is ' + str(most_common_user_byear)+ '\n'
    else:
        birth_year_info = '\nNo birth year data available for this city\n'
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print(birth_year_info)
    print('-'*40)

def print_data(df):
    """Displays selected bikeshare data on user input request on 5 row increments.
    Args:
        (df) df - source data for calculating the time stats
    Returns:
        nothing
    """
    valid_inputs = ('yes', 'no')
    total_rows = df.shape[0]
    for i in range(0, total_rows, 5):
        print('\nDo you want to review the raw data first?\n')
        answer = input().lower()
        if answer not in valid_inputs:
            print('Please answer yes or no')
            continue
        elif answer == 'yes':
            start = i
            finish = i + 5
            print('Printing from ' + str(start) + ' to ' + str(finish) + ' data rows')
            print(df.iloc[start:finish])

        elif answer == 'no':
            break

def main():
    while True:
        city, month, day = get_filters()
        print('-'*40)
        print('--- Loading required data ---')
        print('-'*40)
        df = load_data(city, month, day)
        if not df.empty:
            print('-'*40)
            print_data(df)
            print('-'*40)
            time_stats(df)
            print('-'*40)
            station_stats(df)
            print('-'*40)
            trip_duration_stats(df)
            print('-'*40)
            user_stats(df)
            print('-'*40)
        else:
            print('-'*40)
            print('There is no data for your selection')
            print('-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
