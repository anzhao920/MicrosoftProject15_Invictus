import pandas as pd
import sys
import subprocess
import platform


def executeCProgram(CprogramFileName, systemType):
    command = []
    if 'Linux' in systemType:
        print(systemType)
        subprocess.call(["gcc", CprogramFileName, '-o', 'Cprogram'])  # For Compiling
        command = ['./Cprogram']
    elif 'Windows' in systemType:
        subprocess.call(["gcc", CprogramFileName])
        subprocess.call('a.exe')
        command = ['./Cprogram']
    elif 'Darwin' in systemType:
        subprocess.call(["gcc", CprogramFileName, '-o', 'Cprogram'])  # For Compiling
        command = ['./Cprogram']
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.communicate(input='dataToReadFile.txt\n'.encode())[0]


def writeInputForParser(WODFileName, CSVFileName):
    dataToReadFile = open("dataToReadFile.txt", "w")
    dataToReadFile.write(WODFileName + "\n")
    dataToReadFile.write("0\nA\n")
    dataToReadFile.write(CSVFileName + "\n1\n")
    dataToReadFile.close()


CprogramFileName = "wodtodepthmatrix.c"
WODFileName = "CTDO7106"
CSVFileName = "CTDO7106CSV.csv"
writeInputForParser(WODFileName, CSVFileName)
executeCProgram(CprogramFileName, platform.system())

wodDf = pd.read_csv("CTDO7105CSV.csv")
for col in wodDf.columns:
    print(col)
print(wodDf.head())