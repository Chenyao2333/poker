#! /usr/bin/env python3

import os
import datetime

def tar_name(major, minor, date):
    l = [major, minor, date.year, date.month, date.day]
    l = [str(x) for x in l]
    return "-".join(l)


def upload(config):
    try:
        oss_cfg = config["save_to"]["oss"]
        entrypoint = oss_cfg["entrypoint"]
        ak = oss_cfg["access_key"]
        sk = oss_cfg["secret_key"]
        bucket = oss_cfg["bucket"]

    except Exception:
        raise
