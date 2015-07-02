import boto
import json
import os
import subprocess
from datetime import datetime
from boto import rds2
import glob
import warnings

db_identifier = 'stage'
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

log = conn.describe_db_log_files(db_identifier)
log_files = log['DescribeDBLogFilesResponse']['DescribeDBLogFilesResult']['DescribeDBLogFiles']
log_files.sort(key=lambda r: r['LastWritten'], reverse=True)
time = datetime.today().strftime('%Y-%m-%dT%H%M%S')


for lf in log_files:
    log_local_fn = time + '-' + lf['LogFileName'].split('/')[-1]
    mkr = u'0'
    f = open(log_local_fn, 'w+')
    try:
        while mkr is not False:
            print 'mkr:{2} | {0}MB | {1}'.format(lf['Size'] / 1024 / 1024, lf['LogFileName'], mkr)
            fr = conn.download_db_log_file_portion(db_identifier, lf['LogFileName'], mkr)
            fpr = fr['DownloadDBLogFilePortionResponse']['DownloadDBLogFilePortionResult']

            if fpr['LogFileData'] is not None:
                f.write(fpr['LogFileData'].encode('utf8'))
            f.close()
            if fpr['AdditionalDataPending']:
                mkr = fpr['Marker']
                f = open(log_local_fn, 'a')
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
            else:
                mkr = False
    except (SyntaxError):
        pass

log_local_fn_merged = log_local_fn[:-3]
print log_local_fn_merged
log_local_fn_raw = log_local_fn[:-2] + '*'
print log_local_fn_raw
merge_log = 'cat {0} > {1}'.format(log_local_fn_raw, log_local_fn_merged)
subprocess.call(merge_log, shell=True)
#    log_local_fn_out = log_local_fn + '.html'
#    badger = '/usr/local/bin/pgbadger --prefix "%t:%r:%u@%d:[%p]:" {0} -o {1}'.format(log_local_fn, log_local_fn_out)
#    subprocess.call(badger, shell=True)
