import time
import pandas as pd
import numpy as np
import json

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days= ['monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'all'  ]

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

    print ("Welcome to my bikeshare data explorer")
    print ("Dear User, Lets start with the City you want to explore data about")
    while True:
       city= input ("ENTER YOUR CITY OF CHOICE FOR ANALYSIS: Chicago, New York or Washington? \n> ").lower()
       if city in cities:
           break
    # get user input for month (all, january, february, ... , june)
    print ("Please enter which month you need data from, within the range of January to June")
    print ("Ready!!!, Roll")
    month= input ("Enter your choice of month for analysis :" ).lower()
    while month not in ['january','february', 'march', 'april','may','june', 'all'] :  
        month= input ('Dear User, Plese type a month within these options January, February, March, April, May, June or all :' )

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print ("Please enter which Day of the week you need data from, within the range of Monday to Friday")
    print("Ready!!!, Roll")
    while True:
        day= input ('Enter your day of Choice for analysis :').lower()
        if day in days:
            break

    print('Loading','.'*50)
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
# This section loads the data for the city to analyse into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # code to convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # code to extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day
    df['hour'] = df['Start Time'].dt.hour

     # code to filter by month if applicable
    if month != 'all':
        month =  months.index(month) + 1
        df = df[ df['month'] == month ]

#Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nAbout to display the statistics of the most frequent time of travel\n", '..'*50)
    start_time = time.time()


        # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is ", most_common_month)

 
    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week for this data is :", 
    most_common_day_of_week)

    # display the most common starting hour
    most_common_starting_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour for this data is :", 
    most_common_starting_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("Loading"'..'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip are displayed as follows...\n')
    start_time = time.time()

    # Code that displays the most commonly used start station 
    most_commonly_used_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station :", 
    most_commonly_used_start_station)

    # Code that displays the most commonly used end station
    most_commonly_used_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station :", most_commonly_used_end_station )

    # display most frequent combination of starting station and ending station in the trip
    most_common_starting_and_ending_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used starting station and ending station : {}, {}"\
            .format(most_common_starting_and_ending_station[0], most_common_starting_and_ending_station[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('..'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration_of_the_travel = sum(df['Trip Duration'])
    print('In the selected filters the total_duration_of_the_travel:', total_duration_of_the_travel/86400, " Days")
    
    # display mean travel time
    time_mean_for_travelling= df['Trip Duration'].mean()
    print("Mean travel time :", time_mean_for_travelling)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print("Loading",'..'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Lets count the user types in the data:\n")
    user_counts = df['User Type'].value_counts()
    print ("We've found the User Typers to be :",user_counts)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
        most_recent_year_of_birth= sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        earliest_year_of_birth= sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        most_common_year_of_birth= df['Birth Year'].mode()[0]
        print("The most earliest year of birth is ", earliest_year_of_birth , "\n")
        print("The most recent birth year is ", most_recent_year_of_birth, "\n")
        print("The most common year of all the birth years is ", most_common_year_of_birth, "\n")

        print("\nThis took %s seconds." % (time.time() - start_time))
    print("please wait",'..'*80)


    # Display first 5 rows of the table columns
def display_data(df):  
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):
        yes = input('\nHey there, I have the trip data for you, would you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break
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
