# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Nik Lutz <nik.lutz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys
use_old = True
if sys.version_info >= (3, 0):
    use_old = False

class UnicodingError(Exception):
    pass

# these encodings should be in most likely order to save time
encodings = [ "ascii", "utf_8", "big5", "big5hkscs", "cp037", "cp424", "cp437", "cp500", "cp737", "cp775", "cp850", "cp852", "cp855",
    "cp856", "cp857", "cp860", "cp861", "cp862", "cp863", "cp864", "cp865", "cp866", "cp869", "cp874", "cp875", "cp932", "cp949",
    "cp950", "cp1006", "cp1026", "cp1140", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257", "cp1258",
    "euc_jp", "euc_jis_2004", "euc_jisx0213", "euc_kr", "gb2312", "gbk", "gb18030", "hz", "iso2022_jp", "iso2022_jp_1", "iso2022_jp_2",
    "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr", "latin_1", "iso8859_2", "iso8859_3", "iso8859_4", "iso8859_5",
    "iso8859_6", "iso8859_7", "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_13", "iso8859_14", "iso8859_15", "johab", "koi8_r", "koi8_u",
    "mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman", "mac_turkish", "ptcp154", "shift_jis", "shift_jis_2004",
    "shift_jisx0213", "utf_32", "utf_32_be", "utf_32_le", "utf_16", "utf_16_be", "utf_16_le", "utf_7", "utf_8_sig" ]

def in_unicode(string):
    if use_old:
        return _in_unicode(string)
    if isinstance(string, bytes):
        return string.decode("utf-8")
    return str(string)

def _in_unicode(string):
    # FIXME - fix the sender!
    if string == None:
        return "None"
    if isinstance(string, int):
        return str(string)
    if isinstance(string, float):
        return str(string) 
    if isinstance(string, long):
        return str(string)     
    if isinstance(string, tuple):
        if len(string) > 1:
            return in_unicode(string[0])
        return ""
    if isinstance(string, unicode):
        return string
    for enc in encodings:
        try:
            utf8 = unicode(string, enc)
            return utf8
        except:
            if enc == encodings[-1]:
                #raise UnicodingError("still don't recognise encoding after trying do guess.")
#                print type(string)
                return "problem with string decoding"
    return "problem with string decoding"


def proplist_to_dict(string):
    dict = {}
    lines = string.split("\n")
    for line in lines:
        arr = line.split(" = ")
        if len(arr) == 2:
            dict[arr[0]] = in_unicode(arr[1].strip('"'))
    return dict

def assertEncoding(aDict):
    for key in aDict.keys():
        try:
            aDict[key]= in_unicode(aDict[key])
        except:
            aDict[key] = "error with string encoding #1"
    return aDict
