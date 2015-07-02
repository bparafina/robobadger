import boto
import json
import os
import subprocess
from datetime import datetime
from boto import rds2
import glob
import warnings
import fnmatch

db_identifier = 'stage'
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

log = conn.describe_db_log_files(db_identifier)
log_files = log['DescribeDBLogFilesResponse']['DescribeDBLogFilesResult']['DescribeDBLogFiles']
time = datetime.today().strftime('%Y-%m-%dT%H%M%S')

def index():
    for lf in log_files:
        lf = lf['LogFileName'].split('/')[-1]
        li = lf[24:]
        print li
        db_day = []
        db_hour = []
        print lf
        for hour in len(lf):
            print hour

def Getlogs():
    for lf in log_files:
        log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
        mkr = u'0'
        log_local_index =[]
        f = open(log_local_fn, 'w+')
        while mkr is not False:
            print mkr
            print 'mkr:{2} | {0}MB | {1}'.format(lf['Size'] / 1024 / 1024, lf['LogFileName'], mkr)
            fr = conn.download_db_log_file_portion(db_identifier, lf['LogFileName'], mkr)
            fpr = fr['DownloadDBLogFilePortionResponse']['DownloadDBLogFilePortionResult']

            if fpr['LogFileData'] is not None:
                f.write(fpr['LogFileData'].encode('utf8'))
            f.close()
            if fpr['AdditionalDataPending']:
                mkr = fpr['Marker']
                f = open(log_local_fn, 'a')
            else:
                mkr = False

def Processlogs():
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, log_local_fn):
            log_local_index.insert(file)
            print file
    log_local_fn_merged = log_local_fn[:-3]
    log_local_fn_raw = log_local_fn[:-2] + '*'
    merge_log = 'cat {0} > {1}'.format(log_local_fn_raw, log_local_fn_merged)
    subprocess.call(merge_log, shell=True)


    log_local_fn_out = log_local_fn + '.html'
    badger = '/usr/local/bin/pgbadger --prefix "%t:%r:%u@%d:[%p]:" {0} -o {1}'.format(log_local_fn, log_local_fn_out)
    subprocess.call(badger, shell=True)

if __name__ == '__main__':
    index()
    Getlogs()
    Processlogs()
