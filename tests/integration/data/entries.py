"""
Entry payload factories — faithful Python ports of the JS sanity-suite entry mocks
(test/sanity-check/mock/entries/index.js).

Covers simple/medium/complex entries (groups, modular blocks, JSON RTE), author and
article entries (references set dynamically by tests), singleton, atomic operations
(PUSH/PULL/UPDATE/ADD), localized variants, and version naming.

Each factory returns a deep copy so tests may mutate freely.
"""

import copy


def simple_entry(title: str = "Simple Test Entry", description: str = None) -> dict:
    return {"entry": {
        "title": title,
        "description": description or "This is a simple test entry for basic CRUD operations.",
    }}


def simple_entry_update() -> dict:
    return {"entry": {
        "title": "Updated Simple Entry",
        "description": "This entry has been updated with new content.",
    }}


def medium_entry(title: str = "Medium Complexity Entry") -> dict:
    return {"entry": {
        "title": title,
        "url": "/test/medium-entry",
        "summary": "This is a multi-line summary that spans multiple lines.\n\n"
                   "It contains paragraph breaks and detailed information about the content.",
        "view_count": 1250,
        "is_featured": True,
        "publish_date": "2024-01-15T00:00:00.000Z",
        "external_link": {"title": "Learn More", "href": "https://example.com/learn-more"},
        "status": "published",
        "categories": ["technology", "business"],
        "content_tags": ["sdk", "testing", "api", "python"],
    }}


def medium_entry_update() -> dict:
    return {"entry": {
        "title": "Updated Medium Entry",
        "view_count": 2500,
        "is_featured": False,
        "status": "archived",
        "content_tags": ["sdk", "testing", "api", "python", "updated"],
    }}


_COMPLEX_ENTRY = {
    "entry": {
        "title": "Complex Page Entry",
        "url": "/complex-page-entry",
        "body_html": "<h2>Welcome</h2><p>This is HTML rich text content with "
                     "<strong>bold</strong> and <em>italic</em> formatting.</p>",
        "content_json_rte": {
            "type": "doc", "uid": "doc_uid", "attrs": {}, "children": [
                {"type": "p", "attrs": {}, "uid": "p_uid_1",
                 "children": [{"text": "This is JSON RTE content with proper structure."}]},
                {"type": "h2", "attrs": {}, "uid": "h2_uid",
                 "children": [{"text": "Heading Level 2"}]},
                {"type": "p", "attrs": {}, "uid": "p_uid_2", "children": [
                    {"text": "More paragraph content with "},
                    {"text": "bold text", "bold": True},
                    {"text": " and "},
                    {"text": "italic text", "italic": True},
                    {"text": "."}]},
            ],
        },
        "seo": {
            "meta_title": "Complex Page - SEO Title",
            "meta_description": "This is the meta description for the complex page entry. "
                                "It should be between 150-160 characters for optimal SEO.",
            "canonical": "https://example.com/complex-page-entry",
        },
        "links": [
            {"link": {"title": "Primary Link", "href": "/primary"}, "appearance": "primary", "new_tab": False},
            {"link": {"title": "Secondary Link", "href": "/secondary"}, "appearance": "secondary", "new_tab": True},
            {"link": {"title": "External Link", "href": "https://external.com"}, "appearance": "default", "new_tab": True},
        ],
        "sections": [
            {"hero_section": {
                "headline": "Welcome to Our Platform",
                "subheadline": "Discover amazing features and capabilities that will transform your workflow.",
                "cta_link": {"title": "Get Started", "href": "/get-started"}}},
            {"content_block": {
                "title": "Our Features",
                "content": {"type": "doc", "uid": "feature_doc", "attrs": {}, "children": [
                    {"type": "p", "attrs": {}, "uid": "feature_p",
                     "children": [{"text": "Explore our comprehensive set of features designed for modern teams."}]}]},
                "layout": "two_column"}},
            {"card_grid": {
                "grid_title": "Featured Products", "columns": "3", "cards": [
                    {"card_title": "Product One", "card_description": "Description for product one with key features.",
                     "card_link": {"title": "Learn More", "href": "/products/one"}},
                    {"card_title": "Product Two", "card_description": "Description for product two with benefits.",
                     "card_link": {"title": "Learn More", "href": "/products/two"}},
                    {"card_title": "Product Three", "card_description": "Description for product three with details.",
                     "card_link": {"title": "Learn More", "href": "/products/three"}}]}},
            {"accordion": {"items": [
                {"question": "What is this platform?",
                 "answer": {"type": "doc", "uid": "faq_1", "attrs": {}, "children": [
                     {"type": "p", "attrs": {}, "uid": "faq_1_p",
                      "children": [{"text": "This platform is a comprehensive solution for content management."}]}]}},
                {"question": "How do I get started?",
                 "answer": {"type": "doc", "uid": "faq_2", "attrs": {}, "children": [
                     {"type": "p", "attrs": {}, "uid": "faq_2_p",
                      "children": [{"text": "Sign up for an account and follow our quick start guide."}]}]}},
            ]}},
        ],
    }
}


