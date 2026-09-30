"""
Provided to be able to create tables in empty file

This produces tables that could be used outside of python, and outside of sqlalchemy.
Meaning default values need to be 'server_defaults'.
"""

from typing import Optional
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    create_engine,
    select,
    func,
    delete,
    update,
    asc,
    desc,
)
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    LargeBinary,
    Time,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import timedelta, datetime, timezone

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


Base = declarative_base()


class ApiKeys(Base):
    """
    Keys that allows users to access system
    """
    __tablename__ = "apikeys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(1000), unique=True)
    user_id: Mapped[int]


class AppLogging(Base):
    __tablename__ = "applogging"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    info_text: Mapped[str] = mapped_column(String(2000))
    detail_text: Mapped[Optional[str]] = mapped_column(String(2000))
    level: Mapped[int] = mapped_column(server_default="0")
    date = mapped_column(DateTime(timezone=True), nullable=True)


class BackgroundJob(Base):
    __tablename__ = "backgroundjob"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job: Mapped[str] = mapped_column(String(1000))
    task: Mapped[Optional[str]]
    subject: Mapped[str] = mapped_column(String(1000))
    args: Mapped[Optional[str]]
    date_created = mapped_column(DateTime(timezone=True), nullable=True)

    priority: Mapped[int] = mapped_column(server_default="0")
    errors: Mapped[int] = mapped_column(server_default="0")
    enabled: Mapped[bool] = mapped_column(server_default="1")

    user_id: Mapped[Optional[int]]


class BackgroundJobHistory(Base):
    __tablename__ = "backgroundjobhistory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job: Mapped[str] = mapped_column(String(1000))
    task: Mapped[Optional[str]]
    subject: Mapped[str] = mapped_column(String(1000))
    args: Mapped[Optional[str]]
    date_created = mapped_column(DateTime(timezone=True), nullable=True)


class BlockEntryList(Base):
    __tablename__ = "blockentrylist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    processed: Mapped[bool] = mapped_column(server_default="0")


class BlockEntry(Base):
    __tablename__ = "blockentry"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    block_list_id: Mapped[Optional[int]]


class Browser(Base):
    __tablename__ = "browser"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(server_default="1")
    name: Mapped[Optional[str]] = mapped_column(String(2000)) # name of browser, could be crawler_name
    priority: Mapped[int] = mapped_column(server_default="0")
    ignore_errors: Mapped[bool] = mapped_column(server_default="0")
    user_agent: Mapped[Optional[str]] = mapped_column(String(2000))
    request_headers: Mapped[Optional[str]] = mapped_column(String(2000))
    timeout_s: Mapped[int] = mapped_column(server_default="0")
    delay_s: Mapped[int] = mapped_column(server_default="0")
    ssl_verify: Mapped[bool] = mapped_column(server_default="0")
    respect_robots_txt: Mapped[bool] = mapped_column(server_default="0")
    accept_types: Mapped[Optional[str]] = mapped_column(String(2000))
    bytes_limit: Mapped[int] = mapped_column(server_default="0")
    http_proxy: Mapped[Optional[str]] = mapped_column(String(2000))
    https_proxy: Mapped[Optional[str]] = mapped_column(String(2000))
    settings: Mapped[Optional[str]] = mapped_column(String(2000)) # obsolete
    cookies: Mapped[Optional[str]] = mapped_column(String(2000))
    handler_name: Mapped[Optional[str]] = mapped_column(String(2000)) # handler_name


