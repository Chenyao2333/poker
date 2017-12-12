
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

- Should we clean the packaged files after the Packer be dereferenced? Or we shold clean them explicitly?

- Should we allow the multiple filters in one map in yaml config files?
  Maybe we can treate the multiple filters in one map as the "or" filer. The implementation is more "clear" in this defination! But is it a little confusing? e.g.

  Expression: (name = abc) or ((suffix = iso) or (name = def))
  ~~~yaml
  - name: abc
  - suffix: iso
    name: def
  ~~~

  Exception, `and`'s value is null
  ~~~yaml
  - and:
    name: abc
    file_size: < 10m
  ~~~

  Exception, `and` expect the list, not map
  ~~~yaml
  - and:
      name: abc
      file_size: < 10m
  ~~~

  Expression: (name = abc or file_zie < 10m>) and True
  ~~~yaml
  - and:
      - name: abc
        file_size: < 10m
  ~~~ 
  
  Expression: (name = .git or suffix = .svn) and (name = abc or name = def) and (dir_size < 10m)
  ~~~yaml
  - and:
    - name: .git
      suffix: .svn
    - or:
      - name: .git
      - name: .svn
    - dir_size: < 10m
  ~~~

  The decision is, **if the `dict` in the `list` of AndRule or OrRule**, then this dict is an OrRule.

## Coverage 

The codeclimate is good, but the it only supports the coverage.py with version >=4.0 <4.4. Why the pip won't solve it automatically? I will submit an issue.

Ok, I'm so frustrating with Codeclimate now. The readme badage load failed! I don't want to touch it until the project is done. Very frustrating!

I'm consdier using coverall to repalce it!