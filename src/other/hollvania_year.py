"""
the Hex quest drops at 2024-12-13 (Fri)
Assumes that week AND the next week is 2000 winter, then 2024-12-16 is 2000 winter, 2024-12-23 is 2000 spring, etc
"""
import datetime

SEASON = ["Winter", "Spring", "Summer", "Fall"]

start_date = datetime.date(2024, 12, 16)
start_year = 2000
start_season = 0    # winter

cur_date = datetime.date.today()
delta_weeks = (cur_date - start_date).days // 7
cur_year = start_year + (delta_weeks // 4)
cur_season = (start_season + (delta_weeks % 4)) % 4

print('Current Hollvania year:', cur_year, SEASON[cur_season])