class ConfigurationEntry(Base):
    __tablename__ = "configurationentry"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instance_title: Mapped[str] = mapped_column(String(500))
    instance_description: Mapped[Optional[str]] = mapped_column(String(500))
    instance_internet_location: Mapped[Optional[str]] = mapped_column(String(200))
    favicon_internet_url: Mapped[Optional[str]] = mapped_column(String(200))
    admin_user: Mapped[Optional[str]] = mapped_column(String(500))

    view_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    download_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    add_access_type: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Fixed typo: "sever_default" -> "server_default"
    logging_level: Mapped[int] = mapped_column(server_default="0")
    initialized: Mapped[bool] = mapped_column(server_default="false")
    initialization_type: Mapped[Optional[str]] = mapped_column(String(100))
    enable_background_jobs: Mapped[bool] = mapped_column(server_default="true")
    block_job_queue: Mapped[bool] = mapped_column(server_default="false")
    use_internal_scripts: Mapped[bool] = mapped_column(server_default="false")
    cleanup_time = mapped_column(Time(), nullable=True)

    data_import_path: Mapped[Optional[str]] = mapped_column(String(2000))
    data_export_path: Mapped[Optional[str]] = mapped_column(String(2000))
    download_path: Mapped[Optional[str]] = mapped_column(String(2000))
    auto_store_thumbnails: Mapped[bool] = mapped_column(server_default="false")
    thread_memory_threshold: Mapped[int] = mapped_column(server_default="0")

    enable_keyword_support: Mapped[bool] = mapped_column(server_default="false")
    enable_domain_support: Mapped[bool] = mapped_column(server_default="false")
    enable_file_support: Mapped[bool] = mapped_column(server_default="false")
    enable_link_archiving: Mapped[bool] = mapped_column(server_default="false")
    enable_source_archiving: Mapped[bool] = mapped_column(server_default="false")
    enable_crawling: Mapped[bool] = mapped_column(server_default="false")
    enable_social_data: Mapped[bool] = mapped_column(server_default="false")

    accept_dead_links: Mapped[bool] = mapped_column(server_default="false")
    accept_ip_links: Mapped[bool] = mapped_column(server_default="false")
    accept_domain_links: Mapped[bool] = mapped_column(server_default="false")
    accept_non_domain_links: Mapped[bool] = mapped_column(server_default="false")
    accept_unknown_links: Mapped[bool] = mapped_column(server_default="false")
    accept_onion_links: Mapped[bool] = mapped_column(server_default="false")
    accept_same_hashes: Mapped[bool] = mapped_column(server_default="false")

    auto_crawl_sources: Mapped[bool] = mapped_column(server_default="false")
    auto_scan_new_entries: Mapped[bool] = mapped_column(server_default="false")
    auto_scan_updated_entries: Mapped[bool] = mapped_column(server_default="false")
    new_entries_merge_data: Mapped[bool] = mapped_column(server_default="false")
    new_entries_use_clean_data: Mapped[bool] = mapped_column(server_default="false")
    new_entries_fetch_social_data: Mapped[bool] = mapped_column(server_default="false")
    browse_entries_fetch_social_data: Mapped[bool] = mapped_column(server_default="false")
    browse_entry_fetch_social_data: Mapped[bool] = mapped_column(server_default="false")
    entry_update_fetches_social_data: Mapped[bool] = mapped_column(server_default="false")
    entry_update_via_internet: Mapped[bool] = mapped_column(server_default="false")
    days_inactivity_to_disable_source: Mapped[int] = mapped_column(server_default="0")

    log_remove_entries: Mapped[bool] = mapped_column(server_default="false")
    auto_create_sources: Mapped[bool] = mapped_column(server_default="false")
    default_source_state: Mapped[bool] = mapped_column(server_default="false")
    prefer_https_links: Mapped[bool] = mapped_column(server_default="false")
    prefer_non_www_links: Mapped[bool] = mapped_column(server_default="false")

    new_entries_download_audio: Mapped[bool] = mapped_column(server_default="false")
    new_entries_download_video: Mapped[bool] = mapped_column(server_default="false")
    entry_update_download_audio: Mapped[bool] = mapped_column(server_default="false")
    entry_update_download_video: Mapped[bool] = mapped_column(server_default="false")

    sources_refresh_period: Mapped[int] = mapped_column(server_default="0")
    days_to_move_to_archive: Mapped[int] = mapped_column(server_default="0")
    days_to_remove_links: Mapped[int] = mapped_column(server_default="0")
    days_to_remove_stale_entries: Mapped[int] = mapped_column(server_default="0")
    days_to_check_std_entries: Mapped[int] = mapped_column(server_default="0")
    days_to_check_stale_entries: Mapped[int] = mapped_column(server_default="0")
    days_to_remove_social_data: Mapped[int] = mapped_column(server_default="0")
    remove_entry_vote_threshold: Mapped[int] = mapped_column(server_default="1")
    number_of_update_entries: Mapped[int] = mapped_column(server_default="1")

    remote_webtools_server_location: Mapped[Optional[str]] = mapped_column(String(500), server_default="")
    internet_status_test_url: Mapped[Optional[str]] = mapped_column(
        String(500), server_default="https://google.com"
    )

    track_user_actions: Mapped[bool] = mapped_column(server_default="false")
    track_user_searches: Mapped[bool] = mapped_column(server_default="false")
    track_user_navigation: Mapped[bool] = mapped_column(server_default="false")
    max_user_entry_visit_history: Mapped[int] = mapped_column(server_default="1")
    max_number_of_user_search: Mapped[int] = mapped_column(server_default="1")
    vote_min: Mapped[int] = mapped_column(server_default="-100")
    vote_max: Mapped[int] = mapped_column(server_default="-100")
    number_of_comments_per_day: Mapped[int] = mapped_column(server_default="-100")

    time_zone: Mapped[int] = mapped_column(server_default="-100")
    display_style: Mapped[str] = mapped_column(String(100), server_default="")

    display_type: Mapped[str] = mapped_column(String(100), server_default="")
    show_icons: Mapped[bool] = mapped_column(server_default="false")
    entry_preview: Mapped[bool] = mapped_column(server_default="true")  # entry detail view playback
    thumbnails_as_icons: Mapped[bool] = mapped_column(server_default="false")
    small_icons: Mapped[bool] = mapped_column(server_default="false")
    local_icons: Mapped[bool] = mapped_column(server_default="false")
    highlight_bookmarks: Mapped[bool] = mapped_column(server_default="false")
    click_behavior_modal_window: Mapped[bool] = mapped_column(server_default="false")
    links_per_page: Mapped[int] = mapped_column(server_default="100")
    sources_per_page: Mapped[int] = mapped_column(server_default="100")
    max_links_per_page: Mapped[int] = mapped_column(server_default="100")
    max_sources_per_page: Mapped[int] = mapped_column(server_default="100")
    max_number_of_related_links: Mapped[int] = mapped_column(server_default="100")

    entries_visit_alpha: Mapped[float] = mapped_column(server_default="0.6")
    entries_dead_alpha: Mapped[float] = mapped_column(server_default="0.6")

    debug_mode: Mapped[bool] = mapped_column(server_default="false")


