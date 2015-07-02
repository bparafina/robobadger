import boto
import json
import os
import subprocess
from datetime import datetime
from boto import rds2
import glob
import warnings
import fnmatch

## set connection
db_identifier = 'stage'
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

## get the logs, set the time
log = conn.describe_db_log_files(db_identifier)
log_files = log['DescribeDBLogFilesResponse']['DescribeDBLogFilesResult']['DescribeDBLogFiles']
time = datetime.today().strftime('%Y-%m-%dT')

## this needs to not be dumb
def Buildindex():
    for lf in log_files:
        output.add(lf)
        print output
    return(output)
## Retrieve Logs
def Getlogs():
    try:
        for lf in log_files:
            log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
            mkr = u'0'
            ## speed things up by checking for dupes
            if os.path.isfile(log_local_fn):
                print 'File Exists... skipping ' + log_local_fn
            else:
                f = open(log_local_fn, 'w+')
                while mkr is not False:
                    ## open the file after you've checked


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
    ## ignore the fact that there are logs that don't exist
    except (JSONResponseError):
        pass

def Processlogs():
    for lf in log_files:
#        log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
#        log_local_fn_merged = log_local_fn[:-3]
#        log_local_fn_raw = log_local_fn[:-2] + '*'
#        log_files_lf = lf['LogFileName'].split('/')[-1]
        print log_files_lf
#        log_local_list = set(log_files_lf).elems
#        print log_local_list

#        merge_log = 'cat {0} > {1}'.format(log_local_fn_raw, log_local_fn_merged)
#        subprocess.call(merge_log, shell=True)
#        log_local_fn_out = log_local_fn + '.html'
#        badger = '/usr/local/bin/pgbadger --prefix "%t:%r:%u@%d:[%p]:" {0} -o {1}'.format(log_local_fn, log_local_fn_out)
#        subprocess.call(badger, shell=True)


if __name__ == '__main__':
    Getlogs()
    Processlogs()
