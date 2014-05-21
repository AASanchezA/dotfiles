/*
 *   Copyright (C) 2008-2011 Matthias Fuchs <mat69@gmx.net>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License as
 *   published by the Free Software Foundation; either version 2, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details
 *
 *   You should have received a copy of the GNU Library General Public
 *   License along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

function init()
{
    comic.comicAuthor = "Joscha Sauer";
    comic.firstIdentifier = "2000-11-02";
    comic.shopUrl = "http://www.nichtlustig-shop.de/index.php";
    comic.websiteUrl = "http://static.nichtlustig.de/toondb/";

    if (comic.identifierSpecified) {
        comic.websiteUrl += comic.identifier.toString("yyMMdd") + ".html";
        comic.requestPage(comic.websiteUrl, comic.Page);
    } else {
        comic.requestPage("http://nichtlustig.de/main.html", comic.User);
    }
}

function extractDate(search, data)
{
    var dataString = data.toString();
    var start = dataString.indexOf(search);
    var url = "http://static.nichtlustig.de/toondb/";
    if (start != -1) {
        start = dataString.indexOf(url, start);
        if (start != -1) {
            start += url.length;
            var end = start + 6;
            return date.fromString("20" + dataString.slice(start, end), "yyyyMMdd");
        }
    }

    print("Could not find " + search);
    return null;
}

function pageRetrieved(id, data)
{
    if (id == comic.User) {
        var re = new RegExp("id=\"cartoontest\"><div class=\"front\"><a href=\"[^\"]*(\\d{6})\\.html");
        var match = re.exec(data);
        if (match != null) {
            comic.lastIdentifier = date.fromString("20" + match[1], "yyyyMMdd");
            comic.websiteUrl += comic.identifier.toString("yyMMdd") + ".html";
            comic.requestPage(comic.websiteUrl, comic.Page);
        } else {
            print("Could not find most recent comic strip.");
            comic.error();
            print(data);
            return;
        }
    } else if (id == comic.Page) {
        // Previous
        comic.previousIdentifier = extractDate("\"cl\"", data);

        // Next
        comic.nextIdentifier = extractDate("\"cr\"", data);

        // Cartoon
        var url = "http://static.nichtlustig.de/comics/full/" + comic.identifier.toString("yyMMdd") + ".jpg";
        comic.requestPage(url, comic.Image);
    }
}
