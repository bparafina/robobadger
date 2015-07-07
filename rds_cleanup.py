import os, re, time
import pprint
from boto import rds2
import boto
import datetime

DAYS_EXPIRE = 7
## for future use to modularize script
region = os.getenv('region')
conn = boto.rds2.connect_to_region('us-east-1',aws_access_key_id=os.getenv('aws_access_key_id'),aws_secret_access_key=os.getenv('aws_secret_access_key'))

## what does this do now...???
def GetDBset():
    ## generate the dbset
    dbs = []
    instances = conn.describe_db_instances()
    instances = instances['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances']
    for db in instances:
        dbname = db['DBInstanceIdentifier']
        dbs.append(dbname)
    db_list = dbs


def Getsnapshots():
    ## get snapshot list to clean up
    dead_snaps = []
    snapshots = conn.describe_db_snapshots()
    list_snapshots = snapshots['DescribeDBSnapshotsResponse']['DescribeDBSnapshotsResult']['DBSnapshots']
    pprint.pprint(list_snapshots)
    for f in list_snapshots:
        snaptype = f['SnapshotType']
        if snaptype == 'manual':
            snap_name = f['DBSnapshotIdentifier']
            print snap_name
            snap_date = f['DBSnapshotIdentifier'][:-13]
            delta_date = datetime.timedelta(days=DAYS_EXPIRE)
            acceptable_date = datetime.datetime.now() - delta_date
            datestr = re.search(r'\d{4}-\d{2}-\d{2}', snap_date).group()
            try:
                ## shitty data made me do this
                date_object = datetime.datetime.strptime(datestr, '%Y-%m-%d')
            except:
                pass
            if (date_object < acceptable_date):
                dead_snaps.append(snap_name)
            continue
    print dead_snaps
    return dead_snaps


def Snapshotcleanup():
    ## delete those snaps
    dead_snaps = Getsnapshots()
    for f in dead_snaps:
        print 'Removing ' + f + ' from RDS'
        conn.delete_db_snapshot(f)

if __name__ == '__main__':
    GetDBset()
    Getsnapshots()
    Snapshotcleanup()
