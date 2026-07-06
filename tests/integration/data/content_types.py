"""
Content-type schema payload factories.

Faithful Python ports of the JavaScript CMA SDK sanity-suite schemas
(test/sanity-check/mock/content-types/index.js). These deliberately exercise the
full range of field types — text, multiline, number, boolean, isodate, file, link,
select (dropdown/checkbox), group (nested + repeatable), reference (single + multi),
JSON RTE, HTML RTE, and modular blocks (with deeply nested groups) — because that is
where production serialization/round-trip bugs surface.

Each factory returns a deep copy so tests may mutate freely. Canonical UIDs are used
(the stack is created fresh per run); pass `uid`/`title` to override, e.g. for
duplicate-UID negative tests.
"""

import copy

# ---------------------------------------------------------------------------
# Reusable field fragments
# ---------------------------------------------------------------------------
_TITLE = {
    "display_name": "Title", "uid": "title", "data_type": "text",
    "mandatory": True, "unique": True,
    "field_metadata": {"_default": True, "version": 3},
    "multiple": False, "non_localizable": False,
}
_URL = {
    "display_name": "URL", "uid": "url", "data_type": "text", "mandatory": False,
    "field_metadata": {"_default": True, "version": 3},
    "multiple": False, "non_localizable": False, "unique": False,
}
_FILE = lambda name, uid: {  # noqa: E731
    "display_name": name, "uid": uid, "data_type": "file", "mandatory": False,
    "field_metadata": {"description": "", "rich_text_type": "standard", "image": True},
    "multiple": False, "non_localizable": False, "unique": False,
    "dimension": {"width": {"min": None, "max": None}, "height": {"min": None, "max": None}},
}
_LINK = lambda name, uid: {  # noqa: E731
    "display_name": name, "uid": uid, "data_type": "link", "mandatory": False,
    "field_metadata": {"description": "", "default_value": {"title": "", "url": ""}},
    "multiple": False, "non_localizable": False, "unique": False,
}
_JSON_RTE = lambda name, uid, embed=True: {  # noqa: E731
    "display_name": name, "uid": uid, "data_type": "json", "mandatory": False,
    "field_metadata": {
        "allow_json_rte": True, "embed_entry": embed, "description": "",
        "default_value": "", "multiline": False, "rich_text_type": "advanced", "options": [],
    },
    "format": "", "error_messages": {"format": ""}, "reference_to": ["sys_assets"],
    "multiple": False, "non_localizable": False, "unique": False,
}


# ---------------------------------------------------------------------------
# SIMPLE — basic CRUD
# ---------------------------------------------------------------------------
_SIMPLE = {
    "content_type": {
        "title": "Simple Test", "uid": "simple_test",
        "description": "Simple content type for basic CRUD operations",
        "options": {"is_page": False, "singleton": False, "title": "title", "sub_title": []},
        "schema": [
            copy.deepcopy(_TITLE),
            {
                "display_name": "Description", "uid": "description", "data_type": "text",
                "mandatory": False,
                "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
                "multiple": False, "non_localizable": False, "unique": False,
            },
        ],
    }
}

