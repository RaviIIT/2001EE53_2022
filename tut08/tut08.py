# team india and pakistan squads
team_india = []
team_pakistan = []

# opened teams file
team_file = open('teams.txt')
count = 0
while True:
    # Get next line from file
    line = team_file.readline()
    line = str(line)
    strng = ''
    if not line:
        break
    if count == 2:
        for w in range(len(line)):
            if line[w] == ':':
                strng = line[w+2:len(line)-1]
                break
        break
    count = count + 1

team_india = strng.split(', ')

# team india members
for w in range(len(team_india)):
    if team_india[w][len(team_india[w])-1] == ')':
        team_india[w] = team_india[w][:len(team_india[w])-3]

# openend India innings file
file1 = open('india_inns2.txt', 'r')


ind_batsman_runs = {}                                   #runs of indian batsman
ind_batsman_balls = {}                                  #balls taken by indian batsman
ind_batsman_four = {}                                   #fours scored by indian batsman 
ind_batsman_six = {}                                    #sixes scored by indian batsman
ind_bowler_runs = {}                                    #runs on indian bowlers ball
ind_bowler_balls = {}                                   #balls delivered by indian bowlers
ind_bowled = {}                                         #wickets and their infos that India took
ind_bowler_wide = {}                                    #wide balls by india, bowler wise info
ind_bowler_wickets = {}                                 #wickets count by indian bowlers
ind_runs = 0                                            #dynamic run count of India after each ball
ind_extras = 0                                          #extras india got
ind_last_ball = ''                                      #last ball of India
ind_wick_down = 0                                       #no. of wickets down of India
ind_fall_wick = ''                                      #fall of wickets info of India
ind_pplay = 0                                           #power play runs by India
ind_extra_dic = {'b': 0, 'lb':0, 'w':0, 'nb':0, 'p': 0} #extras mapping dictionary           
ind_not_bat = []                        

pak_batsman_runs = {}                                   #runs of pak batsman  
pak_batsman_balls = {}                                  #balls taken by pak batsman
pak_batsman_four = {}                                   #fours scored by pak batsman
pak_batsman_six = {}                                    #six scored by pak batsman
pak_bowler_runs = {}                                    #runs on pak bowlers ball
pak_bowler_balls = {}                                   #balls delivered by pak bowlers
pak_bowled = {}                                         #pakistani bowlers took wicket
pak_bowler_wide = {}                                    #wide balls by pak, bowler wise info
pak_bowler_wickets = {}                                 #wickets count by pak bowlers
pak_runs = 0                                            #dynamic run count of pak after each ball
pak_extras = 0                                          #extras pakistan got
pak_last_ball = ''                                      #last ball of pakistan
pak_wick_down = 0                                       #no. of wickets down of pak
pak_fall_wick = ''                                      #fall of wickets info
pak_pplay = 0                                           #power play runs pak
pak_extra_dic = {'b': 0, 'lb':0, 'w':0, 'nb':0, 'p': 0} #extras mapping dictionary

