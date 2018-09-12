import datetime
from datetime import datetime

import pandas as pd
from Utils.GlobalVariables import *
from Utils.FileUtils import FileUtils


def is_date_actual(date_to_check, last_date_file="", last_date="", date_time_format="%d.%m.%Y um %H:%M",
                   default_text=GlobalVariables.get_date_time_file_header() + "\n01.01.2000 um 00:00"):
    """

    :param date_to_check:
    :param last_date_file:
    :type last_date: object
    :param date_time_format:
    :param default_text:
    :return:
    """

    if date_to_check is None:
        raise NotImplementedError

    if last_date == "":
        # no need to check, creates anyway
        if FileUtils.check_file_exists_or_create(last_date_file,
                                                 default_text):
            data = pd.read_csv(last_date_file)
            last_date_str = str(data[GlobalVariables.get_date_time_file_header()][0])
            last_date = datetime.strptime(last_date_str, date_time_format)
        else:
            return False, ""

    is_news_current = last_date < date_to_check

    if is_news_current:
        with open(last_date_file, "w") as myfile:
            myfile.write(GlobalVariables.get_date_time_file_header() + "\n")
            datetime_object_str = datetime.strftime(date_to_check, date_time_format)
            myfile.write(str(datetime_object_str) + "\n")
            return is_news_current, date_to_check

    return is_news_current, last_date
