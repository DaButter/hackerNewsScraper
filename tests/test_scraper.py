from hn_flask.scraper import fetch_articles_from_html_page


SAMPLE_HTML = '''
<tr class="athing submission" id="46068015">
    <td align="right" valign="top" class="title">
        <span class="rank">1.</span>
    </td>
    <td valign="top" class="votelinks">
        <center>
            <a id='up_46068015' href='vote?id=46068015&amp;how=up&amp;goto=news'>
                <div class='votearrow' title='upvote'></div>
            </a>
        </center>
    </td>
    <td class="title">
        <span class="titleline">
            <a href="https://scienceclock.com/arthur-conan-doyle-delved-into-mens-mental-health-through-his-sherlock-holmes-stories/">Arthur Conan Doyle explored men’s mental health through Sherlock Holmes</a>
            <span class="sitebit comhead">
                (
                <a href="from?site=scienceclock.com">
                    <span class="sitestr">scienceclock.com</span>
                </a>
                )
            </span>
        </span>
    </td>
</tr>
<tr>
    <td colspan="2"></td>
    <td class="subtext">
        <span class="subline">
            <span class="score" id="score_46068015">130 points</span>
            by <a href="user?id=PikelEmi" class="hnuser">PikelEmi</a>
            <span class="age" title="2025-11-27T10:54:02 1764240842">
                <a href="item?id=46068015">5 hours ago</a>
            </span>
            <span id="unv_46068015"></span>
            | <a href="hide?id=46068015&amp;goto=news">hide</a>
            | <a href="item?id=46068015">145 &nbsp;comments</a>
        </span>
    </td>
</tr>
'''


def test_fetch_articles_from_html_page_basic():
    articles = fetch_articles_from_html_page(SAMPLE_HTML)
    assert len(articles) == 1
    a = articles[0]
    assert a["id"] == 46068015
    assert "Sherlock Holmes" in a["title"]
    assert a["link"].startswith("https://scienceclock.com")
    assert a["points"] == 130
    assert a["created"] == "2025-11-27T10:54:02"
