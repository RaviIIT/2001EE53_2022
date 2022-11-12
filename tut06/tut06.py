import pandas as pd
import re
import datetime
import math
import os
import datetime
from datetime import timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

start_time = datetime.datetime.now()

def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body, file_path):
    # try block for error handling
    try:
        msg = MIMEMultipart()
        print("[+] Message Object Created")
    except:
        print("[-] Error in Creating Message Object")
        return

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = msg_subject

    body = msg_body
    msg.attach(MIMEText(body, 'plain'))

    filename = file_path
    attachment = open(filename, "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # try block for error handling
    try:
        msg.attach(p)
        print("[+] File Attached")
    except:
        print("[-] Error in Attaching file")
        return

    # try block for error handling
    try:
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        s = smtplib.SMTP('stud.iitp.ac.in', 587)
        print("[+] SMTP Session Created")
    except:
        print("[-] Error in creating SMTP session")
        return

    s.starttls()

    # try block for error handling
    try:
        s.login(fromaddr, frompasswd)
        print("[+] Login Successful")
    except:
        print("[-] Login Failed")

    text = msg.as_string()

    # try block for error handling
    try:
        s.sendmail(fromaddr, toaddr, text)
        print("[+] Mail Sent successfully")
    except:
        print('[-] Mail not sent')

    s.quit()


def isEmail(x):
    if ('@' in x) and ('.' in x):
        return True
    else:
        return False



def attendance_report():

    # try block for error handling
    try:
        inp = pd.read_csv('/content/sample_data/input_registered_students.csv')
        inp.rename(columns = {'Roll No':'Roll'}, inplace = True)

        inp_att = pd.read_csv('/content/sample_data/input_attendance.csv')

        # try block for error handling
        try:
            # creating directory if not present
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'output')
            if not os.path.exists(final_directory):
              os.makedirs(final_directory)
        except:
            print('Error occured while making output folder.')

        # lists to be used for pushing columns into excel file at the end
        dates_list = []
        times_list = []
        is_valid_time = []
        class_dates = []
        attend_list = []
        actual_lec = []
        att_per = []

        first_class = datetime.date.today()
        last_class = datetime.date.today()
        attend_list.extend([0]*(len(inp['Roll'])))

        # checking first and last date of classes dynamically
        # ----------------------------------------------------------first and last dates---------------------------------------------------------------
        for i in inp_att['Timestamp']:
          datetime_obj = datetime.datetime.strptime(str(i), "%d-%m-%Y %H:%M")
          myDate = datetime.datetime.strptime(str(datetime_obj.date()), "%Y-%m-%d")
          if myDate.weekday() == 0 or myDate.weekday() == 3:
            first_class = datetime_obj.date()
            break

        for i in inp_att['Timestamp']:
          datetime_obj = datetime.datetime.strptime(str(i), "%d-%m-%Y %H:%M")
          myDate = datetime.datetime.strptime(str(datetime_obj.date()), "%Y-%m-%d")
          if myDate.weekday() == 0 or myDate.weekday() == 3:
            last_class = datetime_obj.date()

        first_year, first_month, first_date = str(first_class).split('-')
        last_year, last_month, last_date = str(last_class).split('-')

        # writing dates into datetime object format
        start_date = datetime.date(int(first_year), int(first_month), int(first_date))
        end_date = datetime.date(int(last_year), int(last_month), int(last_date))
        delta = datetime.timedelta(days=1)

        # pushing all class days into a list for future use
        while start_date <= end_date:
          myDate = datetime.datetime.strptime(str(start_date), "%Y-%m-%d")
          if myDate.weekday() == 0 or myDate.weekday() == 3:
            class_dates.append(start_date)
          start_date += delta

        # ---------------------------------------------------------------------------------------------------------------
        # is_valid_time will store 1 if this time is valid (2-3 PM) irrespective of day else 0
        for i in inp_att['Timestamp']:
          datetime_obj = datetime.datetime.strptime(str(i), "%d-%m-%Y %H:%M")
          dates_list.append(datetime_obj.date())

          start_time = datetime.time(int(14), int(0), int(0))
          end_time = datetime.time(int(15), int(0), int(0))

          if start_time <= datetime_obj.time() and datetime_obj.time() <= end_time:
            is_valid_time.append(1)
          else:
            is_valid_time.append(0)

        # ------------------------------------------------------------------------------------------------------------------
        # for each date (for making consolidated report)
        for i in class_dates:
          # for each roll
          # absent present array (A/P)
          abs_prs = []

          cur_cnt = 0
          for w in inp['Roll']:
            cur_roll = w
            
            flag = 0
            for t in range(len(inp_att['Attendance'])):
              temp = re.split("\s", str(inp_att['Attendance'][t]))
              # taking roll from name and roll concatenated string
              new_roll = temp[0]

              # valid attendance
              if str(cur_roll) == str(new_roll) and str(i) == str(dates_list[t]) and is_valid_time[t] == 1:
                flag = 1
                break

            # marking present if valid attendance
            if flag == 1:
              abs_prs.append('P')
              attend_list[cur_cnt] = attend_list[cur_cnt] + 1
            else:
              abs_prs.append('A')
            
            cur_cnt = cur_cnt + 1
          
          try:
              inp[str(i)] = abs_prs
          except:
              print('Error while entering column in consolidated report.')

        actual_lec.extend([int(len(class_dates))]*(len(inp['Roll'])))

        for i in range(len(inp['Roll'])):
          att_per.append(round((attend_list[i]*100)/actual_lec[i], 2))

        cur_cnt = 0

        # for individual roll files
        # iterating for each roll number
        for i in inp['Roll']:
          # lists to be pushed in form of columns in individual roll files.
          indv_date = []
          indv_roll = []
          indv_name = []
          indv_tot_cnt = []
          indv_real = []
          indv_dup = []
          indv_invalid = []
          indv_abs = []

          indv_date.append('')
          indv_roll.append(i)
          indv_tot_cnt.append('')
          indv_real.append('')
          indv_dup.append('')
          indv_invalid.append('')
          indv_abs.append('')
          indv_name.append(inp['Name'][cur_cnt])
          indv_roll.extend(['']*(len(class_dates) + 1 - len(indv_roll)))
          indv_name.extend(['']*(len(class_dates) + 1 - len(indv_name)))
          indv_tot_cnt.extend([0]*(len(class_dates) + 1 - len(indv_tot_cnt)))
          indv_real.extend([0]*(len(class_dates) + 1 - len(indv_real)))
          indv_dup.extend([0]*(len(class_dates) + 1 - len(indv_dup)))
          indv_invalid.extend([0]*(len(class_dates) + 1 - len(indv_invalid)))
          indv_abs.extend([0]*(len(class_dates) + 1 - len(indv_abs)))

          for w in range(len(class_dates)):
            indv_date.append(class_dates[w])

            for t in range(len(inp_att['Attendance'])):
              cur_roll = re.split("\s", str(inp_att['Attendance'][t]))[0]

              # total attendance count
              if str(i) == str(cur_roll) and str(class_dates[w]) == str(dates_list[t]):
                indv_tot_cnt[w+1] = indv_tot_cnt[w+1] + 1

              # invalid attendance count
              if str(i) == str(cur_roll) and str(class_dates[w]) == str(dates_list[t]) and is_valid_time[t] == 0:
                indv_invalid[w+1] = indv_invalid[w+1] + 1

              # real attendance count
              if str(i) == str(cur_roll) and str(class_dates[w]) == str(dates_list[t]) and is_valid_time[t] == 1:
                indv_real[w+1] = 1

          # absent condition
          for w in range(1, len(class_dates)+1):
            indv_dup[w] = indv_tot_cnt[w] - indv_real[w] - indv_invalid[w]
            if indv_real[w] == 0:
              indv_abs[w] = 1
          
          df = pd.DataFrame()
          
          # try block for error handling
          try:
              df['Date'] = indv_date
              df['Roll'] = indv_roll
              df['Name'] = indv_name
              df['Total Attendance Count'] = indv_tot_cnt
              df['Real'] = indv_real
              df['Duplicate'] = indv_dup
              df['Invalid'] = indv_invalid
              df['Absent'] = indv_abs
          except:
              print('Error while entering columns in roll files.')

          # try block for error handling
          try:
              df.to_excel(r'output/'+ str(i) + '.xlsx', index=False)
          except:
              print('Error occured while writing to individual roll number files.')
          cur_cnt = cur_cnt + 1   

        # try block for error handling
        try:
            inp['Actual Lecture Taken'] = actual_lec
            inp['Total Real'] = attend_list
            inp['% Attendance'] = att_per
        except:
            print('Error while entering columns in consolidated files.')

        # try block for error handling
        try:
            inp.to_excel(r'output/attendance_report_consolidated.xlsx', index=False) 
        except:
            print('Error occured while writing to attendance_report_consolidated')
        
        # email sending query
        ans = input('Do you want to send attendance_report_consolidated over mail (YES/NO)? ')

        # if YES then for sending email
        if(ans == 'YES'):
            # credentials and contents of mail
            FROM_ADDR = input('Enter Sender\'s webmail id : ')
            FROM_PASSWD = input('Enter Sender\'s webmail Password : ')
            Subject = "attendance_report_consolidated by Ravi Kumar 2001EE53"

            Body ='''
            Dear Student,

            Please find your attached attendance_report_consolidated as per CS384 Tut6 assignment.
            Thanking You.

            --
            Ravi Kumar
            Roll - 2001EE53
            IIT Patna
            '''

            to_mail = input('Enter Receiver\'s mail id : ')
            # calling send_mail function to send mail.
            send_mail(FROM_ADDR, FROM_PASSWD, to_mail, Subject, Body, 'output/attendance_report_consolidated.xlsx')
    except:
          print('Error while reading csv files.')


attendance_report()
end_time = datetime.datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))

  
