from pathlib import Path

log_file = "/tmp/frida_log.log"


def read_file_content_as_string(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "None"


# save the log into the log file
def save_log(log):
    if log is None:
        return
    with open(log_file, 'a') as file:
        file.write("\n")
        file.write(str(log))
        file.flush()


# clear the log file
def clear_log():
    with open(log_file, 'w') as file:
        file.write("")
        file.flush()
        file.close()
