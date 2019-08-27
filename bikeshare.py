import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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

    # set initial values
    city = ""
    month = ""
    day = ""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ('chicago', 'new york city', 'washington'):
        city = input('\nWould you like to see data for chicago, new york city or washington?\n').lower()

    # get user input for month (all, january, february, ... , june)
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        month = input('\nWhich month? january, february, march, april, may, june or all ?\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
        day = input('\nWhich day? monday, tuesday, wednesday, thursday, friday, saturday, sunday or all ?\n').lower()

    # print filters
    print('-'*40)
    print('\nYour city filter is: ', city.title())
    print('\nYour month filter is: ', month.title())
    print('\nYour day of week filter is: ', day.title())
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
 
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['combined'] = 'Start station: ' + df['Start Station'] + '; End station: ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('\nThe most common month is:', popular_month)

    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('\nThe most common day of week is: ', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination = df['combined'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip is: \n  ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nThe total travel time is: ', total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\nThe mean travel time is: ', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nThe user type count are:\n', user_type)

    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        gender_count = df['Gender'].value_counts()
        print('\nThe gender count are:\n', gender_count)

    # Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        eldest = df['Birth Year'].min()
        print('\nThe earliest year of birth is: ', eldest)
    
        youngest = df['Birth Year'].max()
        print('\nThe most recent year of birth is: ', youngest)

        common_year = df['Birth Year'].mode()[0]
        print('\nThe most common year of birth is: ', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    show_raw = input('\nDo you want to see raw data? Enter yes or no\n').lower()
    start_row = 0
    end_row = 5

    if df.size < end_row:
        end_row = df.size
        
    while show_raw == 'yes':
        print(df.iloc[start_row:end_row])
        show_raw = input('\nDo you want to see 5 more lines of raw data? Enter yes or no\n').lower()
        start_row = end_row
        end_row += 5
        if df.size < end_row:
            end_row = df.size

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
