
import poker.contrib.oss as oss

import datetime

def test_name():
    assert(oss.tar_name("backup-test", 5, datetime.datetime(year=2017, month=12, day=31)) == "backup-test-5-2017-12-31")
