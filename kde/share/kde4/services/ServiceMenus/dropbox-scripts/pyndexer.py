#!/usr/bin/env python
#	pyndexer.py - Generates index.html recursively for a given directory
#	Copyleft Eliphas Levy Theodoro
#	This script was primarily made for use with the Public Folder
#	feature of Dropbox - http://www.dropbox.com
#	See more information and get help at http://forums.dropbox.com/topic.php?id=3075
#	Some ideas/code got from AJ's version at http://dl.dropbox.com/u/259928/www/indexerPY/index.html

import getopt, re, ConfigParser
from os import path, getcwd, chdir, walk
from sys import argv, exit
from datetime import datetime as dt
from locale import setlocale, strxfrm, LC_ALL
setlocale(LC_ALL,"")

version = "0.7"
"""
ChangeLog
2009-05-03.0.1
	First try
2009-05-03.0.2
	Ordering folders and files. Forgot it.
2009-05-06.0.3
	Ignoring the index file on the list
2009-09-10.0.4
	File sort order ignoring case
2009-12-07.0.5
	Added two decimal digits to HumanSize
	File sort order with locale (removed case insensitive kludge)
2010-01-16.0.6
	Added JW player support to MP3 files, if JW player files are found on the same folder
		Required files: (player.swf, swfobject.js)
	Added ?dl suffix on links to "generic" files (not html/htm/txt/php)
		Makes the browser download it instead of opening. Change viewInBrowser var to remove other files
	If an index.html file is found on the folder, check it against the new one for differences before overwriting
		Saves a sync action on dropbox and a recent events
	Added a non-recursive togglable option: (-R,--recursive) or (-N,--nonrecursive) - still defaults to recursive!
		Change recursiveDirs variable if want to change the default
	Added verbose (-v,--verbose) option to print indexed files and folders individually
	Added ignorePattern option: (-i,--ignore), accepting python's regex, ex: ['index\..*','\..*']
		You can ignore multiple patterns with multiple --ignore arguments
2010-02-04.0.7
	Added listing encryption (AES-256-CBC) support with javascript
		http://www.vincentcheung.ca/jsencryption/
"""

### Mutable variables

# Index file name
indexFileName = "index.html"
# Stylesheet file name
stylesheet = "style.css"
# Configuration file name
configFileName = ".config;"
# Drop box link: replace this with your Dropbox referral link
dropboxLink = "https://www.dropbox.com/referrals/NTEwMTI3MjM5"
# Date format
dateFormat = "%d-%m-%Y&nbsp;%H:%M"
# Files ignored by default: Files related to pyndexer, all files starting with a dot (unix way to say "hidden"), and Mac OS folder icon files
ignorePattern = [re.escape(indexFileName), re.escape(stylesheet), '%s.*' % re.escape(configFileName), '\..*', 'Icon\\r']
# Files that will have the ?dl (download, not display) suffix on links
downloadExts = ['egg']
# Files to place the "play" radio button option
jwPlayExts = ['mp3']
# JWPlayer files to look for
jwPlayerFiles = ['player.swf','swfobject.js']
# JS encryption script
aesScript = '<script type="text/javascript" src="http://www.vincentcheung.ca/jsencryption/jsencryption.js"></script>'

#### Change this HTML to your needs. The "%(keyword)s" will be replaced by their respective values.

# javascript to place when files of "playable" type are found
htPlayerScript = """
		<script type="text/javascript" src="swfobject.js"></script>
		<script type="text/javascript">
			function toggle(rad){
				var song = rad.value;
				var swf = new SWFObject('player.swf','player','400','24','9','#ffffff');
				swf.addParam('allowfullscreen','false');
				swf.addParam('allowscriptaccess','never');
				swf.addParam('wmode','opaque');
				swf.addVariable('file',song);
				swf.addVariable('autostart','true');
				swf.write('player');
			}
		</script>"""

jsDecrypt = """
			<TR><TD colspan="3"><A href="javascript:decryptText('maincontents')">Show encrypted file listing</A></TD></TR>"""

