from datetime import datetime, timedelta


def format_html_date(string):
    year = string[0:4]
    month = string[5:7]
    day = string[8:10]
    hours = string[11:13]
    minutes = string[14:16]
    date_string= day + '-' + month + '-' + year + ' ' + hours + ':' + minutes + ':' + '00'
    return datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S") - timedelta(hours=5, minutes=30)


def format_date_only(string):
    year = string[0:4]
    month = string[5:7]
    day = string[8:10]
    date_string= day + '-' + month + '-' + year
    return datetime.strptime(date_string, "%d-%m-%Y").date()
