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
import task
import upload

t = task.load("./backup_task.yaml")
p = t.execute() # p = /tmp/backup_tasks-2017-12-11_7:23:34
tar_p = t.targz() # tar_p = /tmp/backup_tasks-2017-12-11_7:23:34.tar.gz


upload.upload_to_oss(tar_p)
#uplaod.upload_to_s3(tar_p)
~~~