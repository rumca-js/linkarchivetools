def iso_z(dt):
    if dt:
        return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def social_data_to_json(social_data):
    json_entry = {}

    json_entry["thumbs_up"] = social_data.thumbs_up
    json_entry["thumbs_down"] = social_data.thumbs_down
    json_entry["view_count"] = social_data.view_count
    json_entry["stars"] = social_data.stars
    json_entry["followers_count"] = social_data.followers_count
    json_entry["upvote_diff"] = social_data.upvote_diff
    json_entry["upvote_ratio"] = social_data.upvote_ratio
    json_entry["upvote_view_ratio"] = social_data.upvote_view_ratio

    return json_entry

def entry_to_json(entry, with_id=False, source=None, social_data=None, tags=None):
    json_entry = {}

    if with_id:
        json_entry["id"] = entry.id
    json_entry["title"] = entry.title
    json_entry["description"] = entry.description
    json_entry["link"] = entry.link
    json_entry["date_created"] = iso_z(entry.date_created)
    json_entry["date_published"] = iso_z(entry.date_published)
    json_entry["date_dead_since"] = iso_z(entry.date_dead_since)
    json_entry["date_update_last"] = iso_z(entry.date_update_last)
    json_entry["date_last_modified"] = iso_z(entry.date_last_modified)
    json_entry["bookmarked"] = entry.bookmarked
    json_entry["permanent"] = entry.permanent
    json_entry["author"] = entry.author
    json_entry["album"] = entry.album
    json_entry["language"] = entry.language
    json_entry["page_rating_contents"] = entry.page_rating_contents
    json_entry["page_rating_votes"] = entry.page_rating_votes
    json_entry["page_rating_visits"] = entry.page_rating_visits
    json_entry["page_rating"] = entry.page_rating
    json_entry["age"] = entry.age
    json_entry["status_code"] = entry.status_code
    json_entry["thumbnail"] = entry.thumbnail

    json_entry["source_title"] = ""
    json_entry["source_url"] = entry.source_url
    if source:
        json_entry["source_title"] = source.title
        json_entry["source"] = source_to_json(source)

    if social_data:
        social_data_json = social_data_to_json(social_data)
        json_entry.update(social_data_json)

    json_entry["backgroundcolor"] = None
    json_entry["alpha"] = 1.0

    if tags:
        json_entry["tags"] = tags

    #json_entry["status_code_str"] = status_code_to_text(entry.status_code)
    #json_entry["contents_hash"] = json_encode_field(entry.contents_hash)
    #json_entry["body_hash"] = json_encode_field(entry.body_hash)
    #json_entry["meta_hash"] = json_encode_field(entry.meta_hash)
    #json_entry["last_browser"] = ""

    return json_entry


def source_to_json(source, with_id=False):
    json_data = {
       "link" : source.url,
       "title" : source.title,
       "language" : source.language,
       "favicon" : source.favicon,
    }

    json_data["id"] = source.id
    return json_data


def source_and_entries_to_rss(source_json, entries_jsons):
    channel_rss_text = source_json_to_rss(source_json)
    entry_rss_text = entry_jsons_to_rss(entries_jsons, channel_rss_text)

    rss_template = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/" 
     xmlns:atom="http://www.w3.org/2005/Atom" 
     version="2.0" 
     xmlns:media="http://search.yahoo.com/mrss/">
    <channel>
        {channel_info}
        {items}
    </channel>
</rss>"""

    return rss_template.format(channel_info=channel_rss_text, items=entry_rss_text)


def source_json_to_rss(source):
    channel_info = ""
    if source.get("title"):
        channel_info += f"<title>{source['title']}</title>\n"
    if source.get("url"):
        channel_info += f"<link>{source['url']}</link>\n"
    if source.get("favicon"):
        channel_info += f"<image><url>{source['favicon']}</url></image>\n"
    if source.get("date_published"):
        channel_info += f"<published>{source['date_published']}</published>\n"
    if source.get("language"):
        channel_info += f"<language>{source['language']}</language>\n"

    return channel_info


def entry_jsons_to_rss(entries, channel_info=""):
    """
    Channel info can be for example <title>Channel Title</title>
    """
    items = ""
    for entry in entries:
        entry_info = "<item>\n"

        if entry.get("title"):
            entry_info += f"<title><![CDATA[{entry['title']}]]></title>\n"
        if entry.get("link"):
            entry_info += f"<link><![CDATA[{entry['link']}]]></link>\n"
        if entry.get("description"):
            entry_info += (
                f"<description><![CDATA[{entry['description']}]]></description>\n"
            )
        if entry.get("date_published"):
            entry_info += f"<pubDate><![CDATA[{entry['date_published']}]]></pubDate>\n"
        if entry.get("thumbnail"):
            entry_info += f"<media:thumbnail url=\"{entry['thumbnail']}\"/>\n"

        entry_info += "</item>\n"

        items += entry_info

    return items