# ---------------------------------------------------------------------------
# MEDIUM — all basic field types
# ---------------------------------------------------------------------------
_MEDIUM = {
    "content_type": {
        "title": "Medium Complexity", "uid": "medium_complexity",
        "description": "Medium complexity content type for field type testing",
        "options": {
            "is_page": True, "singleton": False, "title": "title", "sub_title": [],
            "url_pattern": "/:title", "url_prefix": "/test/",
        },
        "schema": [
            copy.deepcopy(_TITLE),
            copy.deepcopy(_URL),
            {
                "display_name": "Summary", "uid": "summary", "data_type": "text", "mandatory": False,
                "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
                "format": "", "error_messages": {"format": ""},
                "multiple": False, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "View Count", "uid": "view_count", "data_type": "number", "mandatory": False,
                "field_metadata": {"description": "Number of views", "default_value": 0},
                "multiple": False, "non_localizable": False, "unique": False, "min": 0,
            },
            {
                "display_name": "Is Featured", "uid": "is_featured", "data_type": "boolean", "mandatory": False,
                "field_metadata": {"description": "Mark as featured content", "default_value": False},
                "multiple": False, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "Publish Date", "uid": "publish_date", "data_type": "isodate",
                "startDate": None, "endDate": None, "mandatory": False,
                "field_metadata": {"description": "", "default_value": {"custom": False, "date": "", "time": ""}},
                "multiple": False, "non_localizable": False, "unique": False,
            },
            _FILE("Hero Image", "hero_image"),
            _LINK("External Link", "external_link"),
            {
                "display_name": "Status", "uid": "status", "data_type": "text", "display_type": "dropdown",
                "enum": {"advanced": True, "choices": [
                    {"value": "draft", "key": "Draft"}, {"value": "review", "key": "In Review"},
                    {"value": "published", "key": "Published"}, {"value": "archived", "key": "Archived"}]},
                "mandatory": False,
                "field_metadata": {"description": "", "default_value": "draft", "default_key": "Draft", "version": 3},
                "multiple": False, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "Categories", "uid": "categories", "data_type": "text", "display_type": "checkbox",
                "enum": {"advanced": True, "choices": [
                    {"value": "technology", "key": "Technology"}, {"value": "business", "key": "Business"},
                    {"value": "lifestyle", "key": "Lifestyle"}, {"value": "science", "key": "Science"}]},
                "mandatory": False,
                "field_metadata": {"description": "", "default_value": "", "default_key": "", "version": 3},
                "multiple": True, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "Tags", "uid": "content_tags", "data_type": "text", "mandatory": False,
                "field_metadata": {"description": "Content tags", "default_value": "", "version": 3},
                "format": "", "error_messages": {"format": ""},
                "multiple": True, "non_localizable": False, "unique": False,
            },
        ],
    }
}