# Team India part
# ----------------------------------------------------------------------------------------------------------------------------------------
while True:
    # Get next line from file
    line = file1.readline()
  
    # if line is empty end of file is reached
    if not line:
        break
    s = line.strip()

    # if empty line, then proceed to next line
    if s == '':
        continue

    # last ball of india
    ind_last_ball = s.split(' ')[0]

    # status of match per ball - runs, outs, wide, leg byes, byes
    match_status = s.split(", ")[1].split(' ')[0]
    temp = s.split(' ')

    # current batsman and bowler
    cur_batsman = ''
    cur_bowler = ''

    # extracting current batsman and bowler
    for w in range(len(s)-1):
      
        if s[w] == 't' and s[w+1] == 'o':
            for q in range(len(s)):
                if s[q] == ' ':
                    cur_bowler = s[q+1:w-1]
                    break
            
            for q in range(len(s)):
                if s[q] == ',':
                    cur_batsman = s[w+3:q]
                    break
            break
    
    # power play runs scored by india
    if ind_last_ball == '6.1':
        ind_pplay = str(ind_runs)

    # if this batsman has not come before, initialisiing the dictionary elements for this batsman
    usls = 0
    if (cur_batsman in ind_batsman_runs.keys()):
        usls = 0
    else:
        ind_batsman_runs[cur_batsman] = 0
        ind_batsman_balls[cur_batsman] = 0
        ind_batsman_four[cur_batsman] = 0
        ind_batsman_six[cur_batsman] = 0
        pak_bowled[cur_batsman] = ['', '']
    # if this bowler has not come before, initialisiing the dictionary elements for this bowler
    if (cur_bowler in pak_bowler_runs.keys()):
        usls = 0
    else:
        pak_bowler_runs[cur_bowler] = 0
        pak_bowler_balls[cur_bowler] = 0
        pak_bowler_wide[cur_bowler] = 0
        pak_bowler_wickets[cur_bowler] = 0

    # checking for wide runs
    wide_runs = 0    
    wide_check = s.split(', ')[1].split('wide')

    if len(wide_check) > 1:
        match_status = 'wide'
        run_chk = wide_check[0].split(' ')
        if len(run_chk) == 1:
            wide_runs = 1
        else:
            wide_runs = ord(run_chk[0]) - 48

    # proceeding score wise and doing the valid operations after each ball
    if match_status == '1':
        ind_batsman_runs[cur_batsman] = ind_batsman_runs[cur_batsman] + 1
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + 1
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_runs = ind_runs + 1
    elif match_status == '2':
        ind_batsman_runs[cur_batsman] = ind_batsman_runs[cur_batsman] + 2
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + 2
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_runs = ind_runs + 2
    elif match_status == '3':
        ind_batsman_runs[cur_batsman] = ind_batsman_runs[cur_batsman] + 3
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + 3
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_runs = ind_runs + 3
    elif match_status == 'FOUR':
        ind_batsman_runs[cur_batsman] = ind_batsman_runs[cur_batsman] + 4
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + 4
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_batsman_four[cur_batsman] = ind_batsman_four[cur_batsman] + 1
        ind_runs = ind_runs + 4
    elif match_status == 'SIX':
        ind_batsman_runs[cur_batsman] = ind_batsman_runs[cur_batsman] + 6
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + 6
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_batsman_six[cur_batsman] = ind_batsman_six[cur_batsman] + 1
        ind_runs = ind_runs + 6
    elif match_status == 'out':
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        pak_bowler_wickets[cur_bowler] = pak_bowler_wickets[cur_bowler] + 1
        ind_wick_down = ind_wick_down + 1
        ind_fall_wick = ind_fall_wick + str(ind_runs) + '-' + str(ind_wick_down) + ' (' + cur_batsman + ', ' + ind_last_ball + '). '
        # checking if it's caught or bowled
        c_or_b = s.split(', out ')[1].split(' ')[0]                         #caught or bowled

        if c_or_b == 'Caught':
            caught_by = s.split('by ')[1].split('!!')[0]
            pak_bowled[cur_batsman] = [cur_bowler, caught_by]
        else:
            pak_bowled[cur_batsman] = [cur_bowler, '']
    elif match_status == 'no':
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1
    elif match_status == 'byes' or match_status == 'leg':
        pak_bowler_balls[cur_bowler] = pak_bowler_balls[cur_bowler] + 1
        ind_batsman_balls[cur_batsman] = ind_batsman_balls[cur_batsman] + 1

        # byes and leg byes runs
        temp_runs = s.split('byes, ')[1].split(' ')[0]
        if len(temp_runs) > 1:      #definitely FOUR
            ind_runs = ind_runs + 4
            ind_extras = ind_extras + 4
            if match_status == 'byes':
                ind_extra_dic['b'] = ind_extra_dic['b'] + 4
            else:
                ind_extra_dic['lb'] = ind_extra_dic['lb'] + 4
        else:
            ind_runs = ind_runs + ord(temp_runs) - 48
            ind_extras = ind_extras + ord(temp_runs) - 48
            if match_status == 'byes':
                ind_extra_dic['b'] = ind_extra_dic['b'] + ord(temp_runs) - 48
            else:
                ind_extra_dic['lb'] = ind_extra_dic['lb'] + ord(temp_runs) - 48
    elif match_status == 'wide':
        ind_runs = ind_runs + wide_runs
        ind_extras = ind_extras + wide_runs
        ind_extra_dic['w'] = ind_extra_dic['w'] + wide_runs
        pak_bowler_wide[cur_bowler] = pak_bowler_wide[cur_bowler] + wide_runs
        pak_bowler_runs[cur_bowler] = pak_bowler_runs[cur_bowler] + wide_runs


