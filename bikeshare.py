import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {'All': 'all', 'Jan': 'january', 'Feb': 'february', 'Mar': 'march',
              'Apr': 'april', 'May': 'may', 'Jun': 'june'}

DAY_DATA = {'All': 'all', 'Sun': 'Sunday', 'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday',
            'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday'}


def check_filter(filt):
    """ Checks user input matches the prescibed list of filter options """
    return filt not in ['Raw', 'Format']


def check_month(month):
    """ Checks user input matches the prescribed list of month options """
    return month not in ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']


def check_day(day):
    """ Checks user input matches the prescribed list of day options """
    return day not in ['All', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def convert_seconds(seconds):
    """
    Takes seconds and converts them into days, hours, minutes and seconds. Will not include
    days, hours or minutes if there are not enough seconds to make a whole unit.

    Returns:
    A formatted string ready for displaying
    """
    or_word, day, hour, mins, secs = ' or ', '', '', '', seconds
    if secs // (24 * 3600) > 0:
        day = or_word + str(format_num(int(secs // (24 * 3600)))) + ' Days, '
        secs = secs % (24 * 3600)
        or_word = ''
    if secs // 3600 > 0:
        hour = or_word + str(secs // 3600) + ' Hours, '
        secs %= 3600
        or_word = ''
    if secs // 60 > 0:
        mins = or_word + str(secs // 60) + ' Minutes, '
        secs %= 60
    if secs > 0:
        secs = str(secs) + ' Seconds'
    return "{} Seconds{}{}{}{}".format(format_num(seconds), day, hour, mins, secs)


def format_num(num):
    """ Returns the provided number formatted with , to denote thousands e.g. 56789 becomes 56,789 """
    return f"{int(num):,d}"


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = input('Which City would you like to analyze? [Chicago, New York City or Washington] ')
    while city_input.lower() not in CITY_DATA:
        city_input = input('\n"' + city_input + '" not recognised!, enter only Chicago, New York City or Washington: ')
    city = city_input.lower()
    # get user input for month (all, january, february, ... , june)
    month = input('Enter Month to filter by: [All, Jan, Feb, Mar, Apr, May, Jun] ')
    while check_month(month):
        month = input('\n"' + month + '" not recognised! Enter only All, Jan, Feb, Mar, Apr, May, or Jun: ')
    month = MONTH_DATA[month]
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter Weekday to filter by: [All, Sun, Mon, Tue, Wed, Thu, Fri, Sat] ')
    while check_day(day):
        day = input('\n"' + day + '" not recognised! Enter only All, Sun, Mon, Tue, Wed, Thu, Fri, Sat: ')
    day = DAY_DATA[day]

    filtered = input('Would you like to see Raw or Formatted Data? [Raw or Format] ')
    while check_filter(filtered):
        filtered = input('\n"' + filtered + '" not recognised! Enter only Raw or Format: ')
    print('-' * 40)
    return city, month, day, filtered


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
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_name = calendar.month_name[df['month'].mode()[0]]
    print('The most common month of the year is: {}'.format(month_name))

    # TO DO: display the most common day of week
    print('The most common day of the week is: {}'.format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    start_hour = df['start_hour'].mode()[0]
    is_morning = (start_hour >= 0) and (start_hour < 12)
    if is_morning:
        start_hour = str(start_hour) + ' am'
    else:
        start_hour = str((start_hour - 12)) + ' pm'
    print('The most common hour to start is: {}'.format(start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most popular Start Station was: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The most popular End Station was: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    row = df.groupby(['Start Station', 'End Station']).size().reset_index(name='trip_count') \
        .sort_values(by='trip_count', ascending=False).head(1).values[0]
    start = row[0]
    end = row[1]
    stn_count = format_num(row[2])

    print('The most popular trip started at {} and ended at {}, a total of {} times'.format(start, end,
                                                                                            stn_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_seconds = df['Trip Duration'].sum()
    # print(total_seconds)
    if total_seconds < 1:
        print("Unable to provide a total or mean travel time!")
    else:
        # TO DO: display total travel time
        print('A total travel time of ' + convert_seconds(total_seconds))
        # TO DO: display mean travel time
        mean_seconds = int(np.average(df['Trip Duration']))
        print('An average travel time of ' + convert_seconds(mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    customers = format_num(user_types['Customer'])
    subscribers = format_num(user_types['Subscriber'])
    print('Your filtered data shows a total of {} Customers and {} Subscribers'.format(customers, subscribers))
    # TO DO: Display counts of gender
    if city == 'washington':
        print('\nGender and Birthday information are not available for Washington, sorry!')
    else:
        genders = df['Gender'].value_counts()
        male = format_num(genders['Male'])
        female = format_num(genders['Female'])
        print('Your filtered data shows {} Male users and {} Female users'.format(male, female))
        # TO DO: Display earliest, most recent, and most common year of birth
        print('The earliest Birth Year filtered was: {}'.format(int(df['Birth Year'].min())))
        print('The most recent Birth Year found was: {}'.format(int(df['Birth Year'].max())))
        print('The most common Birth Year found was: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    raw_count = 0
    while True:
        city, month, day, filtered = get_filters()
        df = load_data(city, month, day)
        # shortcut to save time typing
        # df = load_data('chicago', 'april', 'saturday')
        if filtered == 'Raw':
            while True:
                print(df.iloc[raw_count:raw_count + 5])
                raw_count += 5
                show_more = input('\nWould you like to see more? [y] ')
                if show_more != 'y':
                    break
            break
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)
            restart = input('\nWould you like to restart? [y]')
            if restart != 'y':
                break


if __name__ == "__main__":
    main()