# htmlBase
# accepts: {currentFolder} {stylesheet} {playerScript} {aesScript} {aesCipher} {dropboxLink} {parentLink} {maincontents} {genDate} {genVersion}
htmlBase = """
<HTML>
	<HEAD>
		<meta charset="utf-8">
		<TITLE>Dropbox :: Folder listing :: %(currentFolder)s</TITLE>
		<link rel="shortcut icon" href="http://www.dropbox.com/static/1238803391/images/favicon.ico"/>
		<link rel="stylesheet" href="http://www.dropbox.com/static/1241315492/css/sprites.css" type="text/css" media="screen"/>
		<style type="text/css"><!--
			*	{ font-family:lucida grande, lucida sans unicode, verdana; font-size:12px; border:none; }

			table	{ border-spacing:0px; width:800px; }
			td	{ padding:2px; }
			hr	{ height:1px; color:#C0C0C0; background-color:#C0C0C0; }
			.header { font-weight:bold; }
			.datecol	{ width:160px; }

			tbody td	{ padding-top:3px; }
			.comment	{ font-size:10px; color:#404040; padding:0px 20px 2px; }
			.sprite	{ float:left; padding-right:4px; }

			tfoot	{ color:#808080; }

			a	{ color:#1F75CC; text-decoration:none; }
			a:hover	{ color:#1F75CC; text-decoration:underline; }
			a:visited	{ color:#1F75CC; text-decoration:none; }
			a:visited:hover	{ color:#1F75CC; text-decoration:underline; }
			#dir:hover	{ background-color:#D7ECFF; }
			#file:hover	{ background-color:#D7ECFF; }

			#player	{ float:right; top:10px; }
		--></style>
		%(stylesheet)s
		%(playerScript)s
		%(aesScript)s
	</HEAD>
	<BODY><CENTER><TABLE>
		<THEAD>
			<TR><TD colspan="3">
				<DIV id="player"><!--replaced by js--></DIV>
				<A href="%(dropboxLink)s">
					<IMG alt="dropbox" src="http://www.dropbox.com/static/images/main_logo.png" title="Get a free Dropbox account">
				</A>
				<HR/>
			</TD></TR>
			<TR class="header">
				<TD align="left" class="namecol">Contents of %(currentFolder)s:</TD>
				<TD align="right" class="sizecol">Size</TD>
				<TD align="right" class="datecol">Date Modified</TD>
			</TR>
			%(parentLink)s
		</THEAD>
		<TFOOT>
			<TR><TD colspan="3"><HR/></TD></TR>
			<TR>
				<TD colspan="2">
					<SPAN id="pyndexmodified">
						Index file generated on %(genDate)s with
						<A href="http://dl.dropbox.com/u/552/pyndexer/index.html">pyndexer</A>
						v.%(genVersion)s
					</SPAN>
				</TD>
				<TD align="right">
					<IMG alt="dropbox" src="http://www.dropbox.com/static/images/gray_logo.gif" style="vertical-align:middle;">
					&copy; 2010 Dropbox
				</TD>
			</TR>
		</TFOOT>
		<TBODY id="maincontents" title="%(aesCipher)s">
			%(maincontents)s
		</TBODY>
	</TABLE></CENTER></BODY>
</HTML>
"""

# custom styles
# accepts: {stylesheet}
htStyleSheet = """
		<link href="%(stylesheet)s" rel="stylesheet" type="text/css" media="screen"/>"""

# parentLink
# used on child folders - the root folder do not provide this "up" link.
htParentLink = """
			<TR id="dir"><TD colspan="3">
				<A href="../%s">
					<IMG alt="up" src="http://www.dropbox.com/static/images/icons/icon_spacer.gif" class="sprite s_arrow_turn_up" />
					Parent folder
				</A>
			</TD></TR>
""" % indexFileName

# directory row
# accepts: {dirName} {indexFileName} {dirSize} {dirDate} {comment}
htDirRow = """
			<TR id="dir">
				<TD>
					<A href="%(dirName)s/%(indexFileName)s">
						<IMG alt="folder" src="http://www.dropbox.com/static/images/icons/icon_spacer.gif" class="sprite s_folder" />
						%(dirName)s%(comment)s
					</A>
				</TD>
				<TD align="right">%(dirSize)s</TD>
				<TD align="right">%(dirDate)s</TD>
			</TR>
"""

# static image of the file type
# accepts: {fileType}
htFileTypeImg = """<IMG alt="file" src="http://www.dropbox.com/static/images/icons/icon_spacer.gif" class="sprite %(fileType)s" />"""