class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(1000), unique=True)  # credential name. github, or reddit etc.
    credential_type: Mapped[str] = mapped_column(String(1000), nullable=True) # refresh token, auth token, etc
    username: Mapped[str] = mapped_column(String(1000), nullable=True)
    password: Mapped[str] = mapped_column(String(1000), nullable=True)
    secret: Mapped[str] = mapped_column(String(1000), nullable=True)
    token: Mapped[str] = mapped_column(String(1000), nullable=True)

    user_id: Mapped[int]


class DataExport(Base):
    __tablename__ = "dataexport"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(server_default="true")
    export_type: Mapped[str] = mapped_column(String(1000))
    export_data: Mapped[str] = mapped_column(String(1000))
    local_path: Mapped[str] = mapped_column(String(1000))
    remote_path: Mapped[str] = mapped_column(String(1000))
    credentials_id: Mapped[int]
    user_id: Mapped[int]

    export_entries: Mapped[bool] = mapped_column(server_default="true")
    export_entries_bookmarks: Mapped[bool] = mapped_column(server_default="false")
    export_entries_permanents: Mapped[bool] = mapped_column(server_default="false")
    export_sources: Mapped[bool] = mapped_column(server_default="false")
    export_keywords: Mapped[bool] = mapped_column(server_default="false")
    format_json: Mapped[bool] = mapped_column(server_default="true")
    format_md: Mapped[bool] = mapped_column(server_default="false")
    format_rss: Mapped[bool] = mapped_column(server_default="false")
    format_html: Mapped[bool] = mapped_column(server_default="false")

    format_sources_opml: Mapped[bool] = mapped_column(server_default="false")
    output_zip: Mapped[bool] = mapped_column(server_default="false")
    output_sqlite: Mapped[bool] = mapped_column(server_default="false")


