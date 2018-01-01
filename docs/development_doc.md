# poker-cli procedures
 1. Creating directory /tmp/tmp_xxxx_poker, we called it `poker dir`.
 2. Cpoy backup.yaml to `poker dir`
 3. For each task, create a directory in `poker dir` for it. We call the created dir as `task dir`
 4. Collect the files matched the rule to coresponding `task dir`
 5. Rename the `poker dir` to /tmp/poker-2017-12-7
 6. tar.gz `poker dir` to poker-2017-12.tar.gz, or the specified name
 7. Uploaded it to S3

Compressed file structure:

~~~
specified_name.tar.gz
  poker-2017-12
    tasks.yml
    home
      [files matched the `home` task]
    etc
      [files matched the `etc` task]
~~~

# Preview Server

We can implement a preview server to brower the files.


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

- How to name the compressed file? Specifying by the command line's arguments? Or by the uploading plugin (in poker/contrib)?
  - How about specifing the major name in `task.yml`
    ~~~yml
    major_name: backup-ubuntu
    ~~~
    The compressed filename like `[marjor_name]-[minor_version]-2018-1-1.tar.gz`. The `minor_version` is used to avoid duplicate name and to identify the version. The `minor_version` is auto assigned to the `maximum minor_version + 1` in the destination. If there are multiple destinations, we increasing based on the maximum one.

    Then don't allow to specifing the name in comandline
    and the comand-cli shoud only print compressed file path, the others output into log/stderr

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

I'm consdier using coverall to repalce it! Codecov seems also easy enough!


## Log

maybe I need detail logs for debug, print is not good


## Issues

The compressed files root is /, not /tmp/poker-files 