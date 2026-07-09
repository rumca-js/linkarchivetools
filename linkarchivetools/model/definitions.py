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
    __tablename__ = "apikeys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(1000), unique=True)
    user_id: Mapped[int]


class AppLogging(Base):
    __tablename__ = "applogging"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    info_text: Mapped[str] = mapped_column(String(2000))
    detail_text: Mapped[Optional[str]] = mapped_column(String(2000))
    level: Mapped[int] = mapped_column(default=0)
    date = mapped_column(DateTime(timezone=True), nullable=True)


class BackgroundJob(Base):
    __tablename__ = "backgroundjob"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    job: Mapped[str] = mapped_column(String(1000))
    task: Mapped[Optional[str]]
    subject: Mapped[str] = mapped_column(String(1000))
    args: Mapped[Optional[str]]
    date_created = mapped_column(DateTime(timezone=True), nullable=True)

    priority: Mapped[int] = mapped_column(default=0)
    errros: Mapped[int] = mapped_column(default=0)
    enabled: Mapped[bool] = mapped_column(default=True)


class BlockEntryList(Base):
    __tablename__ = "blockentrylist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    processed: Mapped[bool] = mapped_column(default=False)


class BlockEntry(Base):
    __tablename__ = "blockentry"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(1000), unique=True)
    block_list_id: Mapped[int]


