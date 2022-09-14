import pandas as pd
import math

def octact_identification(mod=5000):
    
    ## stored csv file in a variable and took indexing on 0th column
    inp = pd.read_csv('octant_input.csv', index_col = 0)
    
    ## stored average of each column in input
    u_avg = inp['U'].mean()
    v_avg = inp['V'].mean()
    w_avg = inp['W'].mean()
    
    ## wrote output to output file in column wise manner
    inp.to_csv('octant_output.csv')
    
    # entered average values in a list
    u_avg_col = [u_avg]
    v_avg_col = [v_avg]
    w_avg_col = [w_avg]
    
    # filled remaininig cells of average column
    u_avg_col.extend(['']*(len(inp['U'])-1))
    v_avg_col.extend(['']*(len(inp['V'])-1))
    w_avg_col.extend(['']*(len(inp['W'])-1))
    
    # read the output.csv file
    outp = pd.read_csv('octant_output.csv', index_col = 0)
    
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
    user_input.extend(['']*(len(inp['U'])-2))
    
    outp[''] = user_input
    
    # formed "Octant ID" column
    octant_id = ["Overall Count", 'Mod ' + str(mod)]

    for i in range(itr):
        num1 = mod*i
        num2 = (mod*(i+1)) - 1
        if num2 > cnt:
            num2 = cnt
            
        str_range = str(num1) + '-' + str(num2)
        octant_id.append(str_range)
    
    octant_id.extend(['']*(len(inp['U'])-2-itr))
    
    # entered "Octant ID" column
    outp['Octant ID'] = octant_id

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
            
            for q in range(cnt):
                if octant_col[q] == i and num1 <= q and q <= num2:
                    sums += 1
            
            col_one.append(sums)
            
        col_one.extend(['']*(len(inp['U'])-2-itr))            
        
        # filled +i octant column in outp variable
        outp[i] = col_one
        
        # reinitialised col_one for -i octant frequency
        col_one = [single_freq[0-i], '']

        # iterating for each range        
        for w in range(itr):
            sums = 0
            num1 = w*mod
            num2 = (mod*(w+1)) - 1
            if num2 > cnt:
                num2 = cnt
            
            for q in range(cnt):
                if octant_col[q] == (0-i) and num1 <= q and q <= num2:
                    sums +=1
            
            col_one.append(sums)
        col_one.extend(['']*(len(inp['U'])-2-itr))            

        # filled -i octant column in outp variable
        outp[0-i] = col_one 
    
    # wrote everything present in outp variable to "octant_output.csv" file
    outp.to_csv('octant_output.csv')
    
    
mod=5000
octact_identification(mod)
