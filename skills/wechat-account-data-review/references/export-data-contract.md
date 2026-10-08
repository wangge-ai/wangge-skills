# Export Data Contract

Use this reference when WeChat backend export parsing fails or when mapping the parser into n8n/Dify.

## Current `tendency*.xls` Shape

The observed data trend export is an old Excel binary file with three horizontal tables in one sheet:

| Columns | Logical table | Required fields |
|---|---|---|
| B:D | daily channel reads | `日期`, `渠道`, `阅读人数` |
| F:J | daily interactions | `日期`, `分享人数`, `跳转阅读原文人数`, `微信收藏人数`, `发表篇数` |
| L:P | article source reads | `传播渠道`, `发表日期`, `内容标题`, `阅读人数`, `阅读人数占比` |

`传播渠道=全部` is the only safe total-read row for an article. Other rows are source-channel reads.

## Current `user_analysis.xls` Shape

The observed user growth export is HTML disguised as `.xls`.

Required row headers:

| Field | Meaning |
|---|---|
| `时间` | date |
| `新关注人数` | new followers |
| `取消关注人数` | unfollows |
| `净增关注人数` | net followers |
| `累积关注人数` | total followers |

Use BeautifulSoup/lxml if `pandas.read_excel` cannot determine the format.

## Article Archive Shape

Each article directory should contain:

| File | Use |
|---|---|
| `article_meta.json` | title, account name, publish date, URL, char/paragraph/image counts |
| `visual_analysis.md` | image role table, first image role, dominant image role |
| `layout.md` | text/image rhythm and article structure |
| `screens/mobile_long.png` | long screenshot for visual verification |
| `content.html` or `preview.html` | WeChat body HTML and image placement |

## Recommended Extra Export

Ask the user for article-level detail when available:

- article title and publish time
- reads / unique readers
- shares
- favorites
- likes / wow / comments
- read-after-follow or new followers
- completion rate / average read duration

Without this file, the report must label conversion and interaction attribution as approximate.
