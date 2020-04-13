#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import base64

with open("icon.py", "a") as f:
    f.write("img='")
with open("./picture/plane.ico", "rb") as i:
    b64str = base64.b64encode(i.read())
    with open("icon.py", "ab+") as f:
        f.write(b64str)
with open("icon.py", "a") as f:
    f.write("'")