class Browser(Base):
    __tablename__ = "browser"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    name: Mapped[Optional[str]] = mapped_column(String(2000)) # name of browser, could be crawler_name
    priority: Mapped[int] = mapped_column(default=0)
    ignore_errors: Mapped[bool] = mapped_column(default=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(2000))
    request_headers: Mapped[Optional[str]] = mapped_column(String(2000))
    timeout_s: Mapped[int] = mapped_column(default=0)
    delay_s: Mapped[int] = mapped_column(default=0)
    ssl_verify: Mapped[bool] = mapped_column(default=False)
    respect_robots_txt: Mapped[bool] = mapped_column(default=False)
    accept_types: Mapped[Optional[str]] = mapped_column(String(2000))
    bytes_limit: Mapped[int] = mapped_column(default=0)
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
    logging_level: Mapped[int] = mapped_column(default=0)
    initialized: Mapped[bool] = mapped_column(default=False)
    initialization_type: Mapped[Optional[str]] = mapped_column(String(100))
    enable_background_jobs: Mapped[bool] = mapped_column(default=True)
    block_job_queue: Mapped[bool] = mapped_column(default=False)
    use_internal_scripts: Mapped[bool] = mapped_column(default=False)
    cleanup_time = mapped_column(Time(), nullable=True) # TODO /Datetime?

    data_import_path: Mapped[Optional[str]] = mapped_column(String(2000))
    data_export_path: Mapped[Optional[str]] = mapped_column(String(2000))
    download_path: Mapped[Optional[str]] = mapped_column(String(2000))
    auto_store_thumbnails: Mapped[bool] = mapped_column(default=False)
    thread_memory_threshold: Mapped[int] = mapped_column(default=0)

    enable_keyword_support: Mapped[bool] = mapped_column(default=False)
    enable_domain_support: Mapped[bool] = mapped_column(default=False)
    enable_file_support: Mapped[bool] = mapped_column(default=False)
    enable_link_archiving: Mapped[bool] = mapped_column(default=False)
    enable_source_archiving: Mapped[bool] = mapped_column(default=False)
    enable_crawling: Mapped[bool] = mapped_column(default=False)
    enable_social_data: Mapped[bool] = mapped_column(default=False)

    accept_dead_links: Mapped[bool] = mapped_column(default=False)
    accept_ip_links: Mapped[bool] = mapped_column(default=False)
    accept_domain_links: Mapped[bool] = mapped_column(default=False)
    accept_non_domain_links: Mapped[bool] = mapped_column(default=False)
    accept_unknown_links: Mapped[bool] = mapped_column(default=False)
    accept_onion_links: Mapped[bool] = mapped_column(default=False)
    accept_same_hashes: Mapped[bool] = mapped_column(default=False)

    auto_crawl_sources: Mapped[bool] = mapped_column(default=False)
    auto_scan_new_entries: Mapped[bool] = mapped_column(default=False)
    auto_scan_updated_entries: Mapped[bool] = mapped_column(default=False)
    new_entries_merge_data: Mapped[bool] = mapped_column(default=False)
    new_entries_use_clean_data: Mapped[bool] = mapped_column(default=False)
    new_entries_fetch_social_data: Mapped[bool] = mapped_column(default=False)
    browse_entries_fetch_social_data: Mapped[bool] = mapped_column(default=False)
    browse_entry_fetch_social_data: Mapped[bool] = mapped_column(default=False)
    entry_update_fetches_social_data: Mapped[bool] = mapped_column(default=False)
    entry_update_via_internet: Mapped[bool] = mapped_column(default=False)

    log_remove_entries: Mapped[bool] = mapped_column(default=False)
    auto_create_sources: Mapped[bool] = mapped_column(default=False)
    default_source_state: Mapped[bool] = mapped_column(default=False)
    prefer_https_links: Mapped[bool] = mapped_column(default=False)
    prefer_https_links: Mapped[bool] = mapped_column(default=False)
    prefer_non_www_links: Mapped[bool] = mapped_column(default=False)

    new_entries_download_music: Mapped[bool] = mapped_column(default=False)
    new_entries_download_video: Mapped[bool] = mapped_column(default=False)
    entry_update_download_music: Mapped[bool] = mapped_column(default=False)
    entry_update_download_video: Mapped[bool] = mapped_column(default=False)

    sources_refresh_period: Mapped[int] = mapped_column(default=0)
    days_to_move_to_archive: Mapped[int] = mapped_column(default=0)
    days_to_remove_links: Mapped[int] = mapped_column(default=0)
    days_to_remove_stale_entries: Mapped[int] = mapped_column(default=0)
    days_to_check_std_entries: Mapped[int] = mapped_column(default=0)
    days_to_check_stale_entries: Mapped[int] = mapped_column(default=0)
    remove_entry_vote_threshold: Mapped[int] = mapped_column(default=1)
    number_of_update_entries: Mapped[int] = mapped_column(default=1)

    remote_webtools_server_location: Mapped[Optional[str]] = mapped_column(default="")
    internet_status_test_url: Mapped[Optional[str]] = mapped_column(
        default="https://google.com"
    )

    track_user_actions: Mapped[bool] = mapped_column(default=False)
    track_user_searches: Mapped[bool] = mapped_column(default=False)
    track_user_navigation: Mapped[bool] = mapped_column(default=False)
    max_user_entry_visit_history: Mapped[int] = mapped_column(default=1)
    max_number_of_user_search: Mapped[int] = mapped_column(default=1)
    vote_min: Mapped[int] = mapped_column(default=-100)
    vote_max: Mapped[int] = mapped_column(default=-100)
    number_of_comments_per_day: Mapped[int] = mapped_column(default=-100)

    time_zone: Mapped[int] = mapped_column(default=-100)
    display_style: Mapped[int] = mapped_column(default=-100)
    display_type: Mapped[int] = mapped_column(default=-100)
    show_icons: Mapped[bool] = mapped_column(default=False)
    entry_preview: Mapped[bool] = mapped_column(default=True)            # allows to show preview to play entry
    thumbnails_as_icons: Mapped[bool] = mapped_column(default=False)
    small_icons: Mapped[bool] = mapped_column(default=False)
    local_icons: Mapped[bool] = mapped_column(default=False)
    highlight_bookmarks: Mapped[bool] = mapped_column(default=False)
    click_behavior_model_window: Mapped[bool] = mapped_column(default=False)
    links_per_page: Mapped[int] = mapped_column(default=-100)
    sources_per_page: Mapped[int] = mapped_column(default=-100)
    max_links_per_page: Mapped[int] = mapped_column(default=-100)
    max_sources_per_page: Mapped[int] = mapped_column(default=-100)
    max_number_of_related_links: Mapped[int] = mapped_column(default=-100)

    entries_visit_alpha: Mapped[float] = mapped_column(default=0.6)
    entries_dead_alpha: Mapped[float] = mapped_column(default=0.6)

    debug_mode: Mapped[bool] = mapped_column(default=False)