file1.close()

for w in team_india:
    names = w.split(' ')
    
    flag = bool(0)
    for name in names:
        if name in ind_batsman_runs.keys():
            flag = bool(1)
    
    if flag == 0:
        ind_not_bat.append(w)

ind_not_bat.remove('Hardik Pandya')
ind_not_bat.remove('Suryakumar Yadav')
# ------------------------------------------------------------------------------------------------------------------------------------


# Team Pakistan Innings
# -------------------------------------------------------------------------------------------------------------------------------------
file1 = open('pak_inns1.txt', 'r')
while True:
    # Get next line from file
    line = file1.readline()
  
    # if line is empty end of file is reached
    if not line:
        break
    s = line.strip()

    # moving to next line if current line is empty
    if s == '':
        continue
    # last ball delivered to pak
    pak_last_ball = s.split(' ')[0]

    # status of match per ball - runs, outs, wide, leg byes, byes
    match_status = s.split(", ")[1].split(' ')[0]
    temp = s.split(' ')

    # current batsman and bowlers
    cur_batsman = ''
    cur_bowler = ''

    # runs scored by pak in power play
    if pak_last_ball == '6.1':
        pak_pplay = str(pak_runs)

    for w in range(len(s)-1):
      
        if s[w] == 't' and s[w+1] == 'o':
            for q in range(len(s)):
                if s[q] == ' ':
                    cur_bowler = s[q+1:w-1]
                    break
            
            for q in range(len(s)):
                if s[q] == ',':
                    cur_batsman = s[w+3:q]
                    break
            break

    # if this batsman has not come before, initialising all the dictionary elements for the batsman
    usls = 0
    if (cur_batsman in pak_batsman_runs.keys()):
        usls = 0
    else:
        pak_batsman_runs[cur_batsman] = 0
        pak_batsman_balls[cur_batsman] = 0
        pak_batsman_four[cur_batsman] = 0
        pak_batsman_six[cur_batsman] = 0
        ind_bowled[cur_batsman] = ['', '']
    # if this bowler has not come before, initialising all the dictionary elements for the bowler
    if (cur_bowler in ind_bowler_runs.keys()):
        usls = 0
    else:
        ind_bowler_runs[cur_bowler] = 0
        ind_bowler_balls[cur_bowler] = 0
        ind_bowler_wide[cur_bowler] = 0
        ind_bowler_wickets[cur_bowler] = 0

    # if wide ball
    wide_runs = 0    
    wide_check = s.split(', ')[1].split('wide')

    if len(wide_check) > 1:
        match_status = 'wide'
        run_chk = wide_check[0].split(' ')
        if len(run_chk) == 1:
            wide_runs = 1
        else:
            wide_runs = ord(run_chk[0]) - 48

    # proceeding according to the result of each ball, and doing the desired operations on runs, balls, wickets etc.
    if match_status == '1':
        pak_batsman_runs[cur_batsman] = pak_batsman_runs[cur_batsman] + 1
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + 1
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_runs = pak_runs + 1
    elif match_status == '2':
        pak_batsman_runs[cur_batsman] = pak_batsman_runs[cur_batsman] + 2
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + 2
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_runs = pak_runs + 2
    elif match_status == '3':
        pak_batsman_runs[cur_batsman] = pak_batsman_runs[cur_batsman] + 3
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + 3
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_runs = pak_runs + 3
    elif match_status == 'FOUR':
        pak_batsman_runs[cur_batsman] = pak_batsman_runs[cur_batsman] + 4
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + 4
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_batsman_four[cur_batsman] = pak_batsman_four[cur_batsman] + 1
        pak_runs = pak_runs + 4
    elif match_status == 'SIX':
        pak_batsman_runs[cur_batsman] = pak_batsman_runs[cur_batsman] + 6
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + 6
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_batsman_six[cur_batsman] = pak_batsman_six[cur_batsman] + 1
        pak_runs = pak_runs + 6
    elif match_status == 'out':
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        pak_wick_down = pak_wick_down + 1
        pak_fall_wick = pak_fall_wick + str(pak_runs) + '-' + str(pak_wick_down) + ' (' + cur_batsman + ', ' + pak_last_ball + '). '
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        ind_bowler_wickets[cur_bowler] = ind_bowler_wickets[cur_bowler] + 1
        c_or_b = s.split(', out ')[1].split(' ')[0]                         #caught or bowled

        # if caught or bowled
        if c_or_b == 'Caught':
            caught_by = s.split('by ')[1].split('!!')[0]
            ind_bowled[cur_batsman] = [cur_bowler, caught_by]
        else:
            ind_bowled[cur_batsman] = [cur_bowler, '']
    elif match_status == 'no':
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
    elif match_status == 'byes' or match_status == 'leg':
        ind_bowler_balls[cur_bowler] = ind_bowler_balls[cur_bowler] + 1
        pak_batsman_balls[cur_batsman] = pak_batsman_balls[cur_batsman] + 1
        
        # if byes or leg byes, and their runs
        temp_runs = s.split('byes, ')[1].split(' ')[0]
        if len(temp_runs) > 1:      #definitely FOUR
            pak_runs = pak_runs + 4
            pak_extras = pak_extras + 4
            if match_status == 'byes':
                pak_extra_dic['b'] = pak_extra_dic['b'] + 4
            else:
                pak_extra_dic['lb'] = pak_extra_dic['lb'] + 4
        else:
            pak_runs = pak_runs + ord(temp_runs) - 48
            pak_extras = pak_extras + ord(temp_runs) - 48
            if match_status == 'byes':
                pak_extra_dic['b'] = pak_extra_dic['b'] + ord(temp_runs) - 48
            else:
                pak_extra_dic['lb'] = pak_extra_dic['lb'] + ord(temp_runs) - 48
    elif match_status == 'wide':
        pak_runs = pak_runs + wide_runs
        pak_extras = pak_extras + wide_runs
        pak_extra_dic['w'] = pak_extra_dic['w'] + wide_runs
        ind_bowler_runs[cur_bowler] = ind_bowler_runs[cur_bowler] + wide_runs
        ind_bowler_wide[cur_bowler] = ind_bowler_wide[cur_bowler] + wide_runs