class Domains(Base):
    __tablename__ = "domains"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(1000))
    main: Mapped[str] = mapped_column(String(200))
    subdomain: Mapped[str] = mapped_column(String(200))
    suffix: Mapped[str] = mapped_column(String(200))
    tld: Mapped[str] = mapped_column(String(200))


class EntryRules(Base):
    __tablename__ = "entryrules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(server_default="true")
    priority: Mapped[int] = mapped_column(server_default="0")
    rule_name: Mapped[str] = mapped_column(String(1000))
    trigger_rule_url: Mapped[str] = mapped_column(String(1000))
    trigger_text: Mapped[str] = mapped_column(String(1000))
    trigger_text_hits: Mapped[int] = mapped_column(server_default="0")
    trigger_text_fields: Mapped[str] = mapped_column(String(1000))
    block: Mapped[bool] = mapped_column(server_default="false")
    trust: Mapped[bool] = mapped_column(server_default="false")
    auto_tag: Mapped[str] = mapped_column(String(1000))
    apply_age_limit: Mapped[int] = mapped_column(server_default="0")
    script: Mapped[str] = mapped_column(String(1000), server_default="''")
    browser_id: Mapped[int] = mapped_column(server_default="0")


class Gateway(Base):
    __tablename__ = "gateway"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(1000))
    title: Mapped[Optional[str]] = mapped_column(String(1000), server_default="")
    description: Mapped[Optional[str]] = mapped_column(String(1000), server_default="")
    gateway_type: Mapped[Optional[str]] = mapped_column(String(1000), server_default="")


class Keywords(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(String(200), unique=True)
    language: Mapped[str] = mapped_column(String(10))
    user_id: Mapped[int]


class LinkDataModel(Base):
    __tablename__ = "linkdatamodel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(30), unique=True)
    source_url: Mapped[Optional[str]]

    title: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    thumbnail: Mapped[Optional[str]]
    language: Mapped[Optional[str]]
    age: Mapped[int] = mapped_column(default=0)

    date_created = mapped_column(DateTime(timezone=True), nullable=True)
    date_published = mapped_column(DateTime(timezone=True), nullable=True)
    date_update_last = mapped_column(DateTime(timezone=True), nullable=True)
    date_dead_since = mapped_column(DateTime(timezone=True), nullable=True)
    date_last_modified = mapped_column(DateTime(timezone=True), nullable=True)

    bookmarked: Mapped[bool] = mapped_column(default=False)
    permanent: Mapped[bool] = mapped_column(default=False)

    author: Mapped[Optional[str]]
    album: Mapped[Optional[str]]

    status_code: Mapped[int] = mapped_column(default=0)
    manual_status_code: Mapped[int] = mapped_column(default=0)
    contents_type: Mapped[int] = mapped_column(default=0)

    page_rating_contents: Mapped[int] = mapped_column(default=0)
    page_rating_votes: Mapped[int] = mapped_column(default=0)
    page_rating_visits: Mapped[int] = mapped_column(default=0)
    page_rating: Mapped[int] = mapped_column(default=0)

    contents_hash: Mapped[bytes | None] = mapped_column(LargeBinary)
    body_hash: Mapped[bytes | None] = mapped_column(LargeBinary)
    meta_hash: Mapped[bytes | None] = mapped_column(LargeBinary)

    # advanced / foreign
    source_id: Mapped[Optional[int]]


class ModelFiles(Base):
    __tablename__ = "modelfiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(2000), unique=True)
    contents: Mapped[Optional[LargeBinary]] = mapped_column(String(1000000))
    date_created = mapped_column(DateTime(timezone=True), nullable=True)


class ReadLater(Base):
    __tablename__ = "readlater"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[int]
    user_id: Mapped[Optional[int]]


class SearchView(Base):
    __tablename__ = "searchview"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), unique=True)
    default: Mapped[bool] = mapped_column(server_default="false")
    hover_text: Mapped[Optional[str]] = mapped_column(String(500))
    priority: Mapped[int] = mapped_column(server_default="0")
    filter_statement: Mapped[Optional[str]] = mapped_column(String(500))
    icon: Mapped[Optional[str]] = mapped_column(String(500))
    order_by: Mapped[Optional[str]] = mapped_column(String(500))
    entry_limit: Mapped[int] = mapped_column(server_default="0")
    auto_fetch: Mapped[bool] = mapped_column(server_default="false")
    date_published_day_limit: Mapped[int] = mapped_column(server_default="0")
    date_created_day_limit: Mapped[int] = mapped_column(server_default="0")
    user: Mapped[bool] = mapped_column(server_default="false")


