/*
 *   Copyright (C) 2008 Stefan Majewsky <majewsky@gmx.net>
 *   Coyprigth (C) 2009-2010 Matthias Fuchs <mat69@gmx.net>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License version 2 as
 *   published by the Free Software Foundation
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
    comic.comicAuthor = "Jorge Cham";
    comic.shopUrl = "http://www.phdcomics.com/store/mojostore.php"
    url = "http://www.phdcomics.com/comics/archive.php";

    if (comic.identifier > 0) {
        url += "?comicid=" + comic.identifier;
    }
    comic.requestPage(url, comic.Page);
}

function pageRetrieved(id, data)
{
    if (id == comic.Page) {
        var match
        var re = new RegExp("http://www.phdcomics.com/comics/archive/phd([^\\.]+\\.gif)");
        var url;

        match = re.exec(data);
        if (match != null) {
            url = "http://www.phdcomics.com/comics/archive/phd" + match[1];
            comic.requestPage(url, comic.Image);
        }
        
        re = new RegExp("<td> <title>PHD Comics: ([^*]+)</title>");
        match = re.exec(data);
        if (match != null) {
            comic.additionalText = match[1];
        }

        // search the id of this comic if it was not specified
        if (comic.identifier < 1) {
            re = new RegExp("tellafriend\\.php\\?comicid=(\\d+)");
            match = re.exec(data);
            if (match != null) {
                comic.identifier = match[1];
            }
        }
        comic.websiteUrl = "http://www.phdcomics.com/comics/archive.php?comicid=" + comic.identifier;

        // now search if there is a next comic
        var s = data.toString();
        if (s.indexOf("images/next_button.gif") > -1) {
            comic.nextIdentifier = comic.identifier + 1;
        }

        // ...and previous
        if (comic.identifier > 1) {
            comic.previousIdentifier = comic.identifier - 1;
        }
    }
}
