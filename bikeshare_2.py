import time
import pandas as pd
import numpy as np

time_filter = '' #needed to be globle to avoid calculating the most common day and month when filtered to specific day or month
MonthesName = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DayesName = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York and washington? \n").lower()
    while city not in CITY_DATA:
        print("Wrong Input")
        city = input("Would you like to see data for Chicago, New York and washington? \n").lower()

    #get user filter
    time_filter = input("Would you like to filter the data by month, day, both, or not at all? Please, Type \'none\' for no time filter \n").lower()
    while time_filter not in ['month', 'day','both','none']:
        print("Wrong Input")
        time_filter = input("Would you like to filter the data by month, day, both, or not at all? Please, Type \'none\' for no time filter \n").lower()

    # get user input for month (all, january, february, ... , june)
    if time_filter in ['month', 'both']:
        month = input("Which moth? all, january, february, ... , june \n").lower()
        while month not in  MonthesName:
            print("Wrong Input")
            month = input("Which moth? all, january, february, ... , june \n").lower()
        if time_filter == 'month':
            day = 'none'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if time_filter in ['day', 'both']:
        day = input("Which day? all, monday, tuesday, ... sunday \n").lower()
        while day not in DayesName :
            print("Wrong Input")
            day = input("Which day? all, monday, tuesday, ... sunday \n").lower()
        if time_filter == 'day':
            month = 'none'

    if time_filter == 'none':
        day = 'none'
        month = 'none'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv( CITY_DATA[city] )
    #prefilter
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month not in ['all', 'none']:
        month = MonthesName.index(month)
        df = df[df['month'] == month] # filter by month to create the new dataframe

    # filter by day of week
    if day not in ['all', 'none']:
        df = df[df['day_of_week'] == day.title()]   # filter by day of week to create the new dataframe

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common = df['month'].mode()[0]
    most_common = str(MonthesName[most_common])
    print("The most common month is ",most_common.title() )

    # display the most common day of week
    print("The most common day of week is ", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most common start hour is ", df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is ", df['Start Station'].value_counts()[[0]])

    # display most commonly used end station
    print("The most common end station is ", df['End Station'].value_counts()[[0]])

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip ", (df['Start Station'] + df['End Station']).value_counts()[[0]])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is {} mins".format(df["Trip Duration"].sum() / 60) )

    # display mean travel time
    print("The mean travel time is {} mins".format(df["Trip Duration"].mean() / 60) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The counts of user types")
    print( df['User Type'].value_counts() )

    if 'Gender' in df:
        # Display counts of gender
        print("The counts of gender")
        print( df['Gender'].value_counts() )

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("The earliest year of birth is ", df['Birth Year'].min())
        print("The most recent year of birth is ", df['Birth Year'].max())
        print("The most common year of birth is ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    #check the view_data
    while view_data not in ['yes', 'no']:
        print('Wrong Input')
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()


    start_loc = 0
    while True:
        #check the view_data
        while view_data not in ['yes', 'no']:
            print('Wrong Input')
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

        if view_data == 'no':
            break
        print(df.iloc[start_loc : start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
