#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auther: ZhengZhong,Jiang

import database


if __name__ == "__main__":
    database.Base.metadata.drop_all(database.engine)