# file to be played: radio button input
# accepts: {fileName}
htPlayerInput = """<input type="radio" name="playthis" title="Click to play" value="%(fileName)s" onclick="toggle(this)"/>"""

# item comment
# accepts: {comment}
htComment = """<div class="comment">%(comment)s</div/>"""

# file row
# accepts: {fileLink} {imgFile} {fileName} {radioButton} {fileSize} {fileDate} {comment}
htFileRow = """
			<TR id="file">
				<TD><A href="%(fileLink)s">%(imgFile)s%(fileName)s</A>%(radioButton)s%(comment)s</TD>
				<TD align="right">%(fileSize)s</TD>
				<TD align="right">%(fileDate)s</TD>
			</TR>
"""

# HTML ends here. From now on, the real script.

### helper things

# temporary file types dict for sprites
fileTypes = {
	('jpg', 'jpeg', 'png', 'tif', 'tiff', 'gif', 'bmp', 'ico', 'icns'): 's_page_white_picture',
	'psd': 's_page_white_paint',
	'pdf': 's_page_white_acrobat',
	('txt', 'rtf'): 's_page_white_text',
	('doc', 'docx'): 's_page_white_word',
	('xls', 'xlsx', 'csv'): 's_page_white_excel',
	('ppt', 'pptx', 'pps'): 's_page_white_powerpoint',
	('odt', 'ods', 'odp'): 's_page_white_tux',
	('html', 'htm', 'xml', 'css', 'js', 'py', 'bat'): 's_page_white_code',
	('c', 'h'): 's_page_white_c',
	'java': 's_page_white_cup',
	'php': 's_page_white_php',
	'rb': 's_page_white_ruby',
	('zip', 'gz', 'bz2', 'tar', 'tgz', 'tbz', 'rar', '7z'): 's_page_white_compressed',
	('iso', 'dmg'): 's_page_white_dvd',
	('mp3', 'm4a', 'ogg', 'oga', 'flac', 'wav', 'aiff', 'wma'): 's_page_white_sound',
	('mpg', 'mpeg', 'mp4', 'm4v', 'ogv', 'mkv', 'avi', 'mov', 'wmv'): 's_film',
	('exe', 'dll'): 's_page_white_gear',
}
# on first run let's make the dict right
for exts, desc in fileTypes.items():
	if not type(exts) == type(tuple()): continue
	for ext in exts: fileTypes[ext] = desc
	del(fileTypes[exts])
del desc, exts

def ignoreThis(thisname):
	for r in ignorePattern:
		if re.match(r, thisname, re.IGNORECASE):
			vprint('    ign:  %s' % thisname)
			return True
	return False

def jwPlayThis(files):
	r = False
	# do we have files of the play type?
	for f in files:
		if path.splitext(f)[1][1:].lower() in jwPlayExts:
			r = True
			break
	# ... but, are player files around?
	for f in jwPlayerFiles:
		if f not in files:
			r = False
	return r

def vprint(msg):
	if verbose: print msg

def HumanSize(bytes):
	"""Humanize a given byte size"""
	if bytes/1024/1024:
		return "%.2f&nbsp;MB" % round(bytes/1024/1024.0,2)
	elif bytes/1024:
		return "%d&nbsp;KB" % round(bytes/1024.0)
	else:
		return "%d&nbsp;B" % bytes

def Usage():
	me = path.basename(argv[0])
	print """%s
  Creates index.html files for proper display of folder contents on a website.

Usage: %s [args] [Folder1] [...] [FolderN]
  Starts index creation on [Folder1] and others.

Optional arguments:
  -h --help          This help text
  -v --verbose       Print indexed folders and files to be linked
  -i --ignore        Ignore this file pattern (python's regex re.match)
  -f --force         Always overwrite existing index files
  -R --recursive     Index subfolders
""" % (me, me)
	exit(1)

### The function that actually does the job

