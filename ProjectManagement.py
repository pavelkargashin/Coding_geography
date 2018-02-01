# -*-coding:utf-8 -*-
import os
import parameters
def create_folders(inputpath):
    try:
       os.makedirs(inputpath)
       print "папка для проекта создана"
    except OSError:
        if not os.path.isdir(inputpath):
            raise

if __name__ == "__main__":
    create_folders(parameters.ProjectFolder)
    create_folders(parameters.InputData)
    create_folders(parameters.TempData)