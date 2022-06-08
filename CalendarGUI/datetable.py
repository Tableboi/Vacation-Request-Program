import pandas as pd

start = '1/1/2022'
end = '12/31/2022'
df = pd.DataFrame(pd.date_range(start, end, freq = "H", tz = 'EST'), columns = ['Datetime'])
df['LocaleTime'] = df["Datetime"].dt.strftime('%c')
df['Day'] = df["Datetime"].dt.day
df['Month'] = df["Datetime"].dt.month
df['Year'] = df["Datetime"].dt.year
df['time'] = df["Datetime"].dt.time
df['timezone'] = df["Datetime"].dt.tz
df['Hour'] = df["Datetime"].dt.hour
df['Quarter'] = df["Datetime"].dt.quarter
df['MonthName'] = df["Datetime"].dt.strftime('%b')
df['Week Name'] = df["Datetime"].dt.strftime('%A')
df['WeekNumber'] = df["Datetime"].dt.strftime('%W')
df['Weekday'] = df["Datetime"].dt.weekday
df['TimeofDay'] = df["Datetime"].dt.strftime('%p')
df['UTC_offset'] = df["Datetime"].dt.strftime('%z')
df['DayofYear'] = df["Datetime"].dt.dayofyear
df['Century'] = df["Datetime"].dt.strftime('%Y')