from src.utilities.select_message_for_sending import select_random_msg, read_file_line_by_line
import xlrd, time, random


sender = []
recipients = read_file_line_by_line("./assets/txt/recipients test.txt")
recipients1 = recipients
number_of_recipients = len(recipients)
senders_file = xlrd.open_workbook("./assets/xls/50-pcs-2020-16.6.xlsx") 
senders_list = senders_file.sheet_by_index(0)
number_of_senders = senders_list.nrows
print(recipients1)
print(number_of_recipients, number_of_senders)
number = 0
while True:
    if number_of_recipients == 0:
        print(number)
        break
    else:
        for i in range(0, number_of_senders):
            try:
                random_number = random.randrange(0, number_of_recipients)
                print(random_number)
                print(senders_list.cell_value(i, 0) + " sent to : " + recipients[random_number])
                recipients.remove(recipients[random_number])
                number_of_recipients = len(recipients)
                print(number_of_recipients)
            except:
                pass
            number += 1

