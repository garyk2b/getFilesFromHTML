# getFilesFromHTML
![Alt text](Download%20By%20File%20Type%20from%20HTML/downloadFileByExtension.png?raw=true "Title")

Get Files from HTML

This Python tool will download files for a given file type (extension) on an HTML web page.  It can be useful for projects that require sharing many links to files within an HTML page.

Enter a website URL and a file extension type (e.g. zip, jpg, kmz) into the field options and click Submit.  The tool will download the files from the page by searching for any link tags or embedded images on the page.  A downloads directory will be created where the tool exists.  This tool will not find any dynamic content such as ASPX or PHP and will not work on FTP protocol pages.

Created using the Beautiful Soup library for finding HTML content. GUI was built with TKinter.

Run the getFilesFromSite.exe file under the dist folder to get started. Or refer to getFilesFromSite.py to see how the tool works.
