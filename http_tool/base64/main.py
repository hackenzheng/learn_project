import base64
import time

inputFile = '/home/zhg/zhg/my_project/test.zip'
outputFile = '/home/zhg/zhg/my_project/testzip-base64'


def Base64EncodeFileToFile(inputFile,outputFile):
    fread = open(inputFile, 'rb')
    fwrite= open(outputFile, 'wb')
    base64.encode(fread,fwrite)
    fread.close()
    fwrite.close()


Base64EncodeFileToFile(inputFile, outputFile)

outputFile = '/home/zhg/zhg/my_project/zip_decode'
inputFile = '/home/zhg/zhg/my_project/testzip-base64'


def Base64DecodeFileToFile(inputFile,outputFile):
    print('[%s]' %(time.strftime('%X')))
    fileRead= open(inputFile, 'rb')

    print(fileRead)
    fileWrite = open(outputFile, 'wb')
    base64.decode(fileRead, fileWrite)
    fileRead.close()
    fileWrite.close()

    print('[%s]' %(time.strftime('%X')))


Base64DecodeFileToFile(inputFile, outputFile)