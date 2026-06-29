"""
Custom dashboard HTML report for the integration suite.

Pure Python, zero dependencies. Collects a TestRecord per test (from conftest hooks)
and renders a single self-contained HTML file at session finish.

Design goals (modelled on the JS suite's Mochawesome output, not a copy):
  - compact summary chips (no oversized cards or full-width bars)
  - human-readable test titles (from docstring, else derived from the test name),
    grouped resource -> describe-block (class) -> test
  - each test expands to show every HTTP call with method/url, a colour-coded
    status, request headers, request body, response body, and copy-ready cURL —
    each in a collapsible block like Mochawesome's context entries
  - HONEST status: a test that passed its assertions but whose HTTP calls returned
    a >=400 status is flagged amber ("passed with warnings") rather than silent green,
    so lenient/tolerant assertions can't hide a real API failure.
"""

import html
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class TestRecord:
    nodeid: str
    name: str
    resource: str
    outcome: str  # 'passed' | 'failed' | 'skipped'
    duration_ms: float
    message: str = ""
    calls: List[dict] = field(default_factory=list)
    assertions: List[dict] = field(default_factory=list)
    description: str = ""
    group: str = ""  # test class / describe block

    # Keywords/markers identifying a deliberately-negative test, where a >=400
    # response is the EXPECTED, asserted outcome (so it is not a warning).
    _NEGATIVE_MARKERS = (
        "negative", "nonexistent", "invalid", "without", "duplicate", "missing",
        "requires", "bad", "no_such", "raises", "not_found", "404",
    )

    @property
    def is_negative(self) -> bool:
        hay = f"{self.group} {self.name}".lower()
        return any(m in hay for m in self._NEGATIVE_MARKERS)

    @property
    def has_warning(self) -> bool:
        """Passed a positive test, but an HTTP call returned >= 400.

        Negative tests are excluded: for them a 4xx is the expected, asserted
        result. This flags only positive operations whose lenient assertions
        swallowed an unexpected API error (e.g. a create that returned 422).
        """
        if self.outcome != "passed" or self.is_negative:
            return False
        return any((c.get("status") or 0) >= 400 for c in self.calls)


# ---------------------------------------------------------------------------
# Title humanisation
# ---------------------------------------------------------------------------
def _humanize_test(name: str) -> str:
    n = name[5:] if name.startswith("test_") else name
    n = n.replace("_", " ").strip()
    return (n[:1].upper() + n[1:]) if n else name


def _humanize_group(cls: str) -> str:
    # 'TestContentTypeCRUD' -> 'Content Type CRUD'
    s = cls[4:] if cls.startswith("Test") else cls
    out, prev_lower = [], False
    for i, ch in enumerate(s):
        if ch.isupper() and prev_lower:
            out.append(" ")
        out.append(ch)
        prev_lower = ch.islower()
    return "".join(out).strip()


def _region_from_host(host: str) -> str:
    if not host:
        return "NA"
    head = host.split("-api")[0] if "-api" in host else ""
    return head.upper() if head and head != "api" else "NA"