class DataExport(Base):
    __tablename__ = "dataexport"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    export_type: Mapped[str] = mapped_column(String(1000))
    export_data: Mapped[str] = mapped_column(String(1000))
    local_path: Mapped[str] = mapped_column(String(1000))
    remote_path: Mapped[str] = mapped_column(String(1000))
    credentials_id: Mapped[int]
    user_id: Mapped[int]

    export_entries: Mapped[bool] = mapped_column(default=True)
    export_entries_bookmarks: Mapped[bool] = mapped_column(default=False)
    export_entries_permanents: Mapped[bool] = mapped_column(default=False)
    export_sources: Mapped[bool] = mapped_column(default=False)
    export_keywords: Mapped[bool] = mapped_column(default=False)
    format_json: Mapped[bool] = mapped_column(default=True)
    format_md: Mapped[bool] = mapped_column(default=False)
    format_rss: Mapped[bool] = mapped_column(default=False)
    format_html: Mapped[bool] = mapped_column(default=False)

    format_sources_opml: Mapped[bool] = mapped_column(default=False)
    output_zip: Mapped[bool] = mapped_column(default=False)
    output_sqlite: Mapped[bool] = mapped_column(default=False)


class Gateway(Base):
    __tablename__ = "gateway"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(String(1000))
    title: Mapped[str] = mapped_column(String(1000))
    description: Mapped[str] = mapped_column(String(1000))
    gateway_type: Mapped[str] = mapped_column(String(1000))


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
    status_code: Mapped[int] = mapped_column(default=0)
    page_rating: Mapped[int] = mapped_column(default=0)
    page_rating_votes: Mapped[int] = mapped_column(default=0)
    page_rating_contents: Mapped[int] = mapped_column(default=0)
    bookmarked: Mapped[bool] = mapped_column(default=False)
    permanent: Mapped[bool] = mapped_column(default=False)
    author: Mapped[Optional[str]]
    album: Mapped[Optional[str]]
    source_url: Mapped[Optional[str]]
    contents_type: Mapped[int] = mapped_column(default=0)
    page_rating_contents: Mapped[int] = mapped_column(default=0)
    page_rating_votes: Mapped[int] = mapped_column(default=0)
    page_rating_visits: Mapped[int] = mapped_column(default=0)
    page_rating: Mapped[int] = mapped_column(default=0)
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
    user_id: Mapped[int]


class SearchView(Base):
    __tablename__ = "searchview"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(500), unique=True)
    default: Mapped[bool] = mapped_column(default=False)
    hover_text: Mapped[Optional[str]] = mapped_column(String(500))
    priority: Mapped[int] = mapped_column(default=0)
    filter_statement: Mapped[Optional[str]] = mapped_column(String(500))
    icon: Mapped[Optional[str]] = mapped_column(String(500))
    order_by: Mapped[Optional[str]] = mapped_column(String(500))
    entry_limit: Mapped[int] = mapped_column(default=0)
    auto_fetch: Mapped[bool] = mapped_column(default=False)
    date_published_day_limit: Mapped[int] = mapped_column(default=0)
    date_created_day_limit: Mapped[int] = mapped_column(default=0)
    user: Mapped[bool] = mapped_column(default=False)


class SocialData(Base):
    __tablename__ = "socialdata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    thumbs_up: Mapped[Optional[int]] = mapped_column(default=0)
    thumbs_down: Mapped[Optional[int]] = mapped_column(default=0)
    view_count: Mapped[Optional[int]] = mapped_column(default=0)
    rating: Mapped[Optional[int]] = mapped_column(default=0)
    upvote_ratio: Mapped[Optional[int]] = mapped_column(default=0)
    upvote_diff: Mapped[Optional[int]] = mapped_column(default=0)
    upvote_view_ratio: Mapped[Optional[int]] = mapped_column(default=0)
    stars: Mapped[Optional[int]] = mapped_column(default=0)
    date_updated = mapped_column(DateTime, nullable=True)


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
    proxy_location: Mapped[Optional[str]]
    remove_after_days: Mapped[Optional[int]]
    source_type: Mapped[Optional[str]]
    category_name: Mapped[Optional[str]]
    subcategory_name: Mapped[Optional[str]]
    auto_tag: Mapped[str] = mapped_column(String(1000), default="")
    auto_update_favicon: Mapped[bool] = mapped_column(default=True)


class SourceOperationalData(Base):
    __tablename__ = "sourceoperationaldata"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_fetched = mapped_column(DateTime, nullable=True)
    source: Mapped[int]


class UserTags(Base):
    __tablename__ = "usertags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date = mapped_column(DateTime)
    tag: Mapped[str] = mapped_column(String(1000))

    entry_object: Mapped[Optional[int]]
    user_object: Mapped[Optional[int]]


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


def create_tables(engine):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