# ---------------------------------------------------------------------------
# COMPLEX — page builder with groups + modular blocks + JSON/HTML RTE
# ---------------------------------------------------------------------------
_COMPLEX = {
    "content_type": {
        "title": "Complex Page", "uid": "complex_page",
        "description": "Complex page builder content type with deep nesting",
        "options": {
            "is_page": True, "singleton": False, "title": "title", "sub_title": [],
            "url_pattern": "/:title", "url_prefix": "/",
        },
        "schema": [
            copy.deepcopy(_TITLE),
            copy.deepcopy(_URL),
            {
                "display_name": "Body HTML", "uid": "body_html", "data_type": "text", "mandatory": False,
                "field_metadata": {
                    "allow_rich_text": True, "description": "", "multiline": False,
                    "rich_text_type": "advanced", "options": [], "embed_entry": True, "version": 3},
                "multiple": False, "non_localizable": False, "unique": False,
            },
            _JSON_RTE("Content", "content_json_rte", embed=True),
            {
                "display_name": "SEO", "uid": "seo", "data_type": "group", "mandatory": False,
                "field_metadata": {"description": "SEO metadata", "instruction": ""},
                "schema": [
                    {"display_name": "Meta Title", "uid": "meta_title", "data_type": "text", "mandatory": False,
                     "field_metadata": {"description": "", "default_value": "", "version": 3},
                     "format": "", "error_messages": {"format": ""},
                     "multiple": False, "non_localizable": False, "unique": False},
                    {"display_name": "Meta Description", "uid": "meta_description", "data_type": "text", "mandatory": False,
                     "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
                     "format": "", "error_messages": {"format": ""},
                     "multiple": False, "non_localizable": False, "unique": False},
                    _FILE("Social Image", "social_image"),
                    {"display_name": "Canonical URL", "uid": "canonical", "data_type": "text", "mandatory": False,
                     "field_metadata": {"description": "", "default_value": "", "version": 3},
                     "format": "", "error_messages": {"format": ""},
                     "multiple": False, "non_localizable": False, "unique": False},
                ],
                "multiple": False, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "Links", "uid": "links", "data_type": "group", "mandatory": False,
                "field_metadata": {"description": "Page links", "instruction": ""},
                "schema": [
                    {**_LINK("Link", "link"),
                     "field_metadata": {"description": "", "default_value": {"title": "", "url": ""}, "isTitle": True}},
                    {"display_name": "Appearance", "uid": "appearance", "data_type": "text", "display_type": "dropdown",
                     "enum": {"advanced": True, "choices": [
                         {"value": "default", "key": "Default"}, {"value": "primary", "key": "Primary"},
                         {"value": "secondary", "key": "Secondary"}]},
                     "mandatory": False,
                     "field_metadata": {"description": "", "default_value": "default", "default_key": "Default", "version": 3},
                     "multiple": False, "non_localizable": False, "unique": False},
                    {"display_name": "Open in New Tab", "uid": "new_tab", "data_type": "boolean", "mandatory": False,
                     "field_metadata": {"description": "", "default_value": False},
                     "multiple": False, "non_localizable": False, "unique": False},
                ],
                "multiple": True, "non_localizable": False, "unique": False,
            },
            {
                "display_name": "Sections", "uid": "sections", "data_type": "blocks", "mandatory": False,
                "field_metadata": {"instruction": "", "description": "Page sections"},
                "multiple": True, "non_localizable": False, "unique": False,
                "blocks": [
                    {"title": "Hero Section", "uid": "hero_section", "schema": [
                        {"display_name": "Headline", "uid": "headline", "data_type": "text", "mandatory": True,
                         "field_metadata": {"description": "", "default_value": "", "version": 3},
                         "format": "", "error_messages": {"format": ""},
                         "multiple": False, "non_localizable": False, "unique": False},
                        {"display_name": "Subheadline", "uid": "subheadline", "data_type": "text", "mandatory": False,
                         "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
                         "format": "", "error_messages": {"format": ""},
                         "multiple": False, "non_localizable": False, "unique": False},
                        _FILE("Background Image", "background_image"),
                        _LINK("CTA Link", "cta_link"),
                    ]},
                    {"title": "Content Block", "uid": "content_block", "schema": [
                        {"display_name": "Title", "uid": "title", "data_type": "text", "mandatory": False,
                         "field_metadata": {"description": "", "default_value": "", "version": 3},
                         "format": "", "error_messages": {"format": ""},
                         "multiple": False, "non_localizable": False, "unique": False},
                        _JSON_RTE("Content", "content", embed=False),
                        _FILE("Image", "image"),
                        {"display_name": "Layout", "uid": "layout", "data_type": "text", "display_type": "dropdown",
                         "enum": {"advanced": True, "choices": [
                             {"value": "full_width", "key": "Full Width"}, {"value": "two_column", "key": "Two Column"},
                             {"value": "sidebar_left", "key": "Sidebar Left"}, {"value": "sidebar_right", "key": "Sidebar Right"}]},
                         "mandatory": False,
                         "field_metadata": {"description": "", "default_value": "full_width", "default_key": "Full Width", "version": 3},
                         "multiple": False, "non_localizable": False, "unique": False},
                    ]},
                    {"title": "Card Grid", "uid": "card_grid", "schema": [
                        {"display_name": "Grid Title", "uid": "grid_title", "data_type": "text", "mandatory": False,
                         "field_metadata": {"description": "", "default_value": "", "version": 3},
                         "format": "", "error_messages": {"format": ""},
                         "multiple": False, "non_localizable": False, "unique": False},
                        {"display_name": "Columns", "uid": "columns", "data_type": "text", "display_type": "dropdown",
                         "enum": {"advanced": False, "choices": [{"value": "2"}, {"value": "3"}, {"value": "4"}]},
                         "mandatory": False,
                         "field_metadata": {"description": "", "default_value": "3", "version": 3},
                         "multiple": False, "non_localizable": False, "unique": False},
                        {"display_name": "Cards", "uid": "cards", "data_type": "group", "mandatory": False,
                         "field_metadata": {"description": "", "instruction": ""},
                         "schema": [
                             {"display_name": "Card Title", "uid": "card_title", "data_type": "text", "mandatory": True,
                              "field_metadata": {"description": "", "default_value": "", "isTitle": True, "version": 3},
                              "format": "", "error_messages": {"format": ""},
                              "multiple": False, "non_localizable": False, "unique": False},
                             _FILE("Card Image", "card_image"),
                             _LINK("Card Link", "card_link"),
                             {"display_name": "Card Description", "uid": "card_description", "data_type": "text", "mandatory": False,
                              "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
                              "format": "", "error_messages": {"format": ""},
                              "multiple": False, "non_localizable": False, "unique": False},
                         ],
                         "multiple": True, "non_localizable": False, "unique": False},
                    ]},
                    {"title": "Accordion", "uid": "accordion", "schema": [
                        {"display_name": "Accordion Items", "uid": "items", "data_type": "group", "mandatory": False,
                         "field_metadata": {"description": "", "instruction": ""},
                         "schema": [
                             {"display_name": "Question", "uid": "question", "data_type": "text", "mandatory": True,
                              "field_metadata": {"description": "", "default_value": "", "isTitle": True, "version": 3},
                              "format": "", "error_messages": {"format": ""},
                              "multiple": False, "non_localizable": False, "unique": False},
                             _JSON_RTE("Answer", "answer", embed=False),
                         ],
                         "multiple": True, "non_localizable": False, "unique": False},
                    ]},
                ],
            },
        ],
    }
}

