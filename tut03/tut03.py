import pandas as pd
import math

from datetime import datetime
start_time = datetime.now()

def octant_longest_subsequence_count():
      # stored excel file in a variable and took indexing on 0th column
    inp = pd.read_excel('/content/sample_data/input_octant_longest_subsequence.xlsx', index_col = 0)
    
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
    
    # read the output.csv file
    outp = pd.read_excel('/content/output_octant_longest_subsequence.xlsx', index_col = 0)
    
    # entered average column in outp variable
    outp["U Avg"] = u_avg_col
    outp["V Avg"] = v_avg_col
    outp["W Avg"] = w_avg_col
    
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
    
    # entered the columns in outp variable
    outp["U\'=U - U avg"] = u_dash
    outp["V\'=V - V avg"] = v_dash
    outp["W\'=W - W avg"] = w_dash
    
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
    
    outp["Octant"] = octant_col 

    # entered empty column in sheet
    empty_col = []
    empty_col.extend(['']*(len(inp['U'])))
    outp[' '] = empty_col

    # created 2 dictionary
    dictn_len = {}            # dictionary for maximum subsequence length of octant values
    dictn_cnt = {}

    for i in range(1,5):
      dictn_len[i] = 0
      dictn_cnt[i] = 0
      dictn_len[0-i] = 0
      dictn_cnt[0-i] = 0


    for w in range(cnt):
      counts = 0

      for q in range(w, cnt):
        if octant_col[q] == octant_col[w]:
          counts += 1
          
          if q == (cnt - 1):
            w = q
        else:
          w = q-1
          break
        
      dictn_len[octant_col[w]] = max(counts, dictn_len[octant_col[w]])

    for i in range(1,5):

      # finding maximum subsequence length's count for +i octant value
      # maximum subsequence length = dictn_len[i]
      for w in range(cnt - dictn_len[i] + 1):
        flag = True

        for q in range(w, w + dictn_len[i]):
          if octant_col[q] != i:
            flag = False
        
        if flag == True:
          dictn_cnt[i] += 1

      
      # finding maximum subsequence length's count for -i octant value
      # maximum subsequence length = dictn_len[0-i]
      for w in range(cnt - dictn_len[0-i] + 1):
        flag = True

        for q in range(w, w + dictn_len[0-i]):
          if octant_col[q] != (0-i):
            flag = False
        
        if flag == True:
          dictn_cnt[0-i] += 1

    count_col = []
    for i in range(1,5):
      count_col.append(i)
      count_col.append(0-i)

    count_col.extend(['']*(len(inp['U']) - 8))
    outp['Octant'] = count_col


    longest_len = []
    for i in range(1,5):
      longest_len.append(dictn_len[i])
      longest_len.append(dictn_len[0-i])

    longest_len.extend(['']*(len(inp['U']) - 8))
    outp['Longest Subsequence Length'] = longest_len


    longest_count = []
    for i in range(1,5):
      longest_count.append(dictn_cnt[i])
      longest_count.append(dictn_cnt[0-i])

    longest_count.extend(['']*(len(inp['U']) - 8))
    outp['Count '] = longest_count

    outp.to_excel('output_octant_longest_subsequence.xlsx')




octant_longest_subsequence_count()

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