class SocialData(Base):
    __tablename__ = "socialdata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[Optional[int]] = mapped_column()
    thumbs_up: Mapped[Optional[int]] = mapped_column(server_default="0")
    thumbs_down: Mapped[Optional[int]] = mapped_column(server_default="0")
    view_count: Mapped[Optional[int]] = mapped_column(server_default="0")
    rating: Mapped[Optional[int]] = mapped_column(server_default="0")
    upvote_ratio: Mapped[Optional[int]] = mapped_column(server_default="0")
    upvote_diff: Mapped[Optional[int]] = mapped_column(server_default="0")
    upvote_view_ratio: Mapped[Optional[int]] = mapped_column(server_default="0")
    stars: Mapped[Optional[int]] = mapped_column(server_default="0")
    followers_count: Mapped[Optional[int]] = mapped_column(server_default="0")
    date_updated: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class SourcesTable(Base):
    __tablename__ = "sourcedatamodel"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    url: Mapped[str] = mapped_column(unique=True)
    title: Mapped[Optional[str]]
    age: Mapped[int] = mapped_column(default=0)
    category_id: Mapped[Optional[int]]
    subcategory_id: Mapped[Optional[int]]
    export_to_cms: Mapped[bool] = mapped_column(default=True)
    favicon: Mapped[Optional[str]]
    fetch_period: Mapped[Optional[int]]
    language: Mapped[Optional[str]]
    remove_after_days: Mapped[Optional[int]]
    source_type: Mapped[Optional[str]]
    category_name: Mapped[Optional[str]]
    subcategory_name: Mapped[Optional[str]]
    auto_tag: Mapped[str] = mapped_column(String(1000), default="")
    entries_backgroundcolor_alpha: Mapped[float] = mapped_column(default=0.0)
    entries_backgroundcolor: Mapped[Optional[str]]
    entries_alpha: Mapped[float] = mapped_column(default=0.0)
    xpath: Mapped[Optional[str]]
    proxy_location: Mapped[Optional[str]]
    auto_update_favicon: Mapped[bool] = mapped_column(default=True)
    credentials_id: Mapped[Optional[int]] = mapped_column()
    category_id: Mapped[Optional[int]] = mapped_column()
    subcategory_id: Mapped[Optional[int]] = mapped_column()


class SourceOperationalData(Base):
    __tablename__ = "sourceoperationaldata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    date_fetched = mapped_column(DateTime, nullable=True)
    import_seconds: Mapped[Optional[int]]
    number_of_entries: Mapped[Optional[int]]
    page_hash: Mapped[bytes | None] = mapped_column(LargeBinary)
    body_hash: Mapped[bytes | None] = mapped_column(LargeBinary)
    consecutive_errors: Mapped[Optional[int]]

    source_id: Mapped[int]


