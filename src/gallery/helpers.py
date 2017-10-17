from datetime import datetime

log_file_path = "logs/all_logs.log"

# def log(msg):
#     file = open(log_file_path, "a")
#     msg = "\n[" + str(datetime.now()) + "]: " + msg
#     file.write(msg)
#     file.close()

#
def log(msg):
    """
    функција за форматирани испис порука у конзоли
    :param msg:
    :return:
    """
    output = f"\n\n[{datetime.now()}: {str(msg)}\n\n"
    print(output)


def prepare_path(raw):
    """
    Функција за замену недозвољених карактера за име фолдера
    :param raw:
    :return: str
    """
    path = str(raw).replace("'","").replace(" ", "_").replace("-", "_")
    return path