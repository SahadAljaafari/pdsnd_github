import pandas as pd
from datetime import datetime
import time
from statistics import mean
import sys 

# Dictionary mapping city names to their corresponding CSV file paths
CITY_DATA = { 
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'  # 'yes' seems to be a placeholder, consider renaming it
}

# List of month names including 'All' for no filter
Months = ['All','January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November','December']

# List of days of the week including 'All' for no filter
days_of_week = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday', 'Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (name must match keys in CITY_DATA)
    city = input('Enter the city name: ').title()
    print(city)
    # Re-prompt until a valid city is entered
    while city not in CITY_DATA:
        city = input('Please reenter the city name: ').title()
    
    # Get user input for month (must match entries in Months list)
    month = input('Enter the month or "All" for no filter: ').title()
    while month not in Months:
        month = input('Please reenter the month or "All" for no filter: ').title()

    # Get user input for day of the week (must match entries in days_of_week list)
    day = input('Enter the day or "All" for no filter: ').title()
    while day not in days_of_week:
        day = input('Please reenter the day or "All" for no filter: ').title()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data from CSV file based on the city input
    df = pd.read_csv(CITY_DATA[city])
    new_df = pd.DataFrame(columns=df.columns)  # Create an empty DataFrame with the same columns as df

    # Filter by month if applicable
    if month != 'All':
        for indx, row in df.iterrows():
            try:
                # Try to parse date with seconds
                date_time_obj = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If above fails, try parsing without seconds
                date_time_obj = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M')
            
            # Convert date to month name
            month_conv = date_time_obj.strftime('%B')
            # If month matches, append row to new_df
            if month == month_conv:
                new_df = pd.concat([new_df, row.to_frame().T])

    # Filter by day of the week if applicable
    if day != 'All':
        for indx, row in new_df.iterrows():
            try:
                # Try to parse date with seconds
                date_time_obj = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                # If above fails, try parsing without seconds
                date_time_obj = datetime.strptime(row['Start Time'], '%Y-%m-%d %H:%M')
            
            # Convert date to day of the week
            day_conv = date_time_obj.strftime('%A')
            # If day does not match, drop the row from new_df
            if day != day_conv:
                new_df = new_df.drop(indx)

    # If no filtering is applied, use the original DataFrame
    if day == 'All' and month == 'All':
        new_df = df

    return new_df.reset_index(drop=True)  # Reset index and return the filtered DataFrame

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert 'Start Time' to datetime to extract time components
    try:
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    except ValueError:
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M')

    # Extract the month name from 'Start Time'
    df['months'] = df['Start Time'].dt.strftime('%B')
    # Display the most common month of travel
    max_months = df.groupby('months').size().idxmax()
    print('The most common month of travel is:', max_months)

    # Extract the day of the week from 'Start Time'
    df['Days'] = df['Start Time'].dt.strftime('%A')
    # Display the most common day of travel
    max_days = df.groupby('Days').size().idxmax()
    print('The most common day of travel is:', max_days)

    # Extract the hour from 'Start Time'
    df['Hours'] = df['Start Time'].dt.strftime('%H')
    # Display the most common hour of travel
    max_Hours = df.groupby('Hours').size().idxmax()
    print('The most common hour of travel is:', max_Hours)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is ', df.groupby('Start Station').size().idxmax())

    # Display most commonly used end station
    print('The most commonly used end station is ', df.groupby('End Station').size().idxmax())

    # Display most frequent combination of start station and end station trip
    print(df.groupby(['Start Station', 'End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    
    df['Total_Travel_Time'] = pd.NaT  # Initialize 'Total_Travel_Time' column with NaT values

    # Convert 'Start Time' and 'End Time' to datetime to calculate travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

    # Calculate 'Total_Travel_Time' using vectorized operations
    df['Total_Travel_Time'] = df['End Time'] - df['Start Time']

    # Display the total travel time for each trip
    print('The total travel time for each trip:')
    print(df['Total_Travel_Time'])

    # Convert timedelta to seconds and calculate the mean travel time
    mean_travel_time = df['Total_Travel_Time'].apply(lambda x: x.total_seconds()).mean()
    print("The mean travel time in seconds:", mean_travel_time)

    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types', df.groupby('User Type').size())

    # Display counts of gender, if available
    if 'Gender' in df.columns:
        print('Counts of gender', df.groupby('Gender').size())

    # Display earliest, most recent, and most common year of birth, if available
    if 'Birth Year' in df.columns:
        print('The most recent year of birth', df['Birth Year'].max())
        print('The earliest year of birth', df['Birth Year'].min())
        print('The common year of birth', df.groupby('Birth Year').size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

try:
    while True:
        # Get user inputs for city, month, day
        city, month, day = get_filters()
        df = load_data(city, month, day)

        while df.empty:  
            i = input('Sorry, the month or the day you chose is not available. Please enter 1 for new or 0 to exit: ')
            
            if i == '0':
                print("Exiting the program...")
                sys.exit() 

            elif i == '1':
                # Re-run the filters and load data again
                city, month, day = get_filters()
                df = load_data(city, month, day)
            else:
                print("Incorrect input. Please enter a valid value.")
        print(df)
        trip_duration_stats(df)
        time_stats(df)
        station_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            sys.exit()

except SystemExit:
    pass 

