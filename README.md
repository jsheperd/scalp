# scalp
Cut the head of a file without rewriting it on the supported filesystems (currently xfs and ext4).

I made it to simplify to truncate the long logfiles when there is no more spece on the disk, need to truncate the log
files but would like to keep the lest part of the long logs in the /var/log
