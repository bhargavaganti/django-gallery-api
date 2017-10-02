from datetime import datetime

log_file_path = "logs/all_logs.log"

# def log(msg):
#     file = open(log_file_path, "a")
#     msg = "\n[" + str(datetime.now()) + "]: " + msg
#     file.write(msg)
#     file.close()

def log(msg):
    output = f"\n\n[{datetime.now()}: {str(msg)}\n\n"
    print(output)