file1.close()

# creating scorecard of both innings
card = open("Scorecard.txt","w")
lines_append = []

# Pakistan innings scorecard
# -------------------------------------------------------------------------------------------------------------------------------
lines_append.append(f"{'Pakistan Innings' : <60}{str(pak_runs) + '-' + str(len(ind_bowled)) + ' (' + pak_last_ball + ' Ov)' : >60}")
lines_append.append(f"{'Batter' : <30}{' ' : <40}{'R' : >10}{'B' : >10}{'4s' : >10}{'6s' : >10}{'SR' : >10}")

# appending batsman details
for w in pak_batsman_runs:
    batsman = w
    if ind_bowled[w][0] == '':
        out_status = 'not out'
    else:  
        out_status = 'b ' + ind_bowled[w][0]
        if ind_bowled[w][1] != '':
            out_status = 'c ' + ind_bowled[w][1] + ' ' + out_status 
        
        R = pak_batsman_runs[w]
        B = pak_batsman_balls[w]
        fours = pak_batsman_four[w]
        sixes = pak_batsman_six[w]
        SR = round((R*100)/B, 2)

    lines_append.append(f"{batsman : <30}{out_status : <40}{R: >10}{B : >10}{fours : >10}{sixes : >10}{SR : >10}")

# appending extras and total
extra_runs = str(pak_extras) + ' ('
for w in pak_extra_dic:
    extra_runs = extra_runs + w + ' ' + str(pak_extra_dic[w])  + '.'

total_runs = str(pak_runs) + ' (' + str(pak_wick_down) + ' wkts, ' + pak_last_ball + ' Ov)'

lines_append.append(f"{'Extras' : <70}{extra_runs : >50}")
lines_append.append(f"{'Total' : <70}{total_runs : >50}")

lines_append.append('\n')

lines_append.append(f"{'Fall of Wickets' : <70}")
lines_append.append(f"{pak_fall_wick}")
lines_append.append('\n')

