import os, re, time
import pprint
from boto import rds2
import boto

## for future use tomodularize script
region = os.getenv('region')
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

def touch (fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)


def GetDBset():
    dbs = []
    conn.describe_db_instances()
    instances = instances['DescribeDBInstanceResponse']['DescribeDBInstanceResult']['DBInstances']
    for db in instances:
        dbname = db['DBInstanceIdentifier']
        dbs.append(dbname)
    return(dbs)


def Getsnapshots():
    conn.describe_db_instances()
    instances = conn.describe_db_instances()
    snapshots = conn.describe_db_snapshots()
    list_snapshots = snapshots['DescribeDBSnapshotsRespone']['DescribeDBSnapshotsResult']['DBSnapshots']

def Snapshotcleanup():
    try:
        foo = bar
    except:
        pass

if name == '__main__':
    dir = 'var/lib/jenkins/jobs/prod-backup-list/rds-snapshots/'
    if not os.path.exists(dir):
        os.makedirs(dir)

    touch()
    Getsnapshots()
    Snapshotcleanup()
