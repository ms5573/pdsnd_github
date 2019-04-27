import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ["all",
          "january",
          "febuary",
          "march",
          "april",
          "may",
          "june",
          "july",
          "august",
          "september",
          "october",
          "november",
          "december"]

days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    
    while True:
        city = input('Please enter the name of the city you would like to explore: ').lower()
        

        if city not in CITY_DATA and city != 'quit':
            print("Sorry, the city you entered is not valid. Try again or type 'QUIT'!")
            continue

        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please enter the name of the month you would like to explore: ').lower()
        
        if month not in months and month != 'quit':
            print("Sorry, the month you entered is not valid. Try again or type 'QUIT'!")
            continue

        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the name of the day you would like to explore: ').lower()
        
        if day not in days and day != 'quit':
            print("Sorry, the day you entered is not valid. Try again or type 'QUIT'!")
            continue

        else:
            break


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


    # filter by month if applicable
    if month != 'all':
        month = months.index(month)
        # generate list of all months in the data set
        data_months = df['month'].unique()
        
        # check if the specified month is part of the data set. If not let the user enter another month
        while month not in data_months:
            print('There is only data for the following months: ')
            for x in data_months:
                print(months[x].title())
            month = input('\nPlease select one of the months listed: ').lower()
            month = months.index(month)

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
    most_common_month = df['month'].mode()[0]
    print('\nThe most common month is: {}'.format(months[most_common_month]).title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\nThe most common day of the week is: {}'.format(most_common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most common start hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station is: {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station is: {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = '\nStart Station: ' + df['Start Station'].astype(str) + '\nEnd Station: ' + df['End Station']
    popular_start_end_station = df['Start End Station'].mode()[0]
    print('\nThe most frequent combination of start station and end station is: {}'.format(popular_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = int(df['Trip Duration'].sum()/60)
    print('The total travel time in min is: {}'.format(total_travel))
    #export_csv = df.to_csv (r'export_dataframe.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path

    # display mean travel time
    mean_travel = int(df['Trip Duration'].mean()/60)
    print('The mean travel time in min is: {}'.format(mean_travel))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        user_types_count = df['User Type'].value_counts()
        print('The count of user types is:')
        print(user_types_count)

    else:
        print('Count of user types: NA')
   

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of genders is:')
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        birth_min = int(df['Birth Year'].min())
        print('\nThe earliest birth year is: {}'.format(birth_min))

        birth_max = int(df['Birth Year'].max())
        print('The most recent birth year is: {}'.format(birth_max))

        birth_mode = int(df['Birth Year'].mode()[0])
        print('The most common year of birth is: {}'.format(birth_mode))

    else:
        print('Gender count: NA')

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
