import boto
import json
import os
import subprocess
from datetime import datetime
from boto import rds2
import glob
import warnings
import fnmatch
from tqdm import *

## set connection
db_identifier = 'stage'
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

## get the logs, set the time
log = conn.describe_db_log_files(db_identifier)
log_files = log['DescribeDBLogFilesResponse']['DescribeDBLogFilesResult']['DescribeDBLogFiles']
time = datetime.today().strftime('%Y-%m-%dT')


def Getlogs():
    try:
        for lf in tqdm(log_files):
            log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
            mkr = u'0'
            ## speed things up by checking for dupes
            if os.path.isfile(log_local_fn):
                print 'File Exists... skipping ' + log_local_fn + '\r',
            else:
                f = open(log_local_fn, 'w+')
                while mkr is not False:
                    ## open the file after you've checked
                    print 'mkr:{2} | {0}MB | {1} '.format(lf['Size'] / 1024 / 1024, lf['LogFileName'], mkr) + '\r',
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
    ## ignore the fact that there are logs that don't exist
    except (JSONResponseError):
        pass

def Processlogs():
    try:
        log_set = []
        for lf in log_files:
            log_local_fn = lf['LogFileName'].split('/')[-1][:-3]
            log_set.append(log_local_fn)
    except:
        pass
        ## get the uniques
    log_set = set(log_set)
    log_list = list(log_set)
    mkr = u'0'
    try:
        for lg in tqdm(log_list):
            log_merge = lg
            log_merge_name = log_merge + '.html'
            log_merge_wildcard = time + '-' + log_merge + '-*'
            if os.path.isfile(log_merge):
                print 'File Exists... skipping ' + log_merge,
            else:
                merge = 'cat {0} > {1}'.format(log_merge_wildcard, log_merge)
                subprocess.call(merge, shell=True)
            if os.path.isfile(log_merge_name):
                print 'File Exists... skipping ' + log_merge_name
            else:
                badger = 'pgbadger --prefix "%t:%r:%u@%d:[%p]:" {0} -o {1}'.format(log_merge, log_merge_name)
                subprocess.call(badger, shell=True)
    except:
        pass
    print log_list
def Cleanlogs():
    ## this is redundancy.. kind of irritating
    for lf in tqdm(log_files):
        log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
        mkr = u'0'
        for f in glob.glob(log_local_fn):
            os.remove(f)
    print 'Complete'

if __name__ == '__main__':
    Getlogs()
    Processlogs()
    Cleanlogs()