lines_append.append(f"{'Bowler' : <50}{'O' : >10}{'M' : >10}{'R' : >10}{'W' : >10}{'NB' : >10}{'WD' : >10}{'ECO': >10}")
# appending bowler details
for w in ind_bowler_balls:
    bowler = w
    O = str(int(ind_bowler_balls[w]/6))
    if ind_bowler_balls[w] % 6 != 0:
        O = O + '.' + str(ind_bowler_balls[w] % 6)
    R = str(ind_bowler_runs[w])
    W = str(ind_bowler_wickets[w])
    WD = str(ind_bowler_wide[w])
    ECO = str(round((ind_bowler_runs[w]*6)/ind_bowler_balls[w], 2))

    lines_append.append(f"{bowler : <50}{O : >10}{'0' : >10}{R : >10}{W : >10}{'0' : >10}{WD : >10}{ECO: >10}")

lines_append.append('\n')
# appending power play details
lines_append.append(f"{'Powerplays' : <60}{'Overs' : <30}{'Runs' : >30}")
lines_append.append(f"{'Mandatory' : <60}{'0.1-6' : <30}{pak_pplay : >30}")
lines_append.append('\n')
# --------------------------------------------------------------------------------------------------------------------------------------

# India scorecard
lines_append.append(f"{'India Innings' : <60}{str(ind_runs) + '-' + str(len(pak_bowled)) + ' (' + ind_last_ball + ' Ov)' : >60}")
lines_append.append(f"{'Batter' : <30}{' ' : <40}{'R' : >10}{'B' : >10}{'4s' : >10}{'6s' : >10}{'SR' : >10}")

# appending batsman details
for w in ind_batsman_runs:
    batsman = w
    if pak_bowled[w][0] == '':
        out_status = 'not out'
    else:  
        out_status = 'b ' + pak_bowled[w][0]
        if pak_bowled[w][1] != '':
            out_status = 'c ' + pak_bowled[w][1] + ' ' + out_status
        R = ind_batsman_runs[w]
        B = ind_batsman_balls[w]
        fours = ind_batsman_four[w]
        sixes = ind_batsman_six[w]
        SR = round((R*100)/B, 2)

    lines_append.append(f"{batsman : <30}{out_status : <40}{R: >10}{B : >10}{fours : >10}{sixes : >10}{SR : >10}")

# appending extra runs and total runs
extra_runs = str(ind_extras) + ' ('
for w in ind_extra_dic:
    extra_runs = extra_runs + w + ' ' + str(ind_extra_dic[w]) + '.' 

total_runs = str(ind_runs) + ' (' + str(ind_wick_down) + ' wkts, ' + ind_last_ball + ' Ov)'

lines_append.append(f"{'Extras' : <70}{extra_runs : >50}")
lines_append.append(f"{'Total' : <70}{total_runs : >50}")

no_batting = ''
for i in ind_not_bat:
    no_batting = no_batting + i + ','

no_batting = no_batting[:len(no_batting) - 1]

lines_append.append(f"{'Did not Bat' : <30}{no_batting : >90}")
lines_append.append('\n')

# appending Fall of Wickets
lines_append.append(f"{'Fall of Wickets' : <70}")
lines_append.append(f"{ind_fall_wick}")
lines_append.append('\n')

lines_append.append(f"{'Bowler' : <50}{'O' : >10}{'M' : >10}{'R' : >10}{'W' : >10}{'NB' : >10}{'WD' : >10}{'ECO': >10}")
# appending bowler details
for w in pak_bowler_balls:
    bowler = w
    O = str(int(pak_bowler_balls[w]/6))
    if pak_bowler_balls[w] % 6 != 0:
        O = O + '.' + str(pak_bowler_balls[w] % 6)
    R = str(pak_bowler_runs[w])
    W = str(pak_bowler_wickets[w])
    WD = str(pak_bowler_wide[w])
    ECO = str(round((pak_bowler_runs[w]*6)/pak_bowler_balls[w], 2))

    lines_append.append(f"{bowler : <50}{O : >10}{'0' : >10}{R : >10}{W : >10}{'0' : >10}{WD : >10}{ECO: >10}")

# appending power play details
lines_append.append('\n')
lines_append.append(f"{'Powerplays' : <60}{'Overs' : <30}{'Runs' : >30}")
lines_append.append(f"{'Mandatory' : <60}{'0.1-6' : <30}{ind_pplay : >30}")

# writing all the lines to scorecard
for lines in lines_append:
    card.write(lines + '\n')

# closing scorecard file
card.close()
