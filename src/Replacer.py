'''
@author: Tony
'''

import logging, re, shutil

__author__ = 'tony.zjt.test@gmail.com (Tony ZHOU)'

def replace(pattern, repl, filename):
    newfilename = filename + '.tmp'
    oldfile = open(filename, 'r')
    newfile = open(newfilename, 'w')
    
    for line in oldfile:
        logging.debug(line)
        
        newline = re.sub(pattern, repl, line, flags=re.S)
        logging.debug(newline)

        newfile.write(newline)
        
    oldfile.close()
    newfile.close()
    
    shutil.copy(newfilename, filename)
    
def remove(pattern, filename):
    newfilename = filename + '.tmp'
    oldfile = open(filename, 'r')
    newfile = open(newfilename, 'w')
    
    for line in oldfile:
        if pattern not in line:
            newfile.write(line)
        else:
            logging.debug('Removing "%s"', line)
        
    oldfile.close()
    newfile.close()
    
    shutil.copy(newfilename, filename)
    
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    replace('(.?)/(.?)', '\\1-\\2', "C:/Users/Tony/Desktop/stocks/nasdaq.csv");
    remove('^', "C:/Users/Tony/Desktop/stocks/nasdaq.csv");
    
