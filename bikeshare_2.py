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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print("Sorry, that is not one of the allowed entries.  Please try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to see data for January, February, March, April, May, June or all?').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Sorry, that is not one of the allowed entries.  Please try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''

    while day not in days:
        day = input('Would you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all?').lower()

    print('You have selected: ', day)

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month: ', popular_month)


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Day of the Week: ', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]

    print('The most popular starting station is: ', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]

    print('The most popular ending station is: ', popular_end)

    # display most frequent combination of start station and end station trip
    df['stations_combined'] = df['Start Station'] + ' and ' + df['End Station']
    popular_combination = df['stations_combined'].mode()[0]

    print('The most popular combination of stations is: ', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['travel_time'] = df['End Time'] - df['Start Time']
    total_time = df['travel_time'].sum()
    print('The total travel time was: ', total_time)

    # display mean travel time
    mean_time = df['travel_time'].mean()
    print('The mean travel time was: ', mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('The numbers of each user type is: ', user_type_count)

    # Display counts of gender
    #Not all the datasets include gender information so added a try statement
    while True:
        try:
            gender_count = df['Gender'].value_counts()
            print('The number of each gender using bikeshare is: ', gender_count)
            break
        except KeyError:
            print('Sorry, gender information is not included in this dataset.')
            break

    # Display earliest, most recent, and most common year of birth
    #Not all the data sets include birth year information so added a try
    while True:
        try:
            earliest_birth_year = df['Birth Year'].min()
            print('The earliest birth year of users is ', earliest_birth_year)
            break
        except KeyError:
            print('Sorry, birth year information is not included in this dataset.')
            break

    while True:
        try:
            most_recent_birth_year = df['Birth Year'].max()
            print('The most recent birth year of users is ', most_recent_birth_year)
            break
        except KeyError:
            print('Sorry, birth year information is not included in this dataset.')
            break

    while True:
        try:
            most_common_birth_year = df['Birth Year'].mode()[0]
            print('The most common birth year of users is ', most_common_birth_year)
            break
        except KeyError:
            print('Sorry, birth year information is not included in this dataset.')
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        file_data = 0

        raw_data = input('\nWould you like to view 5 lines of the raw data?  Enter yes or no.\n')

        while raw_data.lower() == 'yes':
            print(df.iloc[file_data:file_data+5])
            raw_data = input('\nWould you like to view 5 lines of the raw data?  Enter yes or no.\n')
            file_data += 5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
