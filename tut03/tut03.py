import pandas as pd
import math

from datetime import datetime
start_time = datetime.now()

def octant_longest_subsequence_count():
      # stored excel file in a variable and took indexing on 0th column
    
    # error handling if input file do not exists
    try:
          inp = pd.read_excel('input_octant_longest_subsequence.xlsx', index_col = 0)

          ## stored average of each column in input
          u_avg = inp['U'].mean()
          v_avg = inp['V'].mean()
          w_avg = inp['W'].mean()

          ## wrote output to output file in column wise manner
          inp.to_excel('output_octant_longest_subsequence.xlsx')

          # entered average values in a list
          u_avg_col = [u_avg]
          v_avg_col = [v_avg]
          w_avg_col = [w_avg]

          # filled remaininig cells of average column
          u_avg_col.extend(['']*(len(inp['U'])-1))
          v_avg_col.extend(['']*(len(inp['V'])-1))
          w_avg_col.extend(['']*(len(inp['W'])-1))

          # read the output excel file
          outp = pd.read_excel('output_octant_longest_subsequence.xlsx', index_col = 0)

          try:
                # entered average column in outp variable
                outp["U Avg"] = u_avg_col
                outp["V Avg"] = v_avg_col
                outp["W Avg"] = w_avg_col
          except:
                print('Error encountered : Mismatch in column length in Average colms entering.')
                
          u_dash = []
          v_dash = []
          w_dash = []

          # computed other columns
          for i in inp['U']:
              u_dash.append(i - u_avg)

          for i in inp['V']:
              v_dash.append(i - v_avg)

          for i in inp['W']:
              w_dash.append(i - w_avg)
          
          try:
                # entered the columns in outp variable
                outp["U\'=U - U avg"] = u_dash
                outp["V\'=V - V avg"] = v_dash
                outp["W\'=W - W avg"] = w_dash
          except:
                print('Error encountered : Mismatch in length of column of Values - Mean value.')
                  
          # created Octant value column
          octant_col = []
          x = []
          y = []
          z = []

          cnt = len(inp['U'])

          # filled x,y,z lists
          for i in outp["U\'=U - U avg"]:
              x.append(i)
          for i in outp["V\'=V - V avg"]:
              y.append(i)
          for i in outp["W\'=W - W avg"]:
              z.append(i)



          # finding octant values of each row
          for i in range(cnt):

              if x[i] > 0 and y[i] > 0:   #1st quadrant
                  if z[i] > 0:
                      octant_col.append(1)
                  else:
                      octant_col.append(-1)
              elif x[i] < 0 and y[i] > 0:   #2nd quadrant
                  if z[i] > 0:
                      octant_col.append(2)
                  else:
                      octant_col.append(-2)
              elif x[i] < 0 and y[i] < 0:   #3rd quadrant
                  if z[i] > 0:
                      octant_col.append(3)
                  else:
                      octant_col.append(-3)
              elif x[i] > 0 and y[i] < 0:   #4th quadrant
                  if z[i] > 0:
                      octant_col.append(4)
                  else:
                      octant_col.append(-4)
          
          try:
                outp["Octant"] = octant_col
          except:
                print('Error : Mismatch in length of octant columns.')

          # entered empty column in sheet
          empty_col = []
          empty_col.extend(['']*(len(inp['U'])))
          outp[' '] = empty_col

          # created 2 dictionary
          dictn_len = {}            # dictionary for maximum subsequence length of octant values
          dictn_cnt = {}            # dictionary for count of maximum subsequence length of octant values

          # initialised dictionary elements with 0
          for i in range(1,5):
            dictn_len[i] = 0
            dictn_cnt[i] = 0
            dictn_len[0-i] = 0
            dictn_cnt[0-i] = 0

          # updating maximum subsequence length of each octant id in dictn_len
          for w in range(cnt):
            counts = 0                          # variable to store length of current subsequence

            for q in range(w, cnt):
              if octant_col[q] == octant_col[w]:      # if same octant id found incrementing count
                counts += 1

                if q == (cnt - 1):                    
                  w = q
              else:                                   # else breaking loop and updating subsequence length
                w = q-1
                break

            dictn_len[octant_col[w]] = max(counts, dictn_len[octant_col[w]])

          # looping over all octant ids
          for i in range(1,5):

            # finding maximum subsequence length's count for +i octant value
            # maximum subsequence length = dictn_len[i]

            # iterating for each starting point of subsequence
            for w in range(cnt - dictn_len[i] + 1):
              flag = True

              # checking over the window of length dictn_len[i] starting from w
              for q in range(w, w + dictn_len[i]):
                if octant_col[q] != i:
                  flag = False
              # updating count if condition satisfied
              if flag == True:
                dictn_cnt[i] += 1


            # finding maximum subsequence length's count for -i octant value
            # maximum subsequence length = dictn_len[0-i]


            # iterating for each starting point of subsequence
            for w in range(cnt - dictn_len[0-i] + 1):
              flag = True

              # checking over the window of length dictn_len[i] starting from w
              for q in range(w, w + dictn_len[0-i]):
                if octant_col[q] != (0-i):
                  flag = False

              # updating count if condition satisfied
              if flag == True:
                dictn_cnt[0-i] += 1

          # for octant column declared a list and appending the respective octant values
          count_col = []
          for i in range(1,5):
            count_col.append(i)
            count_col.append(0-i)

          count_col.extend(['']*(len(inp['U']) - 8))
      
          try:
                # inserting column in outp variable
                outp['octant'] = count_col
          except:
                print('Error : Mismatch in octant column length.')

           # list for longest subsequence length and appending the values respectivelu by lookup from dictionary
          longest_len = []
          for i in range(1,5):
            longest_len.append(dictn_len[i])
            longest_len.append(dictn_len[0-i])

          longest_len.extend(['']*(len(inp['U']) - 8))
          
          try:
                # inserted the column into outp
                outp['Longest Subsequence Length'] = longest_len  
          except:
                print('Error : Mismatch in length of longest subsequence length columns')


          # list for longest subsequence length count
          longest_count = []
          for i in range(1,5):
            longest_count.append(dictn_cnt[i])
            longest_count.append(dictn_cnt[0-i])

          longest_count.extend(['']*(len(inp['U']) - 8))
      
          try:
                # inserted the column into outp
                outp['Count'] = longest_count
          except:
                print('Error : Mismatch in length of count of subsequences')
          
          try:
                # writing to output excel file
                outp.to_excel('output_octant_longest_subsequence.xlsx')
          except:
                print('Error happened while writing to excel file.')
      
    except:
          print('Error encountered: Input file not found.')          
      




octant_longest_subsequence_count()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
