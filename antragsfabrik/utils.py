# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from diff_match_patch import diff_match_patch


def diff_html(text1, text2):
    diff = diff_match_patch()
    text_diffs = diff.diff_main(text1, text2)
    diff.diff_cleanupSemantic(text_diffs)
    return diff_pretty_html(text_diffs)


def diff_pretty_html(diffs):
    html = []
    for (op, data) in diffs:
        text = (data.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br />"))
        if op == diff_match_patch.DIFF_INSERT:
            html.append('<ins class="diff">{}</ins>'.format(text))
        elif op == diff_match_patch.DIFF_DELETE:
            html.append('<del class="diff">{}</del>'.format(text))
        elif op == diff_match_patch.DIFF_EQUAL:
            html.append('<span class="diff">{}</span>'.format(text))
    return "".join(html)