#!C:\Python27\ArcGIS10.5\python.exe
import sys
import Maps_Tools_Regionalization

def main(regions, env, stat, year, chem):
    print year, env, regions, stat, chem
    Maps_Tools_Regionalization.regionalisation_process(regions, env, stat, year, chem)


if __name__ == '__main__':
    regions = sys.argv[1]
    env = sys.argv[2]
    stat = sys.argv[3]
    year = sys.argv[4]
    chem = sys.argv[5]
    main(regions, env, stat, year, chem)

