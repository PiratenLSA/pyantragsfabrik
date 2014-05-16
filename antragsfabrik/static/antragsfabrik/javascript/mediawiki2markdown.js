/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

function header_replacer(match, p1, p2, offset, string) {
    return Array(p1.length + 1).join('#') + ' ' + p2;
}

function sublist_replacer(chars) {
    return function (math, p1, p2, offset, string) {
        return Array(p1.length + 1).join(' ') + chars + ' ' + p2;
    }
}

function markdown2wiki(input) {
    return input
        .replace(/\*(\*+)\s*(.+?)/g, sublist_replacer('*'))
        .replace(/#(#+)\s*(.+?)/g, sublist_replacer('1.'))
        .replace(/#\s*(.+?)/g, '1. $1')
        .replace(/(=+)\s*(.+?)\s*\1/g, header_replacer)
        .replace(/'''\s*(.+?)\s*'''/g, '**$1**')
        .replace(/''\s*(.+?)\s*''/g, '*$1*')
        .replace(/\[\[(.+?)\|(.+?)\]\]/g, '[$2](http://wiki.piratenpartei.de/$1)')
        .replace(/\[\[(.+?)\]\]/g, '[$1](http://wiki.piratenpartei.de/$1)')
        .replace(/\[(.+?) (.+?)\]/g, '[$2]($1)')
}