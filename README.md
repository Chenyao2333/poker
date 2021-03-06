
**It's in developing, Pull Request is welcome!**

# Poker

Rule-based collecting files and backup tool!

[![Build Status](https://travis-ci.org/Chenyao2333/poker.svg?branch=master)](https://travis-ci.org/Chenyao2333/poker)

## Quick Start

Using `pip` to install

~~~bash
pip install poker-tool
~~~

### Case: Backup all the source code in cpp\python\go.

Writing the following into `task.yml`, and run `poker-cli -f task.yml`!

~~~yml
tasks:
  c_and_cpp:
    directory: /home
    match:
      - suffix:
        - cpp
        - c
        - h
        - py
        - go
    ignore:
      - name:
        - .steam
        - "go1.9"
        - louchenyao@gmail.com

~~~


## A More Powerful Example

``` yml
# save_to is not yet implemented
save_to:
  s3:
    entrypoint: https://entrypoint.com
    access_key: AccessKey
    secret_key: SecretKey
    bucket: poker-buckup

tasks:
  home:
    directory: "/home/louch"
    match:
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
    
    ignore:
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