def index(dirname):
	chdir(dirname)
	# we will use this dict to know the number of items indexed in each directory
	dirSizes = {}
	rootDir = getcwd()
	for curDir, dirs, files in walk(rootDir, topdown=not recursiveDirs, followlinks=True):
		# skip over ignored directories (unless it's the root)
		# XXX Subdirs of ignored dirs will still get indexed. Fixing this would require
		#     restructuring as a recursive function, instead of looping with 'walk'.
		if not curDir == rootDir:
			if not recursiveDirs: break
			if ignoreThis(path.basename(curDir)): continue

		# generate index for this dir
		print('\nINFO: indexing "%s"' % curDir)

		# if existing index is not made by pyndexer, skip this dir without indexing it
		if not forceOverwrite and indexFileName in files:
			oldIndex = file(path.join(curDir, indexFileName)).read()
			reg = re.compile('<SPAN id="pyndexmodified">.*?</SPAN>',re.DOTALL)
			if not reg.search(oldIndex):
				print('    info:    existing index not made by pyndexer, will not be overwritten')
				del oldIndex
				continue

		# initialise config
		config = ConfigParser.RawConfigParser()
		config.add_section('Options')
		config.set('Options', 'encrypt', 'False')
		config.set('Options', 'parentlink', str(curDir!=rootDir))
		config.set('Options', 'dirlinks', str(recursiveDirs))
		config.set('Options', 'stylesheet', stylesheet)
		for fileName in files:
			if fileName.startswith(configFileName):
				vprint('    info:    configuration file found')
				config.read(path.join(curDir, fileName))
				password = fileName.replace(configFileName, '', 1)
				break

		# indexed count
		indexedFiles, indexedDirs = 0, 0

		# sort by locale
		dirs.sort(key = lambda k: strxfrm( k ) )
		files.sort(key = lambda k: strxfrm( k ) )

		# header and footer dicts
		htmlBaseDict = dict(
			currentFolder = path.basename(curDir),
			stylesheet = '',
			playerScript = '',
			aesScript = '',
			aesCipher = '',
			dropboxLink = dropboxLink,
			parentLink = '',
			maincontents = '',
			genDate = dt.now().strftime(dateFormat),
			genVersion = version,
		)

		# insert stylesheet if it exists
		if path.exists(path.join(curDir, config.get('Options', 'stylesheet'))):
			htmlBaseDict['stylesheet'] = htStyleSheet % {'stylesheet': config.get('Options', 'stylesheet')}

		# put player script if file requirements are met
		playableFolder = False
		if jwPlayThis(files):
			htmlBaseDict['playerScript'] = htPlayerScript
			playableFolder = True

		# write parent link
		if config.getboolean('Options', 'parentlink'):
			vprint('    link: parent folder')
			htmlBaseDict['parentLink'] = htParentLink

		# write folder links
		if config.getboolean('Options', 'dirlinks'):
			for dirName in dirs:
				if ignoreThis(dirName) or not path.exists(path.join(curDir, dirName, indexFileName)):
					continue # jump ignored names and dirs with no index
				fullDirName = path.join(curDir, dirName)
				fullDirDate = dt.fromtimestamp(path.getmtime(fullDirName)).strftime(dateFormat)
				d = {	'dirName': dirName, 'indexFileName': indexFileName,
					'dirSize': dirSizes.get(fullDirName, '--'), 'dirDate': fullDirDate, 'comment': '' }
				if config.has_option('Comments', dirName):
					d['comment'] = htComment % {'comment': config.get('Comments', dirName)}
				htmlBaseDict['maincontents'] += htDirRow % d
				vprint('    dir:  %s' % dirName)
				indexedDirs+=1

		# write file links
		for fileName in files:
			if ignoreThis(fileName): continue # jump ignored names
			fileExt = path.splitext(fileName)[1][1:].lower()
			fileLink = fileName
			if fileExt in downloadExts:
				fileLink = '%s?dl' % fileName
			fullFileName = path.join(curDir, fileName)
			fullFileDate = dt.fromtimestamp(path.getmtime(fullFileName)).strftime(dateFormat)
			imgFile = htFileTypeImg % { 'fileType': fileTypes.get(path.splitext(fileName)[-1][1:].lower(),'s_page_white') }
			d = {   'fileLink': fileLink, 'imgFile': imgFile, 'fileName': fileName, 'radioButton': '',
				'fileSize': HumanSize(path.getsize(fullFileName)), 'fileDate': fullFileDate, 'comment': '' }
			if playableFolder and fileExt in jwPlayExts:
				d['radioButton'] = htPlayerInput % {'fileName': fileName}
			if config.has_option('Comments', fileName):
				d['comment'] = htComment % {'comment': config.get('Comments', fileName)}
			htmlBaseDict['maincontents'] += htFileRow % d
			vprint('    file: %s' % fileName)
			indexedFiles+=1

		# show indexed file count
		print('    total:   %d dirs, %d files' % (len(dirs), len(files)))
		print('    indexed: %d dirs, %d files' % (indexedDirs, indexedFiles))

		# encrypt contents
		if hascrypto and config.getboolean('Options', 'encrypt'):
			print('    info:    encryption enabled, will encrypt listing.')
			if password == '':
				password = raw_input('*** please enter password for encryption:\n    ')
			else:
				print('    password:%s' % password)
			if password == '':
				print('WARN: no password given, listing will not be encrypted.')
			else:
				ciphertext = encrypt(htmlBaseDict['maincontents'], password)
				htmlBaseDict['aesScript'] = aesScript
				htmlBaseDict['aesCipher'] = '\n'.join(wrap(ciphertext, 64))
				htmlBaseDict['maincontents'] = jsDecrypt

		# see if we really need to write the new index file
		# XXX Unfortunately, cipher text will always be different even if content is unchanged,
		#     so encrypted listings will always be remade. Any thoughts?
		writeIndex = True
		if 'oldIndex' in locals():
			# remove gen.date and version
			oldIndex = reg.sub('', oldIndex)
			newIndex = reg.sub('', htmlBase % htmlBaseDict)
			if oldIndex == newIndex:
				writeIndex = False
				print('    info:    listing not changed, no need to update')
			del oldIndex, newIndex

		if writeIndex:
			htIndexFile = file(path.join(curDir, indexFileName),"w")
			htIndexFile.write(htmlBase % htmlBaseDict)
			htIndexFile.close()

		# get item count for this directory:
		# the trick here is having the walk function be called from bottom up, so the subdirs get processed first
		totalItems = indexedDirs + indexedFiles
		itemString = '%d %s' % (totalItems, 'item' if totalItems==1 else 'items')
		dirSizes[curDir] = itemString

