/***************************************************************************
 *   Copyright (C) 2008-2011 Matthias Fuchs <mat69@gmx.net>                *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA .        *
 ***************************************************************************/

function init()
{
    comic.comicAuthor = "Tim Buckley";
    comic.firstIdentifier = "2002-10-23";
    comic.shopUrl = "http://www.splitreason.com/cad-comic/";

    comic.websiteUrl = "http://www.cad-comic.com/cad/";

    if (comic.identifierSpecified) {
        comic.websiteUrl += comic.identifier.toString("yyyyMMdd");
    }

    comic.requestPage(comic.websiteUrl, comic.Page);
}

function pageRetrieved(id, data)
{
    //find the next id if the next is the most recent
    if (id == comic.User) {
        var patternDate = "(((19|20)\\d\\d)(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))";
        var re = new RegExp("'bookmark-cad',\\s*'" + patternDate + "'");
        var match = re.exec(data);

        var url;

        if (match != null) {
            comic.nextIdentifier = date.fromString(match[1], "yyyyMMdd");
        } else {
            print("Could not find the most recent strip.");
            comic.error();
        }
    }
    if (id == comic.Page) {
        const patternDate = "(((19|20)\\d\\d)(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01]))";
        var re = new RegExp("'bookmark-cad',\\s*'" + patternDate + "'");
        var match = re.exec(data);

        if (!comic.identifierSpecified) {
            if (match != null) {
                comic.lastIdentifier = date.fromString(match[1], "yyyyMMdd");
                comic.websiteUrl += comic.identifier.toString("yyyyMMdd");
            } else {
                print("Failed to find the date.");
                comic.error();
                return
            }
        }

        var url;
        re = new RegExp("\"([^[\"]+/comics/[^\"]+)\"");
        match = re.exec(data);
        if (match != null) {
            url = match[1];
        } else {
            print("Could not find the image url.");
            comic.error();
            return;
        }

        re = new RegExp("/cad/" + patternDate + "\" class=\"nav-back");
        match = re.exec(data);
        if (match != null) {
            comic.previousIdentifier = match[2] + "-" + match[4] + "-" + match[5];
        }

        re = new RegExp("/cad/" + patternDate + "\" class=\"nav-next");
        match = re.exec(data);
        if (match != null) {
            comic.nextIdentifier = match[2] + "-" + match[4] + "-" + match[5];
        } else {
            //check if the next comic is the most recent
            re = new RegExp("href=\"/cad/\" class=\"nav-next");
            match = re.exec(data);
            if (match != null) {
                comic.requestPage("http://www.cad-comic.com/cad/", comic.User);
            }
        }

        re = new RegExp(url + "\" alt=\"([^\"]+)\"");
        match = re.exec(data);
        if (match != null) {
            comic.title = match[1];
        }

        print("Request: " + url);
        comic.requestPage(url, comic.Image);
    }
}
