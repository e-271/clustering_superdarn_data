""" Data sandbox """


# ~~ Get data ~~
from superdarn_cluster.dbtools import flatten_data_11_features, read_db, get_scan_nums
import datetime as dt
from superdarn_cluster.time_utils import *

year, month, day = 2018, 2, 7
rad = 'sas'

start_time = dt.datetime(year, month, day)
end_time = dt.datetime(year, month, day+1)
date_str = '%d-%02d-%02d' % (year, month, day)
db_path = "./Data/%s_GSoC_%s.db" % (rad, date_str)
data_dict = read_db(db_path, rad, start_time, end_time)
data_flat_unscaled = flatten_data_11_features(data_dict, remove_close_range=False)

feature_names = ['beam', 'gate', 'vel', 'wid', 'power', 'freq', 'time', 'phi0', 'elev', 'nsky', 'nsch']

gate = data_flat_unscaled[:, 1]
power = data_flat_unscaled[:, 4]
beam = data_flat_unscaled[:, 0]
vel = data_flat_unscaled[:, 2]
wid = data_flat_unscaled[:, 3]
time_num_days = data_flat_unscaled[:, 6]
time_sec = time_days_to_sec(time_num_days)
time_index = time_sec_to_index(time_sec)
scan_nums = get_scan_nums(beam)

gate_scans = []
beam_scans = []
vel_scans = []
import pickle

for s in np.unique(scan_nums):
    scan_mask = scan_nums == s
    gate_scans.append(gate[scan_mask])
    beam_scans.append(beam[scan_mask])
    vel_scans.append(vel[scan_mask])

data = {'gate' : gate_scans, 'beam' : beam_scans, 'vel' : vel_scans}
filename = "./pickles/%s_%s_scans.pickle" % (rad, date_str)
pickle.dump(data, open(filename, 'wb'))