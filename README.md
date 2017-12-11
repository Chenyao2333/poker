
**It's in developing, the README is just the prototype and the function haven't been implemented. Pull Request is welcome!**

# Poker

Rule-based collect files and backup tool!

## Quick Start

### Case: Backup all the source code in cpp\python\go, and the .git directorys which size is less than 10m. Then save them to `/opt/backup/`.

Just write the following into `task.yml`, and run `poker -f task.yml`!

~~~yml
save_to:
  disk: /opt/poker

tasks:
  home:
    directory: "/home/louch"
    matchs:
      - suffix:
        - py
        - cpp
        - go
      - and:
        - name: .git
        - dir_size: < 10m

    ignores:
        - name:
          - "go1.9"
          - "anaconda3"
~~~


## A More Powerful Example

``` yml
save_to:
  s3:
    entrypoint: http://oss-cn-hangzhou.aliyuncs.com
    access_key: xxx
    secret_key: xxx
    bucket: poker-buckup

  disk: /opt/poker-backup

tasks:
  home:
    directory: "/home/louch"
    matchs:
      - suffix:
        - py
        - cpp
        - tex
        - go
        - conf
        - json
        - ipynb
        - html
        - js
        - css
        - md
        - srl
        - pem
      - name: .ssh
      - file_size: < 1m
      - and:
        - name: .git
        - dir_size: < 10m
      - and:
        - suffix: pdf
        - file_size: < 10m
    
    ignores:
        - and:
          - name: .git
          - file_size: ">= 10m"
        - name:
          - "louchenyao@gmail.com"
          - "go1.9"
          - "anaconda3"

  etc:
    directory: /etc
    match:
      - file_size: < 100k
```