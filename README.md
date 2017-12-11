## Procedures

### client
 1. creating directory /tmp/tmp_xxxx_poker
 2. cpoy backup.yaml to there
 3. for each task, create an directory for it
 4. copy files to each directory
 5. rename directorys to /tmp/poker-2017-12-7
 6. tar.gz it 
 7. upload it to oss?


### server
 1. An web interface to check the current files
 2. auto delete the history files in OSS


## Usage Draft

~~~
import poker

packer = poker.Packer("./backup_task.yaml")
p = packer.collect() # p = /tmp/backup_tasks-2017-12-11_7:23:34
tar_p = packer.compress() # tar_p = /tmp/backup_tasks-2017-12-11_7:23:34.tar.gz
packer.upload() # save the tar.gz file to specified localtion in yaml, e.g. s3, oss, or disk
~~~

~~~
import task
t = task.Task({"directory": ...})
t.collect("/tmp/tmp_ae3x_poker/etc)
~~~

## Discussions

Should we clean the packaged files after the Packer be dereferenced? Or we shold clean them explicitly?