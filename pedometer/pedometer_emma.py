# Emma Oberstein
# example usage: python pedometer.py test_files/EO_Walking
# output: 66
# based on http://ieeexplore.ieee.org/document/7552572/figures?part=1
from sys import argv
import re, math

if __name__ == '__main__':
    fp = open(argv[1])
    # import the magnitudes from the file
    for line_num, line in enumerate(fp):
        if line_num == 7:
            magnitudes = map(int,re.findall(r'\d+',line))
    fp.close()
    # globals
    array_index = 0
    moving_sum = 0
    u_acc = [0] * 20
    u_acc0 = [0] * 20
    filtered_data = [0] * 20
    last_slope = -1
    last_true_min = True
    steps = 0
    fi = []
    ''' our stream of inputs (wont come in as magnitudes
        in amulet but this is how test data was logged) '''
    for magnitude in magnitudes:
        # Part A: Data Preprocessing Phase
        new_value = math.sqrt(magnitude)  # not sure teh point of these two sep 
        moving_sum = moving_sum - u_acc[array_index] + new_value
        u_acc[array_index] = new_value
        u_acc0[array_index] = new_value - moving_sum/20
        # Part B: Data Filtering Phase
        # output function y[n] = 1/16(x[n] + 2x[n-1] + 3x[n-2] + 4x[n-3] + 3x[n-4] + 2x[n-5] + x[n-6])
        n = array_index + 20
        filtered_data[array_index] = (u_acc0[n%20] + 2 * u_acc0[(n-1)%20] + 3 * u_acc0[(n-2)%20] + 4 * u_acc0[(n-3)%20] + 3 * u_acc0[(n-4)%20] + 2 * u_acc0[(n-5)%20] + u_acc0[(n-6)%20])/16
        # Part C: Peak Detection Phase
        slope = -1
        print("filtered data: {}\t{}\n".format(filtered_data[array_index], filtered_data[(array_index+20 - 1) % 20]))

        if filtered_data[array_index] > filtered_data[(array_index+20-1)%20]:
            slope = 1
        if (last_slope != slope):
            avg_threshold = 0
            n = 10
            for j in range(n):
                avg_threshold +=  filtered_data[(array_index-j+20) % 20]
            avg_threshold = avg_threshold/n
            # negative to positive
            if (last_slope == -1 and slope == 1):
                if not last_true_min and filtered_data[array_index] < avg_threshold:
                    last_true_min = True
            # positive to negative
            if (last_slope == 1 and slope == -1):
                if last_true_min and filtered_data[array_index] > avg_threshold:
                    last_true_min = False
                    steps +=1
        last_slope = slope
        array_index = (array_index + 1) % 20
    print(steps)
