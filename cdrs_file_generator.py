#!/usr/bin/env python

import traceback
import gzip
import os
import random
import datetime
import shutil
from cdr import FakeCallDetailRecord, header

# pip install elasticsearch-loader
ELLASTIC_COMMAND = '~/.local/bin/elasticsearch_loader --index cdrs --id-field RECORD_ID csv'


def remove_file(filename):
    if not filename:
        raise ValueError('No file to load. Please provide the first positional parameter')

    try:
        os.remove(filename)
    except Exception as err:
        print(f'Something was wrong during the file {filename} removal: {str(err)}')
        print(traceback.format_exc())


def gzip_a_file(filename=None, remove_original=False):
    """
    Compresses a file using Python gzip module

    :param remove_original: bool. Defines if the original file should be removed after compression
    :param filename: str. Absolute path to the file
    """
    with open(filename, 'rb') as f_in:
        with gzip.open(f'{filename}.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if remove_original:
        remove_file(filename)


def load_to_elastic(filename, remove_after_loading=False):
    if not filename:
        raise ValueError('No file to load. Please provide the first positional parameter')
    try:
        os.system(f"{ELLASTIC_COMMAND} {fname}")
    except Exception as err:
        print(f'Something was wrong during loading the file {filename} to elasticsearch: {str(err)}')
        print(traceback.format_exc())

    if remove_after_loading:
        remove_file(filename)


def generate_cdrs_file(filepath='',
                       filename='',
                       num_records=1000,
                       hours_amount=1,
                       compress=True
                       ):
    """
    Generates a fake Call Detail Record file for the hours_amount hours in past since the latest hour timestamp.

    :param filepath: str. path to save the generated CDR file to
    :param filename: str. name for the generated CDR file. Default convention is start_datetime_end_datetime.cdr
    :param num_records: int. amount of records in the generated file. Default is 1000
    :param hours_amount: int. amount of hours covered with CDR records. Default is 1
    :param compress: bool. Default is True. Defines whether the generated file should be compressed with gzip after the
        generation is complete.
    :return: absolute path to the file
    """

    fpath = ''
    if not filepath:
        fpath = f'{os.getcwd()}/cdrs'
    else:
        fpath = filepath

    fname = ''
    ts_end = datetime.datetime.now().replace(microsecond=0, second=0, minute=0)
    ts_start = ts_end - datetime.timedelta(hours=hours_amount)
    unix_ts_start = int(ts_start.timestamp())
    unix_ts_end = int(ts_end.timestamp())
    if not filename:
        # generate filename
        fmt = "%Y%m%d%H"
        strstarttime = f'{ts_start.strftime(fmt)}0000'
        strendtime = f'{ts_end.strftime(fmt)}0000'
        fname = f'{strstarttime}_{strendtime}.cdr'
    else:
        fname = filename

    if fname:
        with open(f'{fpath}/{fname}', 'w') as f:
            f.write(f'{header}\n')
            records = []
            counter = 0
            while counter < num_records:
                # args = (self, unix_timestamp=None, seconds_length=None)
                unix_call_start_ts = random.randrange(
                    unix_ts_start - random.randrange(2000),
                    unix_ts_end
                )
                shrt = random.randrange(0, 45)
                lng = random.randrange(46, 2000)
                seconds_length = random.choices((0, shrt, lng), weights=(10, 60, 30), k=1)[0]
                unix_call_end_ts = int(unix_call_start_ts) + int(seconds_length)

                if unix_call_end_ts in range(unix_ts_start, unix_ts_end):
                    cdrgn = FakeCallDetailRecord(unix_timestamp=unix_call_start_ts, seconds_length=seconds_length)
                    records.append(str(unix_ts_start) + ',' + cdrgn.get())
                    counter += 1

            if records:
                for arec in sorted(records):
                    f.write(','.join(arec.split(',')[1:]) + '\n')
            else:
                ValueError('CDRs were not generated')

    if compress:
        gzip_a_file(f'{fpath}/{fname}')
        os.remove(f'{fpath}/{fname}')
        return f'{fpath}/{fname}.gz'
    return f'{fpath}/{fname}'


def time_calls_dynamic_model(an_hour_number):
    """
    Provides a tabulated function reflecting the imaginary hourly calls dynamic.
    Please modify values dictionary if you wish provide other numbers.

    values dictionary contains key:value pairs associated with hour_number:multiplier
    logical values

    :param an_hour_number: int. A number from 0 to 23
    :return: int. Multiplier which value is between 1 and 10
    """

    if int(an_hour_number) not in range(0, 24):
        raise ValueError(f'an_hour_number parameter should be in range 0 - 23. {int(an_hour_number)}')

    values = {
        0: 6, 1: 3, 2: 1, 3: 1, 4: 1, 5: 2, 6: 3, 7: 4,
        8: 5, 9: 6, 10: 6,
        11: 6, 12: 7, 13: 6, 14: 7, 15: 8, 16: 8, 17: 9, 18: 10,
        19: 10, 20: 9, 21: 8, 22: 7, 23: 6
    }
    return values[an_hour_number]


if __name__ == '__main__':
    base_num_records = 3000
    num_records = time_calls_dynamic_model(datetime.datetime.now().hour) * \
                  random.randrange(1, 2) * random.randrange(base_num_records - 100, base_num_records + 100)
    fname = generate_cdrs_file(num_records=num_records,
                               hours_amount=1,
                               compress=False)
    load_to_elastic(fname, remove_after_loading=False)
