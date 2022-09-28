import pandas as pd
import math

def octact_identification(mod=5000):
    
    # stored excel file in a variable and took indexing on 0th column

    # error handling if file unable to open
    try:
      inp = pd.read_excel('input_octant_transition_identify.xlsx', index_col = 0)
      
      ## stored average of each column in input
      u_avg = inp['U'].mean()
      v_avg = inp['V'].mean()
      w_avg = inp['W'].mean()
      
      # error handling if file unable to write
      try:
        # wrote output to output file in column wise manner
        inp.to_excel('output_octant_transition_identify.xlsx')
      except:                                                   #code if exception occurs
        print('Error encountered : while writing excel file')
      
      # entered average values in a list
      u_avg_col = [u_avg]
      v_avg_col = [v_avg]
      w_avg_col = [w_avg]
      
      # filled remaininig cells of average column
      u_avg_col.extend(['']*(len(inp['U'])-1))
      v_avg_col.extend(['']*(len(inp['V'])-1))
      w_avg_col.extend(['']*(len(inp['W'])-1))
      
      # read the output file
      outp = pd.read_excel('/content/output_octant_transition_identify.xlsx', index_col = 0)
      
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
          
      itr = math.ceil(cnt/mod)
      
      single_freq = {}
      
      # computed frequency of each octant in whole range
      for i in range(1,5):
          single_freq[i] = 0
          single_freq[0-i] = 0

      # finding octant values of each row
      for i in range(cnt):
          cur = i/mod
          cur = cur*mod
          
          if x[i] > 0 and y[i] > 0:   #1st quadrant
              if z[i] > 0:
                  octant_col.append(1)
                  single_freq[1] +=1
              else:
                  octant_col.append(-1)
                  single_freq[-1] +=1
          elif x[i] < 0 and y[i] > 0:   #2nd quadrant
              if z[i] > 0:
                  octant_col.append(2)
                  single_freq[2] +=1
              else:
                  octant_col.append(-2)
                  single_freq[-2] +=1
          elif x[i] < 0 and y[i] < 0:   #3rd quadrant
              if z[i] > 0:
                  octant_col.append(3)
                  single_freq[3] +=1
              else:
                  octant_col.append(-3)
                  single_freq[-3] +=1
          elif x[i] > 0 and y[i] < 0:   #4th quadrant
              if z[i] > 0:
                  octant_col.append(4)
                  single_freq[4] +=1
              else:
                  octant_col.append(-4)
                  single_freq[-4] +=1

      outp["Octant"] = octant_col 
      
      # entered new column
      user_input = ['',"User Input"]
      user_input.extend(['']*(itr + 6))
      user_input.append('From')
      user_input.extend(['']*8)

      for i in range(itr):
        user_input.extend(['']*5)
        user_input.append('From')
        user_input.extend(['']*7)

      user_input.extend(['']*(len(inp['U'])-(17 + (14*itr))))        #total length filled till now is 14*itr + 17 (found by calculation)
      
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

      # appended remaining cells in the column and entered Overall Transition Count details column wise
      octant_id.append('Verified')    
      octant_id.append('')
      octant_id.append('')
      octant_id.append('Overall Transition Count')
      octant_id.append('')
      octant_id.append('Count')

      # appended +ve and -ve octant values
      for i in range(1,5):
        octant_id.append(i);
        octant_id.append(0 - i);
      
      octant_id.append('')

      # entered Mod Transition Count detailed cells
      for i in range(itr):
          octant_id.extend(['']*2)
          octant_id.append('Mod Transition Count')
          num1 = mod*i
          num2 = (mod*(i+1)) - 1
          if num2 > cnt:
              num2 = cnt - 1
              
          str_range = str(num1) + '-' + str(num2)
          octant_id.append(str_range)

          octant_id.append('Count')
          for w in range(1,5):
              octant_id.append(w);
              octant_id.append(0 - w);
            

      octant_id.extend(['']*(len(inp['U'])-(17 + (14*itr))))        #total length filled till now is 14*itr + 17 (found by calculation)

      # error handling if column length is mismatched     
      try:
        # entered "Octant ID" column
        outp[''] = octant_id
      except:
        print('Error encountered : Mismatch in length of columns in Octant ID column')

      # iterating for each octant value for range frequency
      for i in range(1,5):
          
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

          # appending details to column +i
          col_one.append(single_freq[i])
          col_one.extend(['']*3)

          if i == 1:
            col_one.append('To')
          else:
            col_one.append('')
          col_one.append(i)

          # created dictionary to store count of octant values in total range
          dictn = {}
          for w in range(1,5):
            dictn[w] = 0
            dictn[0-w] = 0
          
          # incrementing dictionary values when corresponding octant value is found
          for q in range(1, cnt):
            if octant_col[q] == i:
              dictn[octant_col[q - 1]] += 1

          # appending data to dictionary for different octant values transition
          for w in range(1,5):
            col_one.append(dictn[w])
            col_one.append(dictn[0-w])
          
          col_one.append('')

          # iterating over individual ranges 
          for w in range(itr):
            col_one.extend(['']*3)

            if i == 1:
              col_one.append('To')
            else:
              col_one.append('')
            col_one.append(i)

            num1 = w*mod
            num2 = (mod*(w+1)) - 1
            if num2 > cnt-1:
              num2 = cnt-2

            # created dictionary for individual ranges whose transition is to +i octant value
            indv_dictn = {}
            for q in range(1,5):
              indv_dictn[q] = 0
              indv_dictn[0-q] = 0

            # filled indv_dictn dictionary
            for q in range(num1, num2+1):
              if octant_col[q+1] == i:
                indv_dictn[octant_col[q]] += 1

            # appending the values of transition of particular octant value
            for q in range(1, 5):
              col_one.append(indv_dictn[q])
              col_one.append(indv_dictn[0-q])
          
          # filled the remaining cells of the column
          col_one.extend(['']*(len(inp['U'])-(17 + (14*itr))))        #total length filled till now is 14*itr + 17 (found by calculation)

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
          
          # appending details to column -i
          col_one.append(single_freq[0-i])
          col_one.extend(['']*3)
          col_one.append('')
          col_one.append(0-i)

          # created dictionary to store count of octant values in total range
          dictn = {}
          for w in range(1,5):
            dictn[w] = 0
            dictn[0-w] = 0
          
          # incrementing dictionary values when corresponding octant value is found
          for q in range(1, cnt):
            if octant_col[q] == (0-i):
              dictn[octant_col[q - 1]] += 1

          # appending data to dictionary for different octant values transition
          for w in range(1,5):
            col_one.append(dictn[w])
            col_one.append(dictn[0-w])

          col_one.append('')

          # iterating over individual ranges for -ve i octant value
          for w in range(itr):
            col_one.extend(['']*3)
            col_one.append('')
            col_one.append(0-i)

            num1 = w*mod
            num2 = (mod*(w+1)) - 1
            if num2 > cnt-1:
              num2 = cnt-2

            # reinitialised dictionary for individual ranges whose transition is to -i octant value
            indv_dictn = {}
            for q in range(1,5):
              indv_dictn[q] = 0
              indv_dictn[0-q] = 0

            # filled indv_dictn dictionary
            for q in range(num1, num2+1):
              if octant_col[q+1] == (0-i):
                indv_dictn[octant_col[q]] += 1

            # appending the values of transition of particular octant value
            for q in range(1, 5):
              col_one.append(indv_dictn[q])
              col_one.append(indv_dictn[0-q])

          # filled the remaining cells of the column
          col_one.extend(['']*(len(inp['U'])-(17 + (14*itr))))        #total length filled till now is 14*itr + 17 (found by calculation)
          
          # filled -i octant column in outp variable
          outp[0-i] = col_one        

      # error handling if unable to write to output file.
      try:
        # wrote everything present in outp variable to 'output_octant_transition_identify.xlsx' file
        outp.to_excel('output_octant_transition_identify.xlsx')
      except:
        print('Error encountered : While writing excel file.')
    except:
      print("Error encountered")
    
    
mod=5000
octact_identification(mod)
