#! c:\python3\python.exe 
# coding: utf-8

with open('info.log') as f:
    logs = f.read().splitlines()
    for s in logs:
        print(s)
        # for val in s:
        #     for key, value in eval(val):
        #         print(key, value)