def complex_entry(title: str = None) -> dict:
    e = copy.deepcopy(_COMPLEX_ENTRY)
    if title:
        e["entry"]["title"] = title
    return e


def author_entry(title: str = "John Doe") -> dict:
    return {"entry": {
        "title": title,
        "url": f"/authors/{title.lower().replace(' ', '-')}",
        "email": f"{title.lower().replace(' ', '.')}@example.com",
        "job_title": "Senior Developer",
        "bio": "Seasoned developer with over 10 years of experience building scalable applications.",
        "social_links": [
            {"platform": "twitter", "profile_url": {"title": "@author", "href": "https://twitter.com/author"}},
            {"platform": "linkedin", "profile_url": {"title": title, "href": "https://linkedin.com/in/author"}},
        ],
    }}


def article_entry(title: str = "Getting Started with the SDK") -> dict:
    return {"entry": {
        "title": title,
        "url": "/articles/getting-started-sdk",
        "publish_date": "2024-01-20T00:00:00.000Z",
        "excerpt": "Learn how to integrate our SDK into your application with this comprehensive guide.",
        "content": {"type": "doc", "uid": "article_content", "attrs": {}, "children": [
            {"type": "h2", "attrs": {}, "uid": "intro_h2", "children": [{"text": "Introduction"}]},
            {"type": "p", "attrs": {}, "uid": "intro_p",
             "children": [{"text": "Welcome to our comprehensive SDK guide."}]},
        ]},
        "is_featured": True,
        "is_published": True,
        "content_tags": ["sdk", "tutorial", "getting-started", "python"],
    }}


def article_entry_with_references(author_uid: str = None, related_article_uid: str = None,
                                  title: str = "Advanced SDK Patterns") -> dict:
    """Article entry that wires up single + multi references when uids are provided."""
    entry = {
        "title": title,
        "url": "/articles/advanced-sdk-patterns",
        "publish_date": "2024-02-15T00:00:00.000Z",
        "excerpt": "Deep dive into advanced patterns and best practices for SDK integration.",
        "content": {"type": "doc", "uid": "advanced_content", "attrs": {}, "children": [
            {"type": "p", "attrs": {}, "uid": "advanced_p",
             "children": [{"text": "This article covers advanced patterns for experienced developers."}]}]},
        "is_featured": False,
        "is_published": True,
        "content_tags": ["sdk", "advanced", "patterns"],
    }
    if author_uid:
        entry["author"] = [{"uid": author_uid, "_content_type_uid": "author"}]
    if related_article_uid:
        entry["related_articles"] = [{"uid": related_article_uid, "_content_type_uid": "article"}]
    return {"entry": entry}


def site_settings_entry() -> dict:
    return {"entry": {
        "title": "My Test Site",
        "footer_text": "© 2024 My Test Site. All rights reserved.\n\nBuilt with Contentstack.",
        "analytics_id": "GA-123456789",
    }}


# ---- Atomic operations ----
def atomic_push_entry() -> dict:
    return {"entry": {"content_tags": {"PUSH": {"data": ["new-tag-1", "new-tag-2"]}}}}


def atomic_pull_entry() -> dict:
    return {"entry": {"content_tags": {"PULL": {"data": ["tag-to-remove"]}}}}


def atomic_update_entry() -> dict:
    return {"entry": {"content_tags": {"UPDATE": {"index": 0, "data": "replaced-tag"}}}}


def atomic_add_subtract() -> dict:
    return {"entry": {"view_count": {"ADD": 100}}}


def atomic_subtract() -> dict:
    return {"entry": {"view_count": {"SUB": 10}}}


def publish_config(environment: str, locale: str = "en-us") -> dict:
    return {"entry": {"environments": [environment], "locales": [locale]}}


def unpublish_config(environment: str, locale: str = "en-us") -> dict:
    return {"entry": {"environments": [environment], "locales": [locale]}}


# ---- Localized ----
def localized_entry_en_us() -> dict:
    return {"entry": {"title": "Localized Entry - English",
                      "description": "This is the English version of the content."}}


def localized_entry_fr_fr() -> dict:
    return {"entry": {"title": "Entrée localisée - Français",
                      "description": "Ceci est la version française du contenu."}}


# ---- Version naming ----
def version_name_config(name: str = "Production Release v1", locale: str = "en-us") -> dict:
    # locale is required in the body for version naming (per the SDK/API contract).
    return {"entry": {"_version_name": name, "locale": locale}}


def invalid_entry_missing_title() -> dict:
    """Entry missing the title field (note: API saves an _in_progress draft, not a 4xx)."""
    return {"entry": {"url": "/no-title"}}
