"""
Style change re-write of Emma code obtained from 
http://ieeexplore.ieee.org/document/7552572/figures?reload=true&part=1
"""
import sys
import re
import math
import operator

DEBUG = False
ARR_SIZE = 20  # if we want to store more values 
DETECTION_FREQ_VAL = 20
AVG_NUM_MAGNITUDES = 10  # average number of magnitudes between peaks
SLOPE_START = -1
SLOPE_CHANGED = 1

# other possibly paramaterized values:
# MOVING_SUM_DENOMINATOR
# MOD_VALUE a denominator 

def read_data(filename, data_line_num=7):
    with open(filename, 'r', encoding='utf-8') as data_file:
        for line_num, line in enumerate(data_file):
            if line_num == data_line_num:  # starting line number of raw data values
                return map(int,re.findall(r'\d+',line))
    return None
    
def find_peaks(magnitudes_all):
    array_idx = 0
    moving_sum = 0
    u_acc = [0] * ARR_SIZE  # not sure of this arrays purpose
    u_acc0 = [0] * ARR_SIZE
    filtered_data = [0] * ARR_SIZE
    
    last_slope = -1
    last_true_min = True

    steps = 0

    for magnitude_value_raw in magnitudes_all:
        # Part A: 'pre-process' the data
        magnitude_value = pre_process_magnitude(magnitude_value_raw)
        moving_sum = moving_sum - u_acc[array_idx] + magnitude_value
        u_acc[array_idx] = magnitude_value
        u_acc0[array_idx] = magnitude_value - moving_sum/DETECTION_FREQ_VAL  # or MOVING_SUM_DENOMINATOR
        # Part B: Filter the Data
        filtered_data[array_idx] = output_function(u_acc0,
                                                   array_idx + DETECTION_FREQ_VAL,
                                                   mod_value = DETECTION_FREQ_VAL, 
                                                   denom = 16)

        # Part C: Peak Detection Phase
        slope = SLOPE_START         # reset slope value for this magnitude
        if DEBUG:
            print("filtered data: {}\t{}\n".format(filtered_data[array_idx], filtered_data[(array_idx+20 - 1) % 20]))
        
        if filtered_data[array_idx] > filtered_data[(array_idx+DETECTION_FREQ_VAL - 1)
                                                    % DETECTION_FREQ_VAL]:
            slope = SLOPE_CHANGED # somewhat arbitrary value; could refine

        
        if (last_slope != slope): # if we have changed directionality WRT peaks!
            avg_threshold = determine_avg_threshold(filtered_data, array_idx, start_value = 0)
            if DEBUG:
                print(avg_threshold)
            # negative to positive
            if (last_slope == SLOPE_START and slope == SLOPE_CHANGED):
                if not last_true_min and filtered_data[array_idx] < avg_threshold:
                    last_true_min = True

            # positive to negative --> we have a step
            if (last_slope == SLOPE_CHANGED and slope == SLOPE_START):
                if last_true_min and filtered_data[array_idx] > avg_threshold:
                    last_true_min = False
                    steps +=1

        last_slope = slope
        array_idx = (array_idx + 1) % DETECTION_FREQ_VAL

    return steps


def pre_process_magnitude(magnitude_value_raw):
    """ 
    Helper function for find_peaks
    Though small, this is a separate helper function for future ease of refactoring
    """
    return math.sqrt(magnitude_value_raw)


def output_function(acc_array, n, mod_value = 20, denom = 16):
    """
    Output function: broken out for future refactors
    Helper function for find_peaks
    y[n] = 1/16(x[n] + 2x[n-1] + 3x[n-2] + 4x[n-3] + 3x[n-4] + 2x[n-5] + x[n-6])

    [QUESTION] Missing x term??
    [FUTURE] recursive expansion of formula?

    Parameters
    acc_array, array[int]:
    n, int:
    mod_value, int:
    denom, int:

    """
    # this is unnec. but IMHO i can read this easier
    sum_of_terms = acc_array[n %mod_value] + \
                   2 * acc_array[(n - 1)%mod_value] + \
                   3 * acc_array[(n - 2)%mod_value] + \
                   4 * acc_array[(n - 3)%mod_value] + \
                   3 * acc_array[(n - 4)%mod_value] + \
                   2 * acc_array[(n - 5)%mod_value] + \
                   acc_array[(n-6)%mod_value]

    return sum_of_terms/denom  # can be changed to fsum


def determine_avg_threshold(filtered_data, array_idx, start_value = 0):
    """
    Helper Function for find_peaks
    """
    n = AVG_NUM_MAGNITUDES
    avg_threshold = start_value
    for j in range(n):
        avg_threshold += filtered_data[(array_idx - j + DETECTION_FREQ_VAL) 
                                       % DETECTION_FREQ_VAL]
    div_avg_threshold = avg_threshold/n
    return div_avg_threshold 

if __name__ == '__main__':
    magnitudes_all = read_data(sys.argv[1])
    steps = find_peaks(magnitudes_all)

    print(steps)
