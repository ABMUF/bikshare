import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

re    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city
    city=''
    while city not in ('chicago','new york', 'washington'):
        city = str(input('Would you like to see data for Chicago, New York, or Washington?')).lower()
        
        if city not in ('chicago','new york', 'washington'):
            print('\nplease choose one of the three cities by typing the correct name of the city')
            
    filter =''        
    while filter not in ('month', 'day', 'both','none'):
        filter = str(input('Would you like to filter data by : month , day , both , or not at all? Type\'none\' for no time filter')).lower()
                     
        if filter not in ('month', 'day', 'both','none'):
            print('please type one of the four time filters that written above')
                  
                  
    # get user input for month (all, january, february, ... , june)
    global month
    month = ''
    while filter in ('month','both') and month not in ('january','february','march', 'april', 'may', 'june'):
        month = str(input('which month? January,February,March, April, May, or June ')).lower()
                  
        if month not in ('january','february','march', 'april', 'may', 'june'):
            print('please make sure you type the right choice')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    global day 
    day =''
    day_numbers = range(1,8)
    
    while filter in ('day','both') and day not in day_numbers:
        try:
            day = int(input('\n which day? sunday, monday..etc (please type the number of the day e.g:Mon =1, Tues =2 , Wed = 3 etc)\n' ))
        except ValueError:
            print("\n That's not an int! \n please make sure you type the right choice")
                  

                  

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
    global df
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    if month != "":
        datetime_object = datetime.datetime.strptime(month, "%B")
        month_number = datetime_object.month
        df = df[df['Start Time'].dt.month == month_number]
    
    if day != "":
        rday= day - 1
        df = df[df['Start Time'].dt.weekday == rday]
     
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    start_time = time.time()
    df['Start Time']= pd.to_datetime(df['Start Time'])
    
    # display the most common month
    if month ==  "":
        ds = df.groupby(df['Start Time'].dt.strftime('%B'))['Unnamed: 0'].count().sort_values(ascending=False)
        ds.index.name = 'most common month'
        print("\n the most common month is {}".format(ds.idxmax()))
    

    # display the most common day of week
    if day == "":
        dd = df.groupby(df['Start Time'].dt.strftime('%A'))['Start Time'].count().sort_values(ascending=False)
        print("\n the most common day of week is {}".format(dd.idxmax()))

    # display the most common start hour
    
    dh = df.groupby(df['Start Time'].dt.strftime('%H'))['Start Time'].count().sort_values(ascending=False)
   
    print("\n the most common start hour is {}\n".format(dh.idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used Start station\n')       
    print(df.groupby('Start Station')['Start Station'].count().sort_values(ascending=False).idxmax())
    print('\n')
            
    # display most commonly used end station
    print('Most commonly used end station\n')
    print(df.groupby('End Station')['End Station'].count().sort_values(ascending=False).idxmax())
    print('\n')
    
    # display most commonly used station among all stations Start & End
    print('Most commonly used station\n')
    s5 = pd.DataFrame(df['Start Station'].append(df['End Station']), columns = ['All Stations'])
    print(s5.groupby('All Stations')['All Stations'].count().sort_values(ascending =False).idxmax())
    print('\n')        
            
    # display most frequent combination of start station and end station trip
    print('Most frequent combination of Start and End station\n')
    print(df.groupby(['Start Station','End Station']).size().sort_values(ascending = False).idxmax())
    print('\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    td = str(datetime.timedelta(seconds= int(df['Trip Duration'].sum())))
    print("\n Total Trips Duration is   {} \n".format(td))

    # display mean travel time
    Md = str(datetime.timedelta(seconds= int(df['Trip Duration'].mean())))
    print("\n The Average for Trips Duration is   {} \n".format(Md))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating Users\' Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Number of Users for each User Type\n")
    print(df.groupby('User Type')['User Type'].count())

    # Display counts of gender
    try: 
        print("Number of Users for each Gender\n")
        print(df.groupby('Gender')['Gender'].count())
    except:
        print("sorry, there is no gender data")

    # Display earliest, most recent, and most common year of birth
    try: 
        e_year = int(df['Birth Year'].min())
        r_year = int(df['Birth Year'].max())
        c_year = int(df['Birth Year'].mode())
        print("the Birth year for the following \n the earliest year of birth is : {} . \n the recent year of Birth is : {}. \n the most common year of birth is : {}. ".format(e_year,r_year,c_year))
    except:
        print("sorry, there is no Birth year data")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """Dispalys individual rows of data"""
    
    view_data = ""
    start_loc = 0
    while view_data not in ('y','n'):
            view_data = input('\nWould you like to view 5 rows of individual trip data? Enter \"Y\" For yes or \"N\" for no \n').lower()
    while (view_data == "y"):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: Enter \"Y\" For yes or \"N\" for no ").lower()
        while view_data not in ('y','n'):
            view_data = input('\n please  Enter yes or no\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter \"Y\" For yes or \"N\" for no\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()