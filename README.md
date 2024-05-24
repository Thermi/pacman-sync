# pacman-sync
script and hook for usage with pacman to synchronize directories that were updated during a system upgrade

## Usage

Install as pacman/libalpm hook.

```bash
$ python3 sync_fs.py -h
usage: sync_fs.py [-h] [-d]

Script for syncing mountpoints after system upgrades, to be used as script for an alpm-hook

options:
  -h, --help   show this help message and exit
  -d, --debug  Enable debug mode

```



## Internals

It finds the mountpoints that were changed by the installation/removal/upgrade of packages and syncs them to make sure the changes were written to disk before you continue using the system. This makes sure that if something bad happens afterwards that kills the system, the files that were changed by the package upgrade are already on the disk and can be used to start the system again.

To do this it does these things:

1) get all mounts on the system
2) remove all mounts of types that are in memory
3) remove all overlay filesystems
4) reads in each line of stdin (this is how pacman/libalpm integrate these hooks)
5) for each line it read from stdin, it finds on which of the remaining mounts it is and adds that mount to a list unless it is already on there
6) it syncs all mounts that are in the list

## Testing

You can easily test the script like this:

```bash
cat <<EOF | python3 sync_fs.py
/
/usr/share/test
/usr/share
/mnt/other/foo
/mnt/other/foobar
/mnt/other/test1
/sys/foo
/sys/foo/bar
/proc/123
/proc123123
/dev/pts/foo
/dev/foo
/dev
EOF
```

It will then output something like this:
```
2024-05-24 04:42:57,777 - INFO: Syncing these mountpoints now: ['/', '/mnt/other']
2024-05-24 04:42:57,778 - INFO: Mountpoints now synced
```

