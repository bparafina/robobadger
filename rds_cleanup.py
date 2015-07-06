import os, re, time
import pprint
from boto import rds2
import boto

DAYS_EXPIRE = 7

## for future use toi modularize script
region = os.getenv('region')
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

def GetDBset():
    ## generate the dbset
    dbs = []
    conn.describe_db_instances()
    instances = instances['DescribeDBInstanceResponse']['DescribeDBInstanceResult']['DBInstances']
    for db in instances:
        dbname = db['DBInstanceIdentifier']
        dbs.append(dbname)
    return(dbs)


def Getsnapshots():
    ## get snapshot list to clean up
    snapshots = conn.describe_db_snapshots()
    list_snapshots = snapshots['DescribeDBSnapshotsRespone']['DescribeDBSnapshotsResult']['DBSnapshots']
    for f in list_snapshots:
        snaptype = f['SnapshotType']
        if snaptype == 'manual':
            continue
        snap_id = f['DBSnapshotIdentifier']
        delta_date = datetime.timedelta(days=DAYS_EXPIRE)
        acceptable_date = datetime.datetime.now() - delta_date


def Snapshotcleanup():
    ## delete those snaps
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
