from hn_flask.scraper import fetch_articles_from_html_page

SINGLE_HTML = """
<html><body>
<tr class="athing submission" id="46068015">
  <td class="title"><span class="titleline">
    <a href="https://example.com/article">Example Title</a>
    <span class="sitebit comhead">(<a href="from?site=example.com"><span class="sitestr">example.com</span></a>)</span>
  </span></td>
</tr>
<tr>
  <td colspan="2"></td>
  <td class="subtext">
    <span class="subline">
      <span class="score" id="score_46068015">130 points</span>
      by <a href="user?id=someone" class="hnuser">someone</a>
      <span class="age" title="2025-11-27T10:54:02 1764240842"><a href="item?id=46068015">5 hours ago</a></span>
    </span>
  </td>
</tr>
</body></html>
"""

MISSING_SCORE_LINK_HTML = """
<html><body>
<tr class="athing submission" id="123">
  <td class="title"><span class="titleline">
    <a>Title Without Link</a>
  </span></td>
</tr>
<tr>
  <td colspan="2"></td>
  <td class="subtext">
    <span class="subline">
      by <a href="user?id=someone" class="hnuser">someone</a>
      <span class="age" title="2025-11-27T12:00:00 0"><a href="item?id=123">2 hours ago</a></span>
    </span>
  </td>
</tr>
</body></html>
"""

MULTI_HTML = """
<html><body>
<tr class="athing submission" id="1">
  <td class="title"><span class="titleline"><a href="https://a">A</a></span></td>
</tr>
<tr><td colspan="2"></td><td class="subtext"><span class="subline">
  <span class="score" id="score_1">10 points</span>
  <span class="age" title="2025-11-27T01:00:00 0"></span>
</span></td></tr>

<tr class="athing submission" id="2">
  <td class="title"><span class="titleline"><a href="https://b">B</a></span></td>
</tr>
<tr><td colspan="2"></td><td class="subtext"><span class="subline">
  <span class="score" id="score_2">20 points</span>
  <span class="age" title="2025-11-27T02:00:00 0"></span>
</span></td></tr>
</body></html>
"""

def test_parse_single_article():
    articles = fetch_articles_from_html_page(SINGLE_HTML)
    assert isinstance(articles, list)
    assert len(articles) == 1
    a = articles[0]
    assert a["id"] == 46068015
    assert a["title"] == "Example Title"
    assert a["link"] == "https://example.com/article"
    assert a["points"] == 130
    assert a["created_at"] == "2025-11-27T10:54:02"

def test_missing_score_and_link():
    articles = fetch_articles_from_html_page(MISSING_SCORE_LINK_HTML)
    assert len(articles) == 1
    a = articles[0]
    assert a["id"] == 123
    assert a["title"] == "Title Without Link"
    assert a["link"] is None
    # no score span -> points should be None per scraper logic
    assert a["points"] is None
    assert a["created_at"] == "2025-11-27T12:00:00"

def test_multiple_articles():
    articles = fetch_articles_from_html_page(MULTI_HTML)
    assert len(articles) == 2
    ids = [a["id"] for a in articles]
    assert ids == [1, 2]
    assert articles[0]["points"] == 10
    assert articles[1]["points"] == 20
    assert articles[0]["created_at"] == "2025-11-27T01:00:00"
    assert articles[1]["created_at"] == "2025-11-27T02:00:00"