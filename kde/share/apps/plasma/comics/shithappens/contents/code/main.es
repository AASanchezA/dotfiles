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
    comic.comicAuthor = "Ralph Ruthe";
    comic.shopUrl = "http://www.ruthe.de/shop.html";
    comic.firstIdentifier = 1;
    comic.websiteUrl = "http://www.ruthe.de/index.php";

    comic.requestPage(comic.websiteUrl, comic.User);
}

function pageRetrieved(id, data)
{
    //find the most recent strip
    if (id == comic.User) {
        var re = new RegExp("rating\\.php', data: \"id=(\\d+)");
        var match = re.exec(data);
        if (match != null) {
            comic.lastIdentifier = match[1];
            comic.websiteUrl += "?pic=" + comic.identifier;
            comic.requestPage(comic.websiteUrl, comic.Page);
        } else {
            print("Could not get most recent strip.");
            comic.error();
            return;
        }
    }
    if (id == comic.Page) {
        var re = new RegExp("<img src=\"(cartoons/strip_\\d+[^\"]*\\.jpg)\"");
        var match = re.exec(data);
        var url;
        if (match != null) {
            url = "http://www.ruthe.de/" + match[1];
        } else {
            comic.error();
            print("Failed finding comic image.");
            return;
        }

        // get next id
        re = new RegExp("<li >[^\n]+b_next'\\);\" href=\"index\\.php\\?pic=(\\d+)");
        match = re.exec(data);
        if (match != null) {
            comic.nextIdentifier = match[1];
        } else {
            print("No next.");
        }

        // get previous id
        re = new RegExp("<li>[^\n]+b_back'\\);\" href=\"index\\.php\\?pic=(\\d+)");
        //re = new RegExp("<li>[^\n]+\('b_back'\);\" href=\"index\\.php\\?pic=(\\d+)");
        match = re.exec(data);
        if (match != null) {
            comic.previousIdentifier = match[1];
        } else {
            print("No previous.");
        }

        comic.requestPage(url, comic.Image);
    } else if (id == comic.Image) {
        comic.combine("header.png");
    }
}
