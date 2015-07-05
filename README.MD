Robobadger just wants to process logs. Robobadger wants to run as an automated job. Robobadger could probably output more useful stuff if combined with more infrastructure. Currently Robobadger works by pulling the full log list from AWS (Note: You'll need to have enabled verbose logging to get the most out of robobadger) and then downloading all of the logs. Since AWS produces one log an hour it will then merge the logs and produce a pgbadger report about them.

In my Jenkins job I then dump the reports into S3. I haven't figured out the rest yet.

You'll need AWS keys of course to actually access the DBs in question

Robobadger is structured to leverage the log file names from RDS. It works by rolling up a full days worth of logs (or max amount) into a single log file and then generates a report using pgbadger.

todo:

1. logs that are generated without full 24 hour coverage should probably report that fact in the name.

2. figure out a way to display this crap.