# ---------------------------------------------------------------------------
# AUTHOR — for reference targets
# ---------------------------------------------------------------------------
_AUTHOR = {
    "content_type": {
        "title": "Author", "uid": "author",
        "description": "Author profile for reference testing",
        "options": {"is_page": True, "singleton": False, "title": "title", "sub_title": [],
                    "url_pattern": "/:title", "url_prefix": "/authors/"},
        "schema": [
            {**copy.deepcopy(_TITLE), "display_name": "Name"},
            copy.deepcopy(_URL),
            {"display_name": "Email", "uid": "email", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": False, "unique": True},
            {"display_name": "Job Title", "uid": "job_title", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Bio", "uid": "bio", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": False, "unique": False},
            _FILE("Profile Image", "profile_image"),
            {"display_name": "Social Links", "uid": "social_links", "data_type": "group", "mandatory": False,
             "field_metadata": {"description": "", "instruction": ""},
             "schema": [
                 {"display_name": "Platform", "uid": "platform", "data_type": "text", "display_type": "dropdown",
                  "enum": {"advanced": True, "choices": [
                      {"value": "twitter", "key": "Twitter"}, {"value": "linkedin", "key": "LinkedIn"},
                      {"value": "github", "key": "GitHub"}]},
                  "mandatory": False,
                  "field_metadata": {"description": "", "default_value": "", "default_key": "", "version": 3},
                  "multiple": False, "non_localizable": False, "unique": False},
                 {**_LINK("Profile URL", "profile_url")},
             ],
             "multiple": True, "non_localizable": False, "unique": False},
        ],
    }
}

# ---------------------------------------------------------------------------
# ARTICLE — references (single + multi), isodate, JSON RTE, file, booleans
# ---------------------------------------------------------------------------
_ARTICLE = {
    "content_type": {
        "title": "Article", "uid": "article",
        "description": "Article content type with references and taxonomy",
        "options": {"is_page": True, "singleton": False, "title": "title", "sub_title": [],
                    "url_pattern": "/:title", "url_prefix": "/articles/"},
        "schema": [
            copy.deepcopy(_TITLE),
            copy.deepcopy(_URL),
            {"display_name": "Publish Date", "uid": "publish_date", "data_type": "isodate",
             "startDate": None, "endDate": None, "mandatory": False,
             "field_metadata": {"description": "", "default_value": {"custom": False, "date": "", "time": ""}, "hide_time": True},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Excerpt", "uid": "excerpt", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": False, "unique": False},
            _JSON_RTE("Content", "content", embed=True),
            _FILE("Featured Image", "featured_image"),
            {"display_name": "Author", "uid": "author", "data_type": "reference", "reference_to": ["author"],
             "mandatory": False, "field_metadata": {"ref_multiple": False, "ref_multiple_content_types": False},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Related Articles", "uid": "related_articles", "data_type": "reference",
             "reference_to": ["article"], "mandatory": False,
             "field_metadata": {"ref_multiple": True, "ref_multiple_content_types": False},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Is Featured", "uid": "is_featured", "data_type": "boolean", "mandatory": False,
             "field_metadata": {"description": "", "default_value": False},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Is Published", "uid": "is_published", "data_type": "boolean", "mandatory": False,
             "field_metadata": {"description": "", "default_value": False},
             "multiple": False, "non_localizable": True, "unique": False},
            {"display_name": "Tags", "uid": "content_tags", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": True, "non_localizable": False, "unique": False},
        ],
    }
}

# ---------------------------------------------------------------------------
# SINGLETON
# ---------------------------------------------------------------------------
_SINGLETON = {
    "content_type": {
        "title": "Site Settings", "uid": "site_settings",
        "description": "Global site settings (singleton)",
        "options": {"is_page": False, "singleton": True, "title": "title", "sub_title": []},
        "schema": [
            {**copy.deepcopy(_TITLE), "display_name": "Site Name"},
            _FILE("Site Logo", "site_logo"),
            {"display_name": "Footer Text", "uid": "footer_text", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "multiline": True, "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": False, "unique": False},
            {"display_name": "Analytics ID", "uid": "analytics_id", "data_type": "text", "mandatory": False,
             "field_metadata": {"description": "", "default_value": "", "version": 3},
             "format": "", "error_messages": {"format": ""},
             "multiple": False, "non_localizable": True, "unique": False},
        ],
    }
}

_SCHEMA_UPDATE_ADD = {
    "display_name": "New Field", "uid": "new_field", "data_type": "text", "mandatory": False,
    "field_metadata": {"description": "Newly added field", "default_value": "", "version": 3},
    "format": "", "error_messages": {"format": ""},
    "multiple": False, "non_localizable": False, "unique": False,
}


def _build(template: dict, uid: str = None, title: str = None) -> dict:
    ct = copy.deepcopy(template)
    if uid is not None:
        ct["content_type"]["uid"] = uid
    if title is not None:
        ct["content_type"]["title"] = title
    return ct


def simple_content_type(uid: str = "simple_test", title: str = None) -> dict:
    return _build(_SIMPLE, uid, title)


def medium_content_type(uid: str = "medium_complexity", title: str = None) -> dict:
    return _build(_MEDIUM, uid, title)


def complex_content_type(uid: str = "complex_page", title: str = None) -> dict:
    return _build(_COMPLEX, uid, title)


def author_content_type(uid: str = "author", title: str = None) -> dict:
    return _build(_AUTHOR, uid, title)


def article_content_type(uid: str = "article", title: str = None) -> dict:
    return _build(_ARTICLE, uid, title)


def singleton_content_type(uid: str = "site_settings", title: str = None) -> dict:
    return _build(_SINGLETON, uid, title)


def schema_update_add_field() -> dict:
    """A single extra field to append to an existing content type's schema."""
    return copy.deepcopy(_SCHEMA_UPDATE_ADD)


def invalid_content_type_missing_title(uid: str) -> dict:
    """Payload with no schema (and no title field) — for validation negatives."""
    return {"content_type": {"uid": uid, "schema": []}}
