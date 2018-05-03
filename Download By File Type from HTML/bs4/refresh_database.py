#-------------------------------------------------------------------------------
# Name:        refresh_database
# Purpose:
#
# Author:      Garret Krawchison
#
# Created:     4/26/2018
#-------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib2
import os
import zipfile

thisDirectory = os.path.dirname(os.path.realpath(__file__))
outDirectory = thisDirectory + '\\txt'
outSqlFile = outDirectory + "\\county.sql"

# Download zips from repository into /zipfiles
repoUrl = 'http://tax1.co.monmouth.nj.us/zipfiles/gis'
extension = 'zip'

"""
Function listFiles(url, extension)
Create an array of all files listed in repository url
	"""

def listFiles(url, extension = ''):
	print "List Files in Repo"
	try:
		page = urllib2.urlopen(repoUrl)
		print page
		soup = BeautifulSoup(page, 'html.parser')
		return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(extension)]
	except Exception as e:
		print e

"""
Function downloadZips()
Loop through listFiles array and download files.
"""
def downloadZips():
	print "Download Zips"
	i = 0
	files = []
	for f in listFiles(repoUrl, extension):
		if (i <= 1):
			print("Download %s" % f)
			files.append(f)
			outFileName =  os.path.basename(f)
			outFilePath = outDirectory + '\\' + outFileName
			print outFilePath
			try:
				# Download zip file
				myZip = urllib2.urlopen(f)
				
				# Open local file for writing
				with open(outFilePath, "wb") as local_file:
					local_file.write(myZip.read())
			# Exceptions					
			except urllib2.HTTPError, e:
				print "HTTP Error:", e.code, f
			except urllib2.URLError, e:
				print "URL Error:", e.reason, f
		i += 1
		
	return ", ".join(files)

"""
Function unpackZips()
Unpack all zips into the output directory
"""
def unpackZips():
	print "Unpack Zips"
	zipFiles = os.listdir(outDirectory)
	files = []
	for f in zipFiles:
		if f.endswith('.zip'):
			try:				
				# Unpack zip		
				myZip = zipfile.ZipFile(outDirectory + '\\' + f, 'r')
				myZip.extractall(outDirectory)
				myZip.close()
				print "Extracted " + f
			except Exception as e:
				print e

	return ", ".join(files)

"""
Function txtToSql()
Read txt files into a SQL file called county.sql
"""
def txtToSql():
	print "Txt to SQL"
	sql = ""
	txtFiles = os.listdir(outDirectory)
	for f in txtFiles:
		if f.endswith('.txt'):
			try:
				txtFile = open(outDirectory + '\\' + f,'r')
				txtFileContents = txtFile.readlines()
				sql += "".join(txtFileContents)
				txtFile.close()
			except Exception as e:
				print e
		else:
			pass
		
	outputFile = open(outSqlFile, 'wb')
	outputFile.write(sql)
	outputFile.close()
	print "File written to %s" % outSqlFile
	
	# Add a column named GIS_PIN. Set value = concatenate "Municipality"_Block"_"Lot"_"Qual"

def index():
	pass


if __name__ == '__main__':
	index()