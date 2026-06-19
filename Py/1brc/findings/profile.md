Wrote profile results to '1brc_profile.py.lprof'
Timer unit: 1e-06 s

Total time: 0.000333 s
File: 1brc_profile.py
Function: parse_c_optimized at line 4

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     4                                           @profile
     5                                           def parse_c_optimized(line):
     6                                               # Using C-backend .partition and float()
     7      1000        132.0      0.1     39.6      station, _, temp_str = line.partition(";")
     8      1000         96.0      0.1     28.8      temp = float(temp_str)
     9      1000        105.0      0.1     31.5      return station, temp

Total time: 0.000593 s
File: 1brc_profile.py
Function: parse_python_vm at line 12

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    12                                           @profile
    13                                           def parse_python_vm(line):
    14                                               # Using pure Python slicing and concatenation
    15      1000        120.0      0.1     20.2      sep_idx = line.find(";")
    16      1000        105.0      0.1     17.7      station = line[:sep_idx]
    17      1000         91.0      0.1     15.3      temp_str = line[sep_idx + 1 : -1]
    18      1000        134.0      0.1     22.6      temp = int(temp_str[:-2] + temp_str[-1:])
    19      1000        143.0      0.1     24.1      return station, temp

Total time: 0.000331 s
File: 1brc_profile.py
Function: parse_split at line 22