class EntryCompactedTags(Base):
    __tablename__ = "entrycompactedtags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(String(1000))
    entry_id: Mapped[Optional[int]]


class CompactedTags(Base):
    __tablename__ = "compactedtags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tag: Mapped[str] = mapped_column(String(1000))
    count: Mapped[int] = mapped_column(server_default="0")


class UserTags(Base):
    __tablename__ = "usertags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date = mapped_column(DateTime)
    tag: Mapped[str] = mapped_column(String(1000))

    entry_id: Mapped[Optional[int]]
    user_id: Mapped[Optional[int]]


class UserBookmarks(Base):
    __tablename__ = "userbookmarks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    date_bookmarked = mapped_column(DateTime)

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


class UserVotes(Base):
    __tablename__ = "uservotes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user: Mapped[str] = mapped_column(String(1000))
    vote: Mapped[int] = mapped_column(default=0)

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


class UserSearchHistory(Base):
    __tablename__ = "usersearchhistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    search_query: Mapped[str] = mapped_column(String(500))
    date = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column()


class UserEntryTransitionHistory(Base):
    __tablename__ = "userentrytransitionhistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    counter: Mapped[Optional[int]] = mapped_column()
    user: Mapped[Optional[int]] = mapped_column()
    entry_from_id: Mapped[Optional[int]] = mapped_column()
    entry_to_id: Mapped[Optional[int]] = mapped_column()


class UserEntryVisitHistory(Base):
    __tablename__ = "userentryvisithistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visits: Mapped[Optional[int]] = mapped_column()
    date_last_visit = mapped_column(DateTime(timezone=True), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column()
    entry_id: Mapped[Optional[int]] = mapped_column()


class SearchHistory(Base):
    __tablename__ = "searchhistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    search_query: Mapped[str] = mapped_column(String(500))
    date = mapped_column(DateTime(timezone=True), nullable=True)


class EntryTransitionHistory(Base):
    __tablename__ = "entrytransitionhistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    counter: Mapped[Optional[int]] = mapped_column()
    entry_from_id: Mapped[Optional[int]] = mapped_column()
    entry_to_id: Mapped[Optional[int]] = mapped_column()


class EntryVisitHistory(Base):
    __tablename__ = "entryvisithistory"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visits: Mapped[Optional[int]] = mapped_column()
    date_last_visit = mapped_column(DateTime(timezone=True), nullable=True)
    entry_id: Mapped[Optional[int]] = mapped_column()


class UserConfig(Base):
    __tablename__ = "userconfig"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(500))
    karma: Mapped[int] = mapped_column(default=0)
    birth_date = mapped_column(DateTime(timezone=True), nullable=True)

    display_style: Mapped[str] = mapped_column(default="")
    display_type: Mapped[str] = mapped_column(default="")
    show_icons: Mapped[bool] = mapped_column(default=False)
    small_icons: Mapped[bool] = mapped_column(default=False)
    thumbnails_as_icons: Mapped[bool] = mapped_column(default=False)
    entries_direct_links: Mapped[bool] = mapped_column(default=False)
    highlight_bookmarks: Mapped[bool] = mapped_column(default=False)
    click_behavior_modal_window: Mapped[bool] = mapped_column(default=False)
    links_per_page: Mapped[int] = mapped_column(default=0)
    sources_per_page: Mapped[int] = mapped_column(default=0)

    debug_mode: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[Optional[int]]


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(500))
    password: Mapped[str] = mapped_column(String(500))
    first_name: Mapped[str] = mapped_column(String(500))
    last_name: Mapped[str] = mapped_column(String(500))
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=True)
    email: Mapped[str] = mapped_column(String(500))
    date_joined = mapped_column(DateTime(timezone=True), nullable=True)


def create_tables(engine):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