With debug mode activated you can see what it does internally:
```bash
2024-05-24 04:43:44,739 - INFO: enabling debug mode
2024-05-24 04:43:44,739 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 0
2024-05-24 04:43:44,740 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 1
2024-05-24 04:43:44,740 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 2
2024-05-24 04:43:44,740 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 3
2024-05-24 04:43:44,740 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 4
2024-05-24 04:43:44,740 - DEBUG: Check values: False False True
2024-05-24 04:43:44,740 - DEBUG: need to remove index 5
2024-05-24 04:43:44,741 - DEBUG: Check values: False False True
2024-05-24 04:43:44,741 - DEBUG: need to remove index 6
2024-05-24 04:43:44,741 - DEBUG: Check values: False True True
2024-05-24 04:43:44,741 - DEBUG: need to remove index 7
2024-05-24 04:43:44,741 - DEBUG: Check values: False True True
2024-05-24 04:43:44,741 - DEBUG: need to remove index 8
2024-05-24 04:43:44,741 - DEBUG: Check values: False True True
2024-05-24 04:43:44,741 - DEBUG: need to remove index 9
2024-05-24 04:43:44,741 - DEBUG: Check values: False True True
2024-05-24 04:43:44,741 - DEBUG: need to remove index 10
2024-05-24 04:43:44,741 - DEBUG: Check values: False True False
2024-05-24 04:43:44,741 - DEBUG: need to remove index 11
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 12
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 13
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 14
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 15
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 16
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,742 - DEBUG: need to remove index 17
2024-05-24 04:43:44,742 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 18
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 19
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 20
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 21
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 22
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 23
2024-05-24 04:43:44,743 - DEBUG: Check values: False True False
2024-05-24 04:43:44,743 - DEBUG: need to remove index 24
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,744 - DEBUG: need to remove index 25
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,744 - DEBUG: need to remove index 26
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,744 - DEBUG: need to remove index 27
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,744 - DEBUG: need to remove index 28
2024-05-24 04:43:44,744 - DEBUG: Check values: False True True
2024-05-24 04:43:44,744 - DEBUG: need to remove index 29
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,744 - DEBUG: need to remove index 30
2024-05-24 04:43:44,744 - DEBUG: Check values: False True False
2024-05-24 04:43:44,745 - DEBUG: need to remove index 31
2024-05-24 04:43:44,745 - DEBUG: Check values: False True True
2024-05-24 04:43:44,745 - DEBUG: need to remove index 32
2024-05-24 04:43:44,745 - DEBUG: Check values: False False False
2024-05-24 04:43:44,745 - DEBUG: Check values: False True True
2024-05-24 04:43:44,745 - DEBUG: need to remove index 34
2024-05-24 04:43:44,745 - DEBUG: Check values: False True False
2024-05-24 04:43:44,745 - DEBUG: need to remove index 35
2024-05-24 04:43:44,745 - DEBUG: Check values: True True False
2024-05-24 04:43:44,745 - DEBUG: need to remove index 36
2024-05-24 04:43:44,745 - DEBUG: Check values: False False False
2024-05-24 04:43:44,745 - DEBUG: Check values: True True False
2024-05-24 04:43:44,745 - DEBUG: need to remove index 38
2024-05-24 04:43:44,746 - DEBUG: Check values: True True False
2024-05-24 04:43:44,746 - DEBUG: need to remove index 39
2024-05-24 04:43:44,746 - DEBUG: Check values: True True True
2024-05-24 04:43:44,746 - DEBUG: need to remove index 40
2024-05-24 04:43:44,746 - DEBUG: Check values: True True True
2024-05-24 04:43:44,746 - DEBUG: need to remove index 41
2024-05-24 04:43:44,746 - DEBUG: Check values: False False False
2024-05-24 04:43:44,746 - DEBUG: indices to remove: [41, 40, 39, 38, 36, 35, 34, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18
, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
2024-05-24 04:43:44,746 - DEBUG: removing index 41 with value sdiskpart(device='tmpfs', mountpoint='/tmp', fstype='tmpfs', opts='rw,nosuid,nodev,size=8106932k,nr_inodes=1048576,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,746 - DEBUG: removing index 40 with value sdiskpart(device='run', mountpoint='/run', fstype='tmpfs', opts='rw,nosuid,nodev,relatime,mode=755,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,746 - DEBUG: removing index 39 with value sdiskpart(device='dev', mountpoint='/dev', fstype='devtmpfs', opts='rw,nosuid,relatime,size=8096312k,nr_inodes=2024078,mode=755,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,746 - DEBUG: removing index 38 with value sdiskpart(device='sys', mountpoint='/sys', fstype='sysfs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,746 - DEBUG: removing index 36 with value sdiskpart(device='proc', mountpoint='/proc', fstype='proc', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 35 with value sdiskpart(device='devpts', mountpoint='/dev/pts', fstype='devpts', opts='rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 34 with value sdiskpart(device='tmpfs', mountpoint='/dev/shm', fstype='tmpfs', opts='rw,nosuid,nodev,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 32 with value sdiskpart(device='tmpfs', mountpoint='/run/user/0', fstype='tmpfs', opts='rw,nosuid,nodev,relatime,size=1621384k,nr_inodes=405346,mode=700,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 31 with value sdiskpart(device='mqueue', mountpoint='/dev/mqueue', fstype='mqueue', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 30 with value sdiskpart(device='bpf', mountpoint='/sys/fs/bpf', fstype='bpf', opts='rw,nosuid,nodev,noexec,relatime,mode=700', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 29 with value sdiskpart(device='tmpfs', mountpoint='/run/user/1000', fstype='tmpfs', opts='rw,nosuid,nodev,relatime,size=1621384k,nr_inodes=405346,mode=700,uid=1000,gid=1000,inode64', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 28 with value sdiskpart(device='hugetlbfs', mountpoint='/dev/hugepages', fstype='hugetlbfs', opts='rw,relatime,pagesize=2M', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 27 with value sdiskpart(device='pstore', mountpoint='/sys/fs/pstore', fstype='pstore', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 26 with value sdiskpart(device='cgroup2', mountpoint='/sys/fs/cgroup', fstype='cgroup2', opts='rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 25 with value sdiskpart(device='debugfs', mountpoint='/sys/kernel/debug', fstype='debugfs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 24 with value sdiskpart(device='configfs', mountpoint='/sys/kernel/config', fstype='configfs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 23 with value sdiskpart(device='tracefs', mountpoint='/sys/kernel/tracing', fstype='tracefs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096) 
2024-05-24 04:43:44,747 - DEBUG: removing index 22 with value sdiskpart(device='securityfs', mountpoint='/sys/kernel/security', fstype='securityfs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 21 with value sdiskpart(device='binfmt_misc', mountpoint='/proc/sys/fs/binfmt_misc', fstype='binfmt_misc', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,747 - DEBUG: removing index 20 with value sdiskpart(device='fusectl', mountpoint='/sys/fs/fuse/connections', fstype='fusectl', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 19 with value sdiskpart(device='systemd-1', mountpoint='/proc/sys/fs/binfmt_misc', fstype='autofs', opts='rw,relatime,fd=34,pgrp=1,timeout=0,minproto=5,maxproto=5,direct,pipe_ino=18790', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 18 with value sdiskpart(device='efivarfs', mountpoint='/sys/firmware/efi/efivars', fstype='efivarfs', opts='rw,nosuid,nodev,noexec,relatime', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 17 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/ca393e273739', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 16 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/e84f66737bb7', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 15 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/a8c25e5b501e', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 14 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/fba85669ee5d', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 13 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/7b782b3a51f1', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 12 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/ddd2818c488a', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 11 with value sdiskpart(device='nsfs', mountpoint='/run/docker/netns/aa2a2be9e8e2', fstype='nsfs', opts='rw', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 10 with value sdiskpart(device='ramfs', mountpoint='/run/credentials/systemd-sysctl.service', fstype='ramfs', opts='ro,nosuid,nodev,noexec,relatime,mode=700', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 9 with value sdiskpart(device='ramfs', mountpoint='/run/credentials/systemd-sysusers.service', fstype='ramfs', opts='ro,nosuid,nodev,noexec,relatime,mode=700', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 8 with value sdiskpart(device='ramfs', mountpoint='/run/credentials/systemd-tmpfiles-setup.service', fstype='ramfs', opts='ro,nosuid,nodev,noexec,relatime,mode=700', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 7 with value sdiskpart(device='ramfs', mountpoint='/run/credentials/systemd-tmpfiles-setup-dev.service', fstype='ramfs', opts='ro,nosuid,nodev,noexec,relatime,mode=700', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 6 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/e63df262669659df35332e2df749755207b91e1eff1690d60b04d02d78ba4434/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/HUE4Z3RC2JAHBBDTHZHDWXRK2X:/var/lib/docker/overlay2/l/ORPZ6OCNV4RZ5TU2QK4KZKIR6D:/var/lib/docker/overlay2/l/VGAHR6N7RHVC5AU6VU64EUALZ3:/var/lib/docker/overlay2/l/GYPI2IC3BWEJIDYCUOSENBBSXP:/var/lib/docker/overlay2/l/DWHCPGT5THRUQVF5UWKWQI2O6N:/var/lib/docker/overlay2/l/ZD5BZVLM6OUMNNSN7QMBJRW74F:/var/lib/docker/overlay2/l/VNNGCD65WATSJXX7HCSBOUXNC2:/var/lib/docker/overlay2/l/AD4B3UZHCJXUEYDKSND5O36UHN:/var/lib/docker/overlay2/l/4PJB342LVG5ZYJPQ7TEOFKQICM:/var/lib/docker/overlay2/l/GUF72W2UX62AN2ABBCH4DAAOTR,upperdir=/var/lib/docker/overlay2/e63df262669659df35332e2df749755207b91e1eff1690d60b04d02d78ba4434/diff,workdir=/var/lib/docker/overlay2/e63df262669659df35332e2df749755207b91e1eff1690d60b04d02d78ba4434/work,index=off', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,748 - DEBUG: removing index 5 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/2326d283cb3f68221fb13cb1a4f7cd0e0dd09ff2209a06ea6d4dd334dafe639b/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/QCQ3IXS43LCSVSWZCBTR4D4JEI:/var/lib/docker/overlay2/l/ORPZ6OCNV4RZ5TU2QK4KZKIR6D:/var/lib/docker/overlay2/l/VGAHR6N7RHVC5AU6VU64EUALZ3:/var/lib/docker/overlay2/l/GYPI2IC3BWEJIDYCUOSENBBSXP:/var/lib/docker/overlay2/l/DWHCPGT5THRUQVF5UWKWQI2O6N:/var/lib/docker/overlay2/l/ZD5BZVLM6OUMNNSN7QMBJRW74F:/var/lib/docker/overlay2/l/VNNGCD65WATSJXX7HCSBOUXNC2:/var/lib/docker/overlay2/l/AD4B3UZHCJXUEYDKSND5O36UHN:/var/lib/docker/overlay2/l/4PJB342LVG5ZYJPQ7TEOFKQICM:/var/lib/docker/overlay2/l/GUF72W2UX62AN2ABBCH4DAAOTR,upperdir=/var/lib/docker/overlay2/2326d283cb3f68221fb13cb1a4f7cd0e0dd09ff2209a06ea6d4dd334dafe639b/diff,workdir=/var/lib/docker/overlay2/2326d283cb3f68221fb13cb1a4f7cd0e0dd09ff2209a06ea6d4dd334dafe639b/work,index=off', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,749 - DEBUG: removing index 4 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/390fad2f36edeb0e392661e35c806752dacd2f535bcfd012339c0af0d203dba7/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/CRVSY23OGLVGSOFEDPMPKXO3A7:/var/lib/docker/overlay2/l/JLML4BXJ6APWKW5ZTCZR3BBOSH:/var/lib/docker/overlay2/l/QMKL2GGUUHUSH4P3OWQAOCMNUJ:/var/lib/docker/overlay2/l/OMOLOGBZTLDZACSOOU26LVKUU6:/var/lib/docker/overlay2/l/3YP2TOATOPDZQYVBAJZPK4K6WQ:/var/lib/docker/overlay2/l/DI74TWURQZJTVPJI63BIAL6EK3:/var/lib/docker/overlay2/l/I4JJQMXCIX7U2KSCF2SZB3U4TC:/var/lib/docker/overlay2/l/HH6WRTUD74YFB2YO7CTBCNVVEU:/var/lib/docker/overlay2/l/HYU7CYH4DLHXTKMONTV7U37BZ4,upperdir=/var/lib/docker/overlay2/390fad2f36edeb0e392661e35c806752dacd2f535bcfd012339c0af0d203dba7/diff,workdir=/var/lib/docker/overlay2/390fad2f36edeb0e392661e35c806752dacd2f535bcfd012339c0af0d203dba7/work,index=off', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,749 - DEBUG: removing index 3 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/cc1750f725ec99523aeaf6417e75bfe352bc537c9c890f2e5526bb91f552c5a2/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/SYRTEESHAXZON6WVCJ6UXHIJHM:/var/lib/docker/overlay2/l/3MUI67QPMBWA45FWM3RSUX5HST:/var/lib/docker/overlay2/l/SI6NOJM7RTORNS6K3IPEF7NILZ:/var/lib/docker/overlay2/l/V3G42JOZC3YWLBPBEVCSHF3GU7:/var/lib/docker/overlay2/l/DLY4CR3VWLQSRJT3NO5LZA7WK4:/var/lib/docker/overlay2/l/6CJDGNK32BA2KZSC3YSANAIEJS:/var/lib/docker/overlay2/l/CTK7Z7C2XLCEJV2GUUXXZN325Z,upperdir=/var/lib/docker/overlay2/cc1750f725ec99523aeaf6417e75bfe352bc537c9c890f2e5526bb91f552c5a2/diff,workdir=/var/lib/docker/overlay2/cc1750f725ec99523aeaf6417e75bfe352bc537c9c890f2e5526bb91f552c5a2/work,index=off', maxfile=255, maxpath=4096) 
2024-05-24 04:43:44,749 - DEBUG: removing index 2 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/35b9c05e43045aa695fa4fa4338982b734c5083792b87cd5e3154d86c5f1cb88/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/ZU3ZW4LFHKV4VRHGPJJ5TXOW6B:/var/lib/docker/overlay2/l/ORPZ6OCNV4RZ5TU2QK4KZKIR6D:/var/lib/docker/overlay2/l/VGAHR6N7RHVC5AU6VU64EUALZ3:/var/lib/docker/overlay2/l/GYPI2IC3BWEJIDYCUOSENBBSXP:/var/lib/docker/overlay2/l/DWHCPGT5THRUQVF5UWKWQI2O6N:/var/lib/docker/overlay2/l/ZD5BZVLM6OUMNNSN7QMBJRW74F:/var/lib/docker/overlay2/l/VNNGCD65WATSJXX7HCSBOUXNC2:/var/lib/docker/overlay2/l/AD4B3UZHCJXUEYDKSND5O36UHN:/var/lib/docker/overlay2/l/4PJB342LVG5ZYJPQ7TEOFKQICM:/var/lib/docker/overlay2/l/GUF72W2UX62AN2ABBCH4DAAOTR,upperdir=/var/lib/docker/overlay2/35b9c05e43045aa695fa4fa4338982b734c5083792b87cd5e3154d86c5f1cb88/diff,workdir=/var/lib/docker/overlay2/35b9c05e43045aa695fa4fa4338982b734c5083792b87cd5e3154d86c5f1cb88/work,index=off', maxfile=255, maxpath=4096)
2024-05-24 04:43:44,749 - DEBUG: removing index 1 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/905473d0199c0471d9789773eb3580ef5986c05881555c69ddb3b3ad952371c4/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/NBKTZCQZMOBSZARNEW5SPPPSSV:/var/lib/docker/overlay2/l/24EWC2RA3WZUNCG4BITVXGOCCO:/var/lib/docker/overlay2/l/HFWRSY2B74P6CY5EQ5Z67NRL2A:/var/lib/docker/overlay2/l/YLG5EGA6F7PLMR6AYYXMLSNN7B:/var/lib/docker/overlay2/l/CSGQTHVH5VG6HQDA6RM2SWL55G:/var/lib/docker/overlay2/l/O3SG2ST4VHYRVOHLUZUBNIBGSN:/var/lib/docker/overlay2/l/NUUM2DTPWTUYJBP7DGJUZGLXOR,upperdir=/var/lib/docker/overlay2/905473d0199c0471d9789773eb3580ef5986c05881555c69ddb3b3ad952371c4/diff,workdir=/var/lib/docker/overlay2/905473d0199c0471d9789773eb3580ef5986c05881555c69ddb3b3ad952371c4/work,index=off', maxfile=255, maxpath=4096) 
2024-05-24 04:43:44,749 - DEBUG: removing index 0 with value sdiskpart(device='overlay', mountpoint='/var/lib/docker/overlay2/ca31d2ffc3e8e4507015c2e31a569c7538c1ad86d183f919e68a3ac3bdc9b9e3/merged', fstype='overlay', opts='rw,relatime,lowerdir=/var/lib/docker/overlay2/l/AXCDT2SVNMAO3A7EX54P5TDOH7:/var/lib/docker/overlay2/l/ORPZ6OCNV4RZ5TU2QK4KZKIR6D:/var/lib/docker/overlay2/l/VGAHR6N7RHVC5AU6VU64EUALZ3:/var/lib/docker/overlay2/l/GYPI2IC3BWEJIDYCUOSENBBSXP:/var/lib/docker/overlay2/l/DWHCPGT5THRUQVF5UWKWQI2O6N:/var/lib/docker/overlay2/l/ZD5BZVLM6OUMNNSN7QMBJRW74F:/var/lib/docker/overlay2/l/VNNGCD65WATSJXX7HCSBOUXNC2:/var/lib/docker/overlay2/l/AD4B3UZHCJXUEYDKSND5O36UHN:/var/lib/docker/overlay2/l/4PJB342LVG5ZYJPQ7TEOFKQICM:/var/lib/docker/overlay2/l/GUF72W2UX62AN2ABBCH4DAAOTR,upperdir=/var/lib/docker/overlay2/ca31d2ffc3e8e4507015c2e31a569c7538c1ad86d183f919e68a3ac3bdc9b9e3/diff,workdir=/var/lib/docker/overlay2/ca31d2ffc3e8e4507015c2e31a569c7538c1ad86d183f919e68a3ac3bdc9b9e3/work,index=off', maxfile=255, maxpath=4096)
2024-05-24 04:49:50,923 - DEBUG: checking /
2024-05-24 04:49:50,923 - DEBUG: checking /usr/share/test
2024-05-24 04:49:50,923 - DEBUG: checking /usr/share
2024-05-24 04:49:50,923 - DEBUG: checking /mnt/other/foo
2024-05-24 04:49:50,923 - DEBUG: checking /mnt/other/foobar
2024-05-24 04:49:50,923 - DEBUG: checking /mnt/other/test1
2024-05-24 04:49:50,924 - DEBUG: checking /sys/foo
2024-05-24 04:49:50,924 - DEBUG: checking /sys/foo/bar
2024-05-24 04:49:50,924 - DEBUG: checking /proc/123
2024-05-24 04:49:50,924 - DEBUG: checking /proc123123
2024-05-24 04:49:50,924 - DEBUG: checking /dev/pts/foo
2024-05-24 04:49:50,924 - DEBUG: checking /dev/foo
2024-05-24 04:49:50,924 - DEBUG: checking /dev
2024-05-24 04:49:50,925 - INFO: Syncing these mountpoints now: ['/', '/mnt/other']
2024-05-24 04:49:50,926 - INFO: Mountpoints now synced
```



## Installation

```bash
install -o root -g root -Dm0644 zz_sync.hook /etc/pacman.d/hooks/
install -o root -g root -Dm0755 sync_fs.py /etc/pacman.d/hooks/
```