try:
	from M2Crypto import EVP
	from os import urandom
	from hashlib import md5
	from cStringIO import StringIO
	from textwrap import wrap
	hascrypto = True
except ImportError:
	print('INFO: no M2Crypto support detected')
	hascrypto = False
def encrypt(string, password):
	prefix = 'Salted__'
	salt = urandom(8)
	hash = ['']
	for i in range(4):
		hash.append(md5(hash[i] + password + salt).digest() )
	key, iv =  hash[1] + hash[2], hash[3] + hash[4]
	del hash
	cipher = EVP.Cipher(alg='aes_256_cbc', key=key, iv=iv, op=1)
	inpb, outb = StringIO(string), StringIO()
	while 1:
		buf = inpb.read()
		if not buf: break
		outb.write(cipher.update(buf))
		outb.write(cipher.final())
	ciphertext = outb.getvalue()
	inpb.close()
	outb.close()
	return (prefix+salt+ciphertext).encode('base64')

# Execution
if __name__ == "__main__":
	# argument checking
	try:
		opts, dirnames = getopt.getopt(argv[1:], 'hvi:RNf', ['help','verbose','ignore=','recursive','nonrecursive','force'])
	except getopt.GetoptError, err:
		print 'ERR:  ', str(err)
		Usage()

	verbose = False
	recursiveDirs = False
	forceOverwrite = False
	for o, a in opts:
		if o in ('-h','--help'):
			Usage()
		elif o in ('-v','--verbose'):
			verbose = True
		elif o in ('-i','--ignore'):
			ignorePattern.append(a)
		elif o in ('-R','--recursive'):
			recursiveDirs = True
		elif o in ('-N','--nonrecursive'):
			recursiveDirs = False
		elif o in ('-f','--force'):
			forceOverwrite = True
	for d in dirnames:
		if not path.isdir(d):
			print "Invalid folder name: %s" % d
			Usage()
	if not dirnames:
		print('WARN: No folder names given')
		Usage()
	vprint('INFO: verbose mode set')
	if forceOverwrite: vprint('INFO: forced mode set')
	vprint('INFO: recursive mode is %s' % ('on' if recursiveDirs else 'off'))
	vprint('INFO: ignore patterns are...\n    %s' % '\n    '.join(ignorePattern))


	for dirname in dirnames:
		index(dirname)
