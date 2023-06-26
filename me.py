from src.utilities.select_message_for_sending import select_random_msg, read_file_line_by_line

re = read_file_line_by_line("./assets/txt/recipients test.txt")
x = "uchitosato@gmail.com\n"
if x.strip() + '\n' in re:
    print("ok")