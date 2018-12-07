#-------------------------------------------------------------------------------
# Name:        download_by_file_type.py
# Purpose:
#
# Author:      Garret Krawchison
#
# Created:     4/26/2018
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib2
import os
#import zipfile
import logging
from urlparse import urlparse


thisDirectory = os.path.dirname(os.path.realpath(__file__))
outDirectory = thisDirectory + '\\downloads'

if not os.path.isdir(outDirectory):
    try:
        os.makedirs(outDirectory)
    except Exception, e:
        logging.info(e)

"""
Function listFiles(url, extension)
Create an array of all files listed in repository url for a given extension type
"""
def listFiles(url, extension):
    #print "Getting list of " + extension + " files on page..."
    logging.info("Getting list of %s files on page..." % extension)
    
    ## Connect to page
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    # Exceptions                    
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code
        logging.info("HTTP Error: %s" % e.code)
        logging.info("Please try again.")
        return
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        logging.info("URL Error: %s" % e.reason)
        logging.info("Please try again.")
        return
    except Exception, e:
        logging.info(e)
        logging.info("Please try again.")
        return
    
    ## Search for extension type on page
    listOfFiles = []
    ## Get a hrefs
    for node in soup.find_all('a'):
        try:
            if node.get('href').endswith(extension):
                listOfFiles.append(node.get('href'))
            elif ("." + extension in node['background']):
                listOfFiles.append(node['src'])
            elif ("." + extension in node['background-image']):
                listOfFiles.append(node['background-image'])
        except:
            pass

    ## Search img tags
    for node in soup.find_all('img'):
        try:
            if node['src'].endswith(extension):
                listOfFiles.append(node['src'])
        except:
            pass
            
    ## Search div backgrounds
    for node in soup.find_all('div'):
        try:
            if ("." + extension in node['background']):
                listOfFiles.append(node['background'])
            elif ("." + extension in node['background-image']):
                listOfFiles.append(node['background-image'])
        except:
            pass

    ## Search span backgrounds
    for node in soup.find_all('span'):
        try:
            if ("." + extension in node['background']):
                listOfFiles.append(node['background'])
            elif ("." + extension in node['background-image']):
                listOfFiles.append(node['background-image'])
        except:
            pass
  
    logging.info( "%s %s files found." % (str(len(listOfFiles)), extension) )
    
    ## Get first part of url with parameter
    for f in listOfFiles:
        if "?" in f:
            f = f.split("?")[0]
        elif "#" in f:
            f = f.split("?")[0]
            
        if f.startswith("//"):
            f = f[2:]
    
    return listOfFiles


"""
Function downloadFiles()
Loop through listFiles array and download files.
"""
def downloadFiles(url, extension):
    print "Searching %s" % url
    logging.info("Searching %s\n" % url)
    listOfFiles = listFiles(url, extension)
    if not listOfFiles:
        logging.info("\nUnable to download %s files from %s" % (extension, url))
        return
    logging.info("\nDownloading...\n")
    i = 0
    #files = []
    for f in listOfFiles:
        #if (i < 1):
        print("%s" % f)
        logging.info("%s" % f)
        #files.append(f)
        outFileName =  os.path.basename(f)
        outFilePath = outDirectory + '\\' + outFileName
        print outFilePath
        try:
            # Download zip file
            tryAgain = False
            try:
                theFile = urllib2.urlopen(f)                
                tryAgain = False
            except Exception as e:
                #logging.info(e)
                tryAgain = True
                            
            if tryAgain:
                try:
                    theFile = urllib2.urlopen(url + '/' + f)              
                    tryAgain = False
                except Exception as e:
                    #logging.info(e)
                    tryAgain = True
            
            if tryAgain:
                try:
                    urlParsed = urlparse(url)
                    base_url = "{uri.scheme}://{uri.netloc}/".format(uri=urlParsed)
                    theFile = urllib2.urlopen(base_url + '/' + f)                   
                except:
                    logging.info("...Failed to download %s" % url)
                    # All out of tries. Move on to next file.
                    continue
                
            # Open local file for writing
            with open(outFilePath, "wb") as local_file:
                local_file.write(theFile.read())  
            
            logging.info("...Success")
            i += 1
        # Exceptions					
        except urllib2.HTTPError, e:
            print "HTTP Error:", e.code, f
            logging.info("HTTP Error:", e.code, f)
        except urllib2.URLError, e:
            print "URL Error:", e.reason, f
            logging.info("URL Error:", e.reason, f)
    
    logging.info("\n%s files downloaded" % str(i))
    logging.info("\nSee: %s" % outDirectory )
    #return ", ".join(files)

"""
Function unpackZips()
Unpack all zips into the output directory
"""
# def unpackZips():
#     print "Unpack Zips"
#     logging.info("Unpack Zips")
#     zipFiles = os.listdir(outDirectory)
#     #files = []
#     for f in zipFiles:
#         if f.endswith('.zip'):
#             try:				
#                 # Unpack zip		
#                 myZip = zipfile.ZipFile(outDirectory + '\\' + f, 'r')
#                 myZip.extractall(outDirectory)
#                 myZip.close()
#                 print "Extracted " + f
#                 logging.info("Extracted " + f)
#             except Exception as e:
#                 print e
#                 logging.info(e)
# 
#     #return ", ".join(files)


def index(url, extension):
    ## Validate url
    if (url is None) or url.strip() == '':
        logging.info("\nEnter a valid URL to download from.")
        return
    
    ## Validate extension
    if (extension is None) or extension.strip() == '' or len(extension) > 10:
        logging.info("\nEnter a valid extension.")
        return
    
    extension = extension.replace(".","")
    
    downloadFiles(url, extension)
    #unpackZips()


if __name__ == '__main__':
    url = 'http://tax1.co.monmouth.nj.us/zipfiles/gis'
    extension = 'zip'
    #index(url, extension)
