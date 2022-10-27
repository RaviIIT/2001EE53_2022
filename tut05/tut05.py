import pandas as pd
import math
from datetime import datetime
start_time = datetime.now()

def octant_range_names(mod = 5000):

    octant_name_id_mapping = {"1":"Internal outward interaction", "-1":"External outward interaction", "2":"External Ejection", "-2":"Internal Ejection", "3":"External inward interaction", "-3":"Internal inward interaction", "4":"Internal sweep", "-4":"External sweep"}

    # error handling if file unable to open
    try:
        outp = pd.read_excel('octant_input.xlsx')

        # stored average of each column in input
        u_avg = outp['U'].mean()
        v_avg = outp['V'].mean()
        w_avg = outp['W'].mean()

        # entered average values in a list
        u_avg_col = [u_avg]
        v_avg_col = [v_avg]
        w_avg_col = [w_avg]

        # filled remaininig cells of average column
        u_avg_col.extend(['']*(len(outp['U'])-1))
        v_avg_col.extend(['']*(len(outp['V'])-1))
        w_avg_col.extend(['']*(len(outp['W'])-1))

        try:
            # entered average column in outp variable
            outp["U Avg"] = u_avg_col
            outp["V Avg"] = v_avg_col
            outp["W Avg"] = w_avg_col
        except:
            print('Error : Mismatch in length of Average quantities columns.')

        u_dash = []
        v_dash = []
        w_dash = []

        # computed other columns
        for i in outp['U']:
            u_dash.append(i - u_avg)

        for i in outp['V']:
            v_dash.append(i - v_avg)

        for i in outp['W']:
            w_dash.append(i - w_avg)

        try:
            # entered the columns in outp variable
            outp["U\'=U - U avg"] = u_dash
            outp["V\'=V - V avg"] = v_dash
            outp["W\'=W - W avg"] = w_dash
        except:
            print('Error : Mismatch in length of colums.')

        # created Octant value column
        octant_col = []
        x = []
        y = []
        z = []

        cnt = len(outp['U'])

        # filled x,y,z lists
        for i in outp["U\'=U - U avg"]:
            x.append(i)
        for i in outp["V\'=V - V avg"]:
            y.append(i)
        for i in outp["W\'=W - W avg"]:
            z.append(i)

        itr = math.ceil(cnt/mod)

        single_freq = {}

        # computed frequency of each octant in whole range
        for i in range(1, 5):
            single_freq[i] = 0
            single_freq[0-i] = 0

        # finding octant values of each row
        for i in range(cnt):
            cur = i/mod
            cur = cur*mod

            if x[i] > 0 and y[i] > 0:  # 1st quadrant
                if z[i] > 0:
                    octant_col.append(1)
                    single_freq[1] += 1
                else:
                    octant_col.append(-1)
                    single_freq[-1] += 1
            elif x[i] < 0 and y[i] > 0:  # 2nd quadrant
                if z[i] > 0:
                    octant_col.append(2)
                    single_freq[2] += 1
                else:
                    octant_col.append(-2)
                    single_freq[-2] += 1
            elif x[i] < 0 and y[i] < 0:  # 3rd quadrant
                if z[i] > 0:
                    octant_col.append(3)
                    single_freq[3] += 1
                else:
                    octant_col.append(-3)
                    single_freq[-3] += 1
            elif x[i] > 0 and y[i] < 0:  # 4th quadrant
                if z[i] > 0:
                    octant_col.append(4)
                    single_freq[4] += 1
                else:
                    octant_col.append(-4)
                    single_freq[-4] += 1

        try:
            outp["Octant"] = octant_col
        except:
            print('Error : Mismatch in length of Octant')

        # entered new column
        user_input = ['', "User Input"]

        user_input.extend(['']*(len(outp['U']) - len(user_input)))

        # error handling if column length is mismatched
        try:
            outp[' '] = user_input
        except:
            print('Error encountered : Mismatch in length of column.')

        # formed "Octant ID" column
        octant_id = ["Overall Count", 'Mod ' + str(mod)]

        # formed the ranges of Octand_ID column
        for i in range(itr):
            num1 = mod*i
            num2 = (mod*(i+1)) - 1
            if num2 > cnt:
                num2 = cnt - 1

            str_range = str(num1) + '-' + str(num2)
            octant_id.append(str_range)

        octant_id.extend(['']*(len(outp['U']) - len(octant_id)))

        # error handling if column length is mismatched
        try:
            # entered "Octant ID" column
            outp[''] = octant_id
        except:
            print('Error encountered : Mismatch in length of columns in Octant ID column')

        # iterating for each octant value for range frequency
        for i in range(1, 5):

            # computing for +i octant value
            col_one = [single_freq[i], '']

            # iterating for each range
            for w in range(itr):
                sums = 0
                num1 = w*mod
                num2 = (mod*(w+1)) - 1
                if num2 > cnt:
                    num2 = cnt

                # finding number of elements in each range
                for q in range(cnt):
                    if octant_col[q] == i and num1 <= q and q <= num2:
                        sums += 1

                col_one.append(sums)

            col_one.extend(['']*(len(outp['U']) - len(col_one)))

            # error handling if column length is mismatched
            try:
                # filled +i octant column in outp variable
                outp[i] = col_one
            except:
                print('Error encountered : Mismatch in length of some octant ids column.')

            # computing for -i octant value
            col_one = [single_freq[0-i], '']
            # iterating for each range
            for w in range(itr):
                sums = 0
                num1 = w*mod
                num2 = (mod*(w+1)) - 1
                if num2 > cnt:
                    num2 = cnt
                # finding number of elements in each range
                for q in range(cnt):
                    if octant_col[q] == (0-i) and num1 <= q and q <= num2:
                        sums += 1

                col_one.append(sums)

            # filled the remaining cells of the column
            col_one.extend(['']*(len(outp['U']) - len(col_one)))

            try:
                # filled -i octant column in outp variable
                outp[0-i] = col_one
            except:
                print('Error encountered while entering -ve octant id columns')
        
        # initially filled all cells as empty then filled values in them
        rank_one_octant = []
        rank_one_octant.extend(['']*len(outp['U']))

        # iterating for each octant rank finding
        for i in range(1, 5):

            # for +i octant id
            rank_col = []
            ar_cmp = []

            # inserting values in a list to calculate rank
            for w in range(1, 5):
                ar_cmp.append([outp[w][0], w])
                ar_cmp.append([outp[0-w][0], 0-w])

            ar_cmp.sort(reverse=True)

            # finding rank
            for w in range(len(ar_cmp)):
                if ar_cmp[w][1] == i:
                    if w == 0:
                        rank_one_octant[0] = i
                    rank_col.append(w+1)
                    break

            rank_col.append(' ')
            
            # iterating for each range for a particular octant id
            for w in range(itr):
                ar_cmp = []

                # inserting values in a list to calculate rank
                for b in range(1, 5):
                    ar_cmp.append([outp[b][2+w], b])
                    ar_cmp.append([outp[0-b][2+w], 0-b])

                ar_cmp.sort(reverse=True)

                # finding rank
                for b in range(len(ar_cmp)):
                    if ar_cmp[b][1] == i:
                        if b == 0:
                            rank_one_octant[2 + w] = i
                        rank_col.append(b+1)
                        break

            rank_col.extend(['']*(len(outp['U']) - len(rank_col)))

            # try catch statements for error checking
            try:
                outp['Rank '+str(i)] = rank_col
            except:
                print('Error : Mismatch in length of Rank column during +ve octant entering')

            # proceeding the same as above for -i octant id
            rank_col = []
            ar_cmp = []

            for w in range(1, 5):
                ar_cmp.append([outp[w][0], w])
                ar_cmp.append([outp[0-w][0], 0-w])

            ar_cmp.sort(reverse=True)

            # finding rank for -ve octant id
            for w in range(len(ar_cmp)):
                if ar_cmp[w][1] == (0-i):
                    if b == 0:
                        rank_one_octant[2 + w] = i
                    rank_col.append(w+1)
                    break

            rank_col.append(' ')
            
            # iterating for each range for a particular octant id
            for w in range(itr):
                ar_cmp = []

                for b in range(1, 5):
                    ar_cmp.append([outp[b][2+w], b])
                    ar_cmp.append([outp[0-b][2+w], 0-b])

                ar_cmp.sort(reverse=True)

                for b in range(len(ar_cmp)):
                    # print(ar_cmp[b][0])
                    if ar_cmp[b][1] == (0-i):
                        if b == 0:
                            rank_one_octant[2 + w] = 0-i
                        rank_col.append(b+1)
                        break

            rank_col.extend(['']*(len(outp['U']) - len(rank_col)))

            # try catch statements for error avoidance
            try:
                outp['Rank '+str(0-i)] = rank_col
            except:
                print(
                    'Error : Mismatch in length of Rank column during -ve octant entering')

        # try catch statements for error avoidance
        try:
            outp['Rank1 Octant ID'] = rank_one_octant
        except:
            print('Error : Mismatch in rank1 octant id column')
        
        # inserting values into list by lookup from given dictionary
        rank_one_name = []
        rank_one_name.append(octant_name_id_mapping[rank_one_octant[0]])
        rank_one_name.append('')

        for i in range(itr):
            rank_one_name.append(octant_name_id_mapping[rank_one_octant[2+i]])

        rank_one_name.extend(['']*(len(outp['U']) - len(rank_one_name)))

        try:
            outp['Rank1 Octant Name'] = rank_one_name
        except:
            print('Error : Mismatch in length og rank1 octant name')

        # entering the lower terms of excel sheet
        cur_cnt = itr+5
        outp[1][cur_cnt] = 'Octant ID'
        cur_cnt = cur_cnt + 1

        for i in range(1, 5):
            outp[1][cur_cnt] = i
            outp[1][cur_cnt+1] = 0-i
            cur_cnt = cur_cnt + 2

        cur_cnt = itr+5
        outp[-1][cur_cnt] = 'Octant Name'
        cur_cnt = cur_cnt + 1
        
        # entering names terms of given dictionary
        for i in range(1, 5):
            outp[-1][cur_cnt] = octant_name_id_mapping[i]
            outp[-1][cur_cnt+1] = octant_name_id_mapping[0-i]
            cur_cnt = cur_cnt + 2

        cur_cnt = itr+5
        outp[2][cur_cnt] = 'Count of Rank 1 Mod Values'
        cur_cnt = cur_cnt + 1
        
        # inserting count of rank1 mod values
        for i in range(1, 5):
            sums = 0
            for w in range(2, 2+itr):
                if outp['Rank1 Octant ID'][w] == i:
                    sums = sums + 1
            outp[2][cur_cnt] = sums

            sums = 0
            for w in range(2, 2+itr):
                if outp['Rank1 Octant ID'][w] == (0-i):
                    sums = sums + 1
            outp[2][cur_cnt+1] = sums
            cur_cnt = cur_cnt+2

        # error handling if unable to write to output file.
        try:
            # wrote everything present in outp variable to 'output_octant_transition_identify.xlsx' file
            outp.to_excel('octant_output_ranking_excel.xlsx', index=0)
        except:
            print('Error encountered : While writing excel file.')
    except:
        print("Error encountered")


mod = 5000
octant_range_names(mod)

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
