import numpy as np
from sortedcontainers import SortedDict


class bb_math:

    def __init__(self):
        self.input_dict = SortedDict({1506379680: 3934, 1506379920: 3925, 1506380460: 3933.9, 1506379620: 3949.4, 1506380280: 3933.9, 1506380520: 3927.54, 1506379560: 3950, 1506379500: 3950, 1506380100: 3925.1, 1506379980: 3925, 1506380400: 3933.9, 1506380340: 3930, 1506379440: 3950, 1506380040: 3925.1, 1506380160: 3933.99, 1506379860: 3925, 1506380580: 3927.54, 1506379800: 3935, 1506379380: 3945, 1506380220: 3934, 1506379740: 3935})
        self.running_avg = {}
        self.std_value = None
        self.upper_line = None
        self.lower_line = None



    def moving_average(self, x, N):
        if (len(x)<N):
            #print("x<N")
            return x[0]
        else:
            #print("x>N")
            #print(np.convolve(x, np.ones((N,)) / N)[(N-1):])
            #return np.convolve(x, np.ones((N,)) / N)[1:]
            #print(np.convolve(x, np.ones((N,)) / N, mode='valid')[-1:])
            return np.convolve(x, np.ones((N,)) / N, mode='valid')[-1:][0]


    def moving_average_dict(self, sorted_dict):
        tmp_lst = []
        #tmp_lst_mov = []
        #tmp_var = None
        for item in sorted_dict.keys():
            time_st = item
            price = sorted_dict[item]
            tmp_lst.append(price)
            tmp_var = self.moving_average(tmp_lst, 3)
            #tmp_lst_mov.append(tmp_var)
            self.running_avg[item] = tmp_var
        #print(tmp_lst_mov)
        #print(len(tmp_lst_mov))
        #print(self.running_avg)
        self.running_avg = SortedDict(self.running_avg)
        #print(self.running_avg)
        #print(len(self.running_avg))
        return self.running_avg


    def bb_std(self, sorted_dict):
        self.std_value = np.std(sorted_dict.values())
        self.std_value = float(self.std_value)
        print(self.std_value)
        return self.std_value

    def bb_upper_line(self):
        #print(float(self.running_avg.values()[-1:][0]))
        self.upper_line = float(self.running_avg.values()[-1:][0]) + (2 * self.std_value)
        #print(self.upper_line)
        return self.upper_line

    def bb_lower_line(self):
        #print(float(self.running_avg.values()[-1:][0]))
        self.lower_line = float(self.running_avg.values()[-1:][0]) - (2 * self.std_value)
        #print(self.lower_line)
        return self.lower_line



def main():
    pass

    math = bb_math()
    print(math.input_dict)
    print(len(math.input_dict))
    math.running_avg = math.moving_average_dict(math.input_dict)
    math.std_dict = math.bb_std(math.input_dict)
    math.upper_line = math.bb_upper_line()
    math.lower_line = math.bb_lower_line()


    #print(math.running_avg)
    #print(len(math.running_avg))







if __name__ == "__main__":
    main()