def _esc(text) -> str:
    return html.escape(str(text)) if text is not None else ""


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
def render(records: List[TestRecord], output_path: str, started_at: float, ended_at: float) -> str:
    total = len(records)
    passed = sum(1 for r in records if r.outcome == "passed")
    failed = sum(1 for r in records if r.outcome == "failed")
    skipped = sum(1 for r in records if r.outcome == "skipped")
    xfailed = sum(1 for r in records if r.outcome == "xfailed")
    xpassed = sum(1 for r in records if r.outcome == "xpassed")
    warnings = sum(1 for r in records if r.has_warning) + xpassed
    pass_rate = round((passed / total) * 100, 1) if total else 0.0
    duration_s = round(ended_at - started_at, 1)
    host = os.getenv("HOST", "")
    region = _region_from_host(host)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Group: resource -> [records]
    by_resource: dict = {}
    for r in records:
        by_resource.setdefault(r.resource, []).append(r)

    # Coverage chips (compact).
    cov = []
    for resource in sorted(by_resource):
        items = by_resource[resource]
        p = sum(1 for r in items if r.outcome == "passed")
        f = sum(1 for r in items if r.outcome == "failed")
        w = sum(1 for r in items if r.has_warning)
        cls = "ok" if f == 0 else "bad"
        warn = f' <span class="cov-warn">⚠{w}</span>' if w else ""
        cov.append(
            f'<div class="cov {cls}"><span class="cov-r">{_esc(resource)}</span>'
            f'<span class="cov-n">{p}/{len(items)}</span>{warn}</div>'
        )

    # Sections: failing/warning resources first.
    def sort_key(resource):
        items = by_resource[resource]
        rank = 0 if any(r.outcome == "failed" for r in items) else (1 if any(r.has_warning for r in items) else 2)
        return (rank, resource)

    sections = []
    for resource in sorted(by_resource, key=sort_key):
        sections.append(_render_resource(resource, by_resource[resource]))

    document = _TEMPLATE.format(
        total=total, passed=passed, failed=failed, skipped=skipped, warnings=warnings,
        xfailed=xfailed, pass_rate=pass_rate, duration=duration_s, region=_esc(region),
        host=_esc(host or "n/a"), timestamp=timestamp,
        coverage="".join(cov), sections="".join(sections) or "<p>No tests recorded.</p>",
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(document)
    return output_path


def _render_resource(resource: str, items: List[TestRecord]) -> str:
    p = sum(1 for r in items if r.outcome == "passed")
    f = sum(1 for r in items if r.outcome == "failed")
    w = sum(1 for r in items if r.has_warning)
    s = sum(1 for r in items if r.outcome == "skipped")

    badges = f'<span class="b ok">{p} passed</span>'
    if f:
        badges += f'<span class="b bad">{f} failed</span>'
    if w:
        badges += f'<span class="b warn">{w} warning</span>'
    if s:
        badges += f'<span class="b skip">{s} skipped</span>'

    # Group by class within resource.
    by_group: dict = {}
    for r in items:
        by_group.setdefault(r.group or "", []).append(r)

    body = []
    for group in by_group:
        if group:
            body.append(f'<div class="grp">{_esc(_humanize_group(group))}</div>')
        for r in by_group[group]:
            body.append(_render_test(r))

    open_attr = " open" if (f or w) else ""
    return (
        f'<details class="resource"{open_attr}><summary>'
        f'<span class="res-name">{_esc(resource)}</span>'
        f'<span class="res-badges">{badges}</span></summary>'
        f'<div class="res-body">{"".join(body)}</div></details>'
    )


def _render_test(r: TestRecord) -> str:
    if r.outcome == "failed":
        icon, cls = "✗", "failed"
    elif r.outcome == "skipped":
        icon, cls = "⊘", "skipped"
    elif r.outcome == "xfailed":
        icon, cls = "▲", "xfailed"
    elif r.outcome == "xpassed":
        icon, cls = "▲", "warning"
    elif r.has_warning:
        icon, cls = "⚠", "warning"
    else:
        icon, cls = "✓", "passed"

    title = r.description or _humanize_test(r.name)
    warn_note = ""
    if r.outcome == "xfailed":
        warn_note = '<span class="tnote">known issue (expected failure)</span>'
    elif r.outcome == "xpassed":
        warn_note = '<span class="tnote">known issue now PASSES — review xfail marker</span>'
    elif r.has_warning:
        codes = sorted({c.get("status") for c in r.calls if (c.get("status") or 0) >= 400})
        warn_note = f'<span class="tnote">passed, but API returned {", ".join(map(str, codes))}</span>'

    parts = [f'<div class="test-meta">{_esc(r.name)}</div>']
    if r.message:
        parts.append(f'<div class="blk"><div class="blk-h">Message</div><pre class="msg">{_esc(r.message)}</pre></div>')
    if r.assertions:
        parts.append(_render_assertions(r.assertions))
    if r.calls:
        parts.append(f'<div class="blk"><div class="blk-h">HTTP calls ({len(r.calls)})</div>'
                     + "".join(_render_call(c) for c in r.calls) + "</div>")

    open_attr = " open" if r.outcome in ("failed", "xpassed") or r.has_warning else ""
    return (
        f'<details class="test {cls}"{open_attr}><summary>'
        f'<span class="ico">{icon}</span><span class="ttitle">{_esc(title)}</span>'
        f'{warn_note}<span class="tdur">{int(r.duration_ms)} ms</span></summary>'
        f'<div class="test-body">{"".join(parts)}</div></details>'
    )


def _render_assertions(assertions: List[dict]) -> str:
    rows = "".join(
        f'<tr class="{"ok" if a.get("passed") else "bad"}"><td>{"✓" if a.get("passed") else "✗"}</td>'
        f'<td>{_esc(a.get("description"))}</td><td>{_esc(a.get("expected"))}</td>'
        f'<td>{_esc(a.get("actual"))}</td></tr>'
        for a in assertions
    )
    return (
        '<div class="blk"><div class="blk-h">Assertions</div>'
        '<table class="assert"><thead><tr><th></th><th>Check</th><th>Expected</th><th>Actual</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>'
    )


def _render_call(c: dict) -> str:
    status = c.get("status")
    if status is None:
        scls, slabel = "sx", (c.get("error") or "—")
    elif 200 <= status < 300:
        scls, slabel = "s2", status
    elif 300 <= status < 400:
        scls, slabel = "s3", status
    else:
        scls, slabel = "s4", status

    method = c.get("method", "")
    mcls = {"GET": "m-get", "POST": "m-post", "PUT": "m-put", "DELETE": "m-del"}.get(method, "m-get")

    blocks = []
    rh = c.get("request_headers") or {}
    if rh:
        hdr = "\n".join(f"{k}: {v}" for k, v in rh.items())
        blocks.append(_sub("Request headers", hdr))
    rb = c.get("request_body")
    if rb:
        blocks.append(_sub("Request body", rb))
    elif c.get("has_files"):
        blocks.append(_sub("Request body", "(multipart file upload)"))
    elif method in ("POST", "PUT"):
        blocks.append(_sub("Request body", "(empty)"))
    resp = c.get("response_body")
    blocks.append(_sub("Response body", resp if resp not in (None, "") else "(empty)"))
    if c.get("curl"):
        blocks.append(_sub("cURL", c.get("curl"), mono=True, open_=False))

    sdk = c.get("sdk_method", "")
    dur = c.get("duration_ms")
    return (
        '<div class="call">'
        '<div class="call-head">'
        f'<span class="method {mcls}">{_esc(method)}</span>'
        f'<span class="url">{_esc(c.get("url"))}</span>'
        f'<span class="status {scls}">{_esc(slabel)}</span>'
        f'<span class="cdur">{_esc(dur)} ms</span></div>'
        f'<div class="sdk">{_esc(sdk)}</div>'
        f'{"".join(blocks)}</div>'
    )


def _sub(label: str, content: str, mono: bool = True, open_: bool = False) -> str:
    o = " open" if open_ else ""
    pre_cls = "mono" if mono else ""
    return (f'<details class="sub"{o}><summary>{_esc(label)}</summary>'
            f'<pre class="{pre_cls}">{_esc(content)}</pre></details>')


_TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CMA Python SDK — Integration Report</title>
<style>
  :root {{
    --bg:#0d1117; --panel:#161b22; --panel2:#0b0f14; --line:#21262d; --txt:#e6edf3;
    --muted:#8b949e; --pass:#3fb950; --fail:#f85149; --warn:#d29922; --skip:#6e7681; --accent:#58a6ff;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--txt);
    font:13.5px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  .top {{ padding:18px 28px; border-bottom:1px solid var(--line); display:flex;
    align-items:baseline; justify-content:space-between; flex-wrap:wrap; gap:8px; }}
  .top h1 {{ margin:0; font-size:17px; font-weight:650; }}
  .top .meta {{ color:var(--muted); font-size:12.5px; }}
  .top .meta b {{ color:var(--txt); }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:20px 28px 60px; }}

  /* Summary chips */
  .chips {{ display:flex; gap:10px; flex-wrap:wrap; margin-bottom:22px; }}
  .chip {{ background:var(--panel); border:1px solid var(--line); border-radius:8px;
    padding:8px 14px; display:flex; align-items:baseline; gap:8px; }}
  .chip .v {{ font-size:18px; font-weight:700; }}
  .chip .k {{ color:var(--muted); font-size:11.5px; text-transform:uppercase; letter-spacing:.4px; }}
  .chip.pass .v {{ color:var(--pass); }} .chip.fail .v {{ color:var(--fail); }}
  .chip.warn .v {{ color:var(--warn); }} .chip.skip .v {{ color:var(--skip); }}
  .chip.xfail .v {{ color:#a371f7; }}
  .chip.rate .v {{ color:var(--accent); }}

  h2 {{ font-size:11.5px; text-transform:uppercase; letter-spacing:.5px; color:var(--muted);
    margin:24px 0 10px; }}

  /* Coverage — compact wrapping chips */
  .cov-wrap {{ display:flex; flex-wrap:wrap; gap:6px; }}
  .cov {{ display:flex; align-items:center; gap:6px; background:var(--panel);
    border:1px solid var(--line); border-radius:6px; padding:4px 9px; font-size:12px; }}
  .cov.ok {{ border-left:2px solid var(--pass); }}
  .cov.bad {{ border-left:2px solid var(--fail); }}
  .cov-r {{ color:var(--txt); }}
  .cov-n {{ color:var(--muted); }}
  .cov-warn {{ color:var(--warn); font-size:11px; }}

  /* Resource sections */
  details.resource {{ background:var(--panel); border:1px solid var(--line);
    border-radius:9px; margin:9px 0; overflow:hidden; }}
  details.resource > summary {{ cursor:pointer; padding:11px 15px; display:flex;
    justify-content:space-between; align-items:center; font-weight:600; list-style:none; }}
  details.resource > summary::-webkit-details-marker {{ display:none; }}
  .res-name {{ font-size:14px; }}
  .res-badges {{ display:flex; gap:6px; }}
  .b {{ font-size:11px; padding:2px 8px; border-radius:10px; font-weight:600; }}
  .b.ok {{ background:rgba(63,185,80,.14); color:var(--pass); }}
  .b.bad {{ background:rgba(248,81,73,.14); color:var(--fail); }}
  .b.warn {{ background:rgba(210,153,34,.16); color:var(--warn); }}
  .b.skip {{ background:rgba(110,118,129,.18); color:var(--skip); }}
  .res-body {{ border-top:1px solid var(--line); padding:4px 12px 10px; }}
  .grp {{ color:var(--muted); font-size:11px; text-transform:uppercase; letter-spacing:.5px;
    margin:12px 4px 4px; }}

  /* Test rows */
  details.test {{ border-top:1px solid var(--line); }}
  details.test:first-child {{ border-top:none; }}
  details.test > summary {{ cursor:pointer; padding:8px 4px; display:flex; align-items:center;
    gap:10px; list-style:none; }}
  details.test > summary::-webkit-details-marker {{ display:none; }}
  .ico {{ width:16px; text-align:center; font-weight:700; }}
  .test.passed .ico {{ color:var(--pass); }} .test.failed .ico {{ color:var(--fail); }}
  .test.warning .ico {{ color:var(--warn); }} .test.skipped .ico {{ color:var(--skip); }}
  .test.xfailed .ico {{ color:#a371f7; }} .test.xfailed .ttitle {{ color:#a371f7; }}
  .ttitle {{ flex:1; }}
  .test.warning .ttitle {{ color:var(--warn); }}
  .tnote {{ color:var(--warn); font-size:11px; font-style:italic; margin-right:8px; }}
  .tdur {{ color:var(--muted); font-size:11.5px; }}
  .test-body {{ padding:4px 0 12px 26px; }}
  .test-meta {{ color:var(--muted); font-size:11px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; margin-bottom:8px; }}

  .blk {{ margin:10px 0; }}
  .blk-h {{ font-size:11px; text-transform:uppercase; color:var(--muted); margin-bottom:5px; letter-spacing:.4px; }}
  pre {{ background:var(--panel2); border:1px solid var(--line); border-radius:6px;
    padding:9px 11px; margin:0; overflow:auto; font-size:12px; white-space:pre-wrap; word-break:break-word; }}
  pre.msg {{ color:var(--fail); }}
  pre.mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}

  table.assert {{ width:100%; border-collapse:collapse; font-size:12px; }}
  table.assert th, table.assert td {{ text-align:left; padding:4px 8px; border-bottom:1px solid var(--line); vertical-align:top; }}
  table.assert th {{ color:var(--muted); font-weight:500; }}
  table.assert tr.bad td {{ color:var(--fail); }}
  table.assert tr.ok td:first-child {{ color:var(--pass); }}

  /* HTTP call cards */
  .call {{ background:var(--panel2); border:1px solid var(--line); border-radius:7px; padding:9px 11px; margin:7px 0; }}
  .call-head {{ display:flex; align-items:center; gap:9px; flex-wrap:wrap; }}
  .method {{ font-weight:700; font-size:11.5px; padding:1px 7px; border-radius:5px; }}
  .m-get {{ background:rgba(88,166,255,.16); color:var(--accent); }}
  .m-post {{ background:rgba(63,185,80,.16); color:var(--pass); }}
  .m-put {{ background:rgba(210,153,34,.16); color:var(--warn); }}
  .m-del {{ background:rgba(248,81,73,.16); color:var(--fail); }}
  .url {{ flex:1; font-size:12px; word-break:break-all; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  .status {{ font-weight:700; font-size:11.5px; padding:1px 8px; border-radius:9px; }}
  .status.s2 {{ background:rgba(63,185,80,.16); color:var(--pass); }}
  .status.s3 {{ background:rgba(210,153,34,.16); color:var(--warn); }}
  .status.s4 {{ background:rgba(248,81,73,.16); color:var(--fail); }}
  .status.sx {{ background:rgba(110,118,129,.2); color:var(--muted); }}
  .cdur {{ color:var(--muted); font-size:11px; }}
  .sdk {{ color:var(--muted); font-size:11.5px; margin:5px 0 2px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
  details.sub {{ margin:5px 0; }}
  details.sub > summary {{ cursor:pointer; color:var(--accent); font-size:11.5px; padding:2px 0; }}
  details.sub > pre {{ margin-top:5px; }}
</style></head>
<body>
<div class="top">
  <h1>CMA Python SDK — Integration Report</h1>
  <div class="meta">Region <b>{region}</b> · {host} · {timestamp}</div>
</div>
<div class="wrap">
  <div class="chips">
    <div class="chip"><span class="v">{total}</span><span class="k">Total</span></div>
    <div class="chip pass"><span class="v">{passed}</span><span class="k">Passed</span></div>
    <div class="chip fail"><span class="v">{failed}</span><span class="k">Failed</span></div>
    <div class="chip warn"><span class="v">{warnings}</span><span class="k">Warnings</span></div>
    <div class="chip xfail"><span class="v">{xfailed}</span><span class="k">Known issues</span></div>
    <div class="chip skip"><span class="v">{skipped}</span><span class="k">Skipped</span></div>
    <div class="chip rate"><span class="v">{pass_rate}%</span><span class="k">Pass rate</span></div>
    <div class="chip"><span class="v">{duration}s</span><span class="k">Duration</span></div>
  </div>
  <h2>Coverage by resource</h2>
  <div class="cov-wrap">{coverage}</div>
  <h2>Test details</h2>
  {sections}
</div>
</body></html>"""


def write_curl_log(records: List[TestRecord], output_path: str) -> None:
    """Plaintext cURL log (failed + warnings first), mirroring the JS test-curls.txt."""
    failed = [r for r in records if r.outcome == "failed"]
    warned = [r for r in records if r.has_warning]
    passed = [r for r in records if r.outcome == "passed" and not r.has_warning]
    lines = [
        "CMA Python SDK — API Requests Log",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Passed: {len(passed)} | Warnings: {len(warned)} | Failed: {len(failed)}",
        "=" * 80, "",
    ]

    def dump(group, header):
        if not group:
            return
        lines.append(f"\n{'=' * 40}\n{header} ({len(group)})\n{'=' * 40}\n")
        for i, r in enumerate(group, 1):
            lines.append("-" * 80)
            lines.append(f"[{i}] {r.nodeid}")
            lines.append("-" * 80)
            for c in r.calls:
                lines.append(f"{c.get('method')} {c.get('url')} [{c.get('status')}]")
                lines.append(c.get("curl", ""))
                lines.append("")

    dump(failed, "FAILED TESTS")
    dump(warned, "PASSED WITH WARNINGS (API >=400)")
    dump(passed, "PASSED TESTS")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
