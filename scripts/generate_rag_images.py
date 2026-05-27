from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency: Pillow. Run `python3 -m pip install -r requirements.txt` "
        "from the repository root, then retry."
    ) from exc


OUT = Path(__file__).resolve().parents[1] / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


F_TITLE = font(56, True)
F_SUB = font(28)
F_H = font(30, True)
F_B = font(22)
F_SM = font(18)
F_XS = font(16)

BG = (247, 249, 250)
INK = (24, 32, 38)
MUTED = (88, 98, 108)
BLUE = (33, 94, 156)
GREEN = (31, 132, 98)
RED = (174, 69, 54)
YELLOW = (216, 154, 46)
PURPLE = (112, 83, 168)
CARD = (255, 255, 255)
BORDER = (210, 218, 225)


def draw_text(draw, xy, text, fnt, fill=INK, max_width=None, line_gap=6):
    x, y = xy
    if max_width is None:
        draw.text((x, y), text, font=fnt, fill=fill)
        return y + draw.textbbox((x, y), text, font=fnt)[3] - y
    words = text.split()
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if draw.textlength(candidate, font=fnt) <= max_width:
            line = candidate
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + line_gap
            line = word
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def rounded(draw, box, fill=CARD, outline=BORDER, radius=18, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, start, end, fill=MUTED, width=4):
    draw.line([start, end], fill=fill, width=width)
    x1, y1 = start
    x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 12 if x2 >= x1 else -12
        draw.polygon([(x2, y2), (x2 - s, y2 - 8), (x2 - s, y2 + 8)], fill=fill)
    else:
        s = 12 if y2 >= y1 else -12
        draw.polygon([(x2, y2), (x2 - 8, y2 - s), (x2 + 8, y2 - s)], fill=fill)


def card(draw, x, y, w, h, title, body, accent):
    rounded(draw, (x, y, x + w, y + h), radius=20)
    draw.rounded_rectangle((x, y, x + 10, y + h), radius=8, fill=accent)
    draw.text((x + 28, y + 20), title, font=F_H, fill=INK)
    draw_text(draw, (x + 28, y + 62), body, F_SM, fill=MUTED, max_width=w - 56, line_gap=4)


def lane(draw, box, title, accent):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=24, fill=(255, 255, 255), outline=BORDER, width=2)
    draw.rounded_rectangle((x1, y1, x1 + 14, y2), radius=8, fill=accent)
    draw.text((x1 + 28, y1 + 22), title, font=F_B, fill=INK)


def small_box(draw, x, y, w, h, title, body, accent):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=14, fill=CARD, outline=BORDER, width=2)
    draw.rounded_rectangle((x, y, x + w, y + 8), radius=4, fill=accent)
    draw.text((x + 18, y + 18), title, font=F_B, fill=INK)
    draw_text(draw, (x + 18, y + 50), body, F_XS, fill=MUTED, max_width=w - 36, line_gap=3)


def hero():
    img = Image.new("RGB", (1600, 900), BG)
    d = ImageDraw.Draw(img)
    for i, color in enumerate([BLUE, GREEN, YELLOW, PURPLE]):
        d.rounded_rectangle((1080 + i * 72, 72 + i * 34, 1440 + i * 72, 760 - i * 20), radius=34, outline=color, width=6)
    draw_text(d, (90, 82), "RAG Is Not a Feature", F_TITLE, max_width=850)
    draw_text(d, (90, 154), "It Is an Evidence Supply Chain", F_TITLE, max_width=900)
    draw_text(
        d,
        (94, 260),
        "Production retrieval-augmented generation connects governed data, hybrid retrieval, reranking, grounded generation, evals, and security controls.",
        F_SUB,
        fill=MUTED,
        max_width=820,
        line_gap=8,
    )
    stages = [
        ("Sources", "Docs, APIs, tickets, code", BLUE),
        ("Indexing", "Parse, chunk, embed, govern", GREEN),
        ("Retrieval", "Hybrid search, fusion, rerank", YELLOW),
        ("Answer", "Cite, verify, abstain", PURPLE),
    ]
    x = 100
    y = 510
    for i, (title, body, accent) in enumerate(stages):
        card(d, x + i * 360, y, 290, 190, title, body, accent)
        if i < len(stages) - 1:
            arrow(d, (x + i * 360 + 300, y + 95), (x + (i + 1) * 360 - 20, y + 95), fill=(105, 114, 122), width=4)
    draw_text(d, (100, 780), "A system design guide for builders who need RAG to be reliable, observable, and secure.", F_B, fill=INK, max_width=1200)
    img.save(OUT / "rag-evidence-supply-chain-hero.png")


def architecture():
    img = Image.new("RGB", (1600, 1000), BG)
    d = ImageDraw.Draw(img)
    draw_text(d, (70, 52), "Production RAG Reference Architecture", F_TITLE, max_width=1250)
    draw_text(d, (75, 126), "Separate the offline data plane from the online control plane, then close the loop with evaluation.", F_SUB, fill=MUTED, max_width=1250)
    d.rounded_rectangle((70, 210, 1530, 510), radius=26, fill=(236, 244, 250), outline=(187, 207, 222), width=2)
    d.text((100, 235), "Offline indexing / data plane", font=F_H, fill=BLUE)
    offline = [
        ("Sources", "Docs, PDFs, DBs, tickets"),
        ("Parse", "Layout, tables, OCR, code"),
        ("Chunk", "Structure, metadata, ACLs"),
        ("Index", "Vectors, BM25, graph, lineage"),
    ]
    for i, (t, b) in enumerate(offline):
        x = 110 + i * 355
        card(d, x, 305, 275, 140, t, b, [BLUE, GREEN, YELLOW, PURPLE][i])
        if i < 3:
            arrow(d, (x + 285, 375), (x + 335, 375), fill=MUTED)
    d.rounded_rectangle((70, 570, 1530, 905), radius=26, fill=(246, 241, 232), outline=(220, 201, 164), width=2)
    d.text((100, 595), "Online inference / control plane", font=F_H, fill=(148, 102, 34))
    online = [
        ("Policy", "Identity, tenant, purpose"),
        ("Query", "Rewrite, decompose, route"),
        ("Retrieve", "Hybrid search + filters"),
        ("Rerank", "Fusion, compression"),
        ("Generate", "Answer, cite, abstain"),
        ("Observe", "Trace, judge, improve"),
    ]
    for i, (t, b) in enumerate(online):
        x = 105 + i * 235
        card(d, x, 675, 200, 145, t, b, [RED, PURPLE, BLUE, GREEN, YELLOW, (80, 95, 110)][i])
        if i < 5:
            arrow(d, (x + 207, 748), (x + 228, 748), fill=MUTED, width=3)
    arrow(d, (1375, 675), (1375, 465), fill=(80, 95, 110), width=5)
    d.text((1250, 520), "feedback loop", font=F_SM, fill=MUTED)
    img.save(OUT / "rag-reference-architecture.png")


def retrieval_eval():
    img = Image.new("RGB", (1600, 1000), BG)
    d = ImageDraw.Draw(img)
    draw_text(d, (70, 52), "Retrieval, Reranking, and Evaluation Loop", F_TITLE, max_width=1280)
    draw_text(d, (75, 126), "Optimize RAG as a ranking system, then prove quality with component and end-to-end evals.", F_SUB, fill=MUTED, max_width=1300)
    top = [
        ("BM25", "Exact terms, IDs, clauses", BLUE),
        ("Dense ANN", "Semantic intent, paraphrase", GREEN),
        ("Graph / SQL / Live", "Relationships and freshness", PURPLE),
    ]
    for i, (t, b, c) in enumerate(top):
        card(d, 130 + i * 460, 240, 350, 150, t, b, c)
        arrow(d, (305 + i * 460, 392), (305 + i * 460, 470), fill=MUTED)
    card(d, 460, 470, 680, 150, "Fusion + Reranking", "RRF merges ranked lists. Cross-encoders or late interaction rerank the candidate pool.", YELLOW)
    arrow(d, (800, 622), (800, 700), fill=MUTED)
    card(d, 460, 700, 680, 150, "Context Assembly", "Dedupe, compress, cite sources, order evidence, and keep the model inside the evidence boundary.", RED)
    arrow(d, (1145, 775), (1290, 775), fill=MUTED)
    card(d, 1210, 700, 270, 150, "Answer", "Grounded response or abstain", GREEN)
    arrow(d, (1295, 700), (1295, 610), fill=(80, 95, 110))
    arrow(d, (1295, 610), (1060, 610), fill=(80, 95, 110))
    d.text((1095, 565), "judge + traces", font=F_SM, fill=MUTED)
    metrics = [
        "Recall@k",
        "Context precision",
        "Faithfulness",
        "Citation support",
        "Negative rejection",
        "Latency + cost",
    ]
    x0, y0 = 130, 710
    d.text((130, 650), "Release gates", font=F_H, fill=INK)
    for i, m in enumerate(metrics):
        y = y0 + i * 38
        d.rounded_rectangle((130, y, 380, y + 28), radius=14, fill=(255, 255, 255), outline=BORDER)
        d.text((148, y + 4), m, font=F_SM, fill=INK)
    img.save(OUT / "rag-retrieval-eval-loop.png")


def online_request_path():
    img = Image.new("RGB", (1600, 1000), BG)
    d = ImageDraw.Draw(img)
    draw_text(d, (70, 52), "Online RAG Serving Request Path", F_TITLE, max_width=1280)
    draw_text(
        d,
        (75, 126),
        "A production request is a policy-scoped ranking pipeline, not a direct call from chat UI to vector DB.",
        F_SUB,
        fill=MUTED,
        max_width=1320,
    )

    boxes = [
        (85, 250, 245, 160, "Client", "User or agent sends query, identity token, tenant, purpose.", BLUE),
        (375, 250, 245, 160, "Gateway", "AuthN, rate limit, budget, request trace.", RED),
        (665, 250, 245, 160, "Policy", "RBAC, ABAC, ReBAC, ACL filters, obligations.", PURPLE),
        (955, 250, 245, 160, "Planner", "Intent classify, rewrite, decompose, choose tools.", YELLOW),
        (1245, 250, 245, 160, "Retrievers", "Vector, BM25, graph, SQL, live source APIs.", GREEN),
    ]
    for i, (x, y, w, h, t, b, c) in enumerate(boxes):
        card(d, x, y, w, h, t, b, c)
        if i < len(boxes) - 1:
            arrow(d, (x + w + 8, y + 80), (boxes[i + 1][0] - 16, y + 80), fill=MUTED, width=4)

    card(d, 245, 525, 310, 160, "Candidate Pool", "Broad permitted candidates with scores, source IDs, ACLs, timestamps.", BLUE)
    card(d, 645, 525, 310, 160, "Rerank + Pack", "Fusion, cross-encoder rerank, dedupe, compress, token budget.", GREEN)
    card(d, 1045, 525, 310, 160, "Grounded LLM", "Source-labeled context, citation instructions, abstention policy.", YELLOW)
    arrow(d, (1368, 410), (1200, 520), fill=MUTED, width=4)
    arrow(d, (555, 605), (635, 605), fill=MUTED, width=4)
    arrow(d, (955, 605), (1035, 605), fill=MUTED, width=4)

    card(d, 1025, 765, 290, 145, "Verify", "Faithfulness, citations, safety, policy obligations.", RED)
    card(d, 245, 765, 710, 145, "Observability + Evaluation", "Trace authorize, rewrite, retrieve, rerank, build_prompt, generate, verify, respond.", PURPLE)
    small_box(d, 1370, 785, 145, 105, "Return", "Answer, cite, abstain, or escalate.", GREEN)
    arrow(d, (1200, 685), (1200, 760), fill=MUTED, width=4)
    arrow(d, (1020, 835), (960, 835), fill=MUTED, width=4)
    arrow(d, (955, 820), (1040, 630), fill=(80, 95, 110), width=3)
    arrow(d, (1315, 835), (1360, 835), fill=MUTED, width=4)
    arrow(d, (600, 765), (600, 695), fill=(80, 95, 110), width=4)
    d.text((625, 716), "production traces feed evals and tuning", font=F_SM, fill=MUTED)
    img.save(OUT / "rag-online-serving-request-path.png")


def policy_authorization_plane():
    img = Image.new("RGB", (1600, 1000), BG)
    d = ImageDraw.Draw(img)
    draw_text(d, (70, 52), "Policy and Identity Plane for RAG", F_TITLE, max_width=1250)
    draw_text(
        d,
        (75, 126),
        "Authorization must shape retrieval before evidence reaches reranking, prompts, tools, caches, or logs.",
        F_SUB,
        fill=MUTED,
        max_width=1320,
    )

    lane(d, (70, 220, 1530, 410), "1. Resolve the subject", BLUE)
    small_box(d, 125, 285, 250, 90, "Identity token", "User, service, agent, delegation.", BLUE)
    small_box(d, 430, 285, 250, 90, "Directory", "Groups, roles, tenant, region.", GREEN)
    small_box(d, 735, 285, 250, 90, "Entitlements", "Apps, cases, accounts, projects.", YELLOW)
    small_box(d, 1040, 285, 250, 90, "Purpose", "Business intent, risk tier, session.", PURPLE)
    for x1, x2 in [(375, 430), (680, 735), (985, 1040)]:
        arrow(d, (x1, 330), (x2 - 12, 330), fill=MUTED, width=3)

    lane(d, (70, 470, 1530, 655), "2. Decide policy", PURPLE)
    small_box(d, 125, 535, 260, 90, "RBAC", "Coarse role permissions.", RED)
    small_box(d, 430, 535, 260, 90, "ABAC", "Attributes, classification, device, time.", BLUE)
    small_box(d, 735, 535, 260, 90, "ReBAC", "User-to-resource relationships.", GREEN)
    small_box(d, 1040, 535, 330, 90, "Policy decision point", "Allow, deny, filters, obligations.", YELLOW)
    arrow(d, (1290, 375), (1210, 530), fill=MUTED, width=3)
    for x1, x2 in [(385, 430), (690, 735), (995, 1040)]:
        arrow(d, (x1, 580), (x2 - 12, 580), fill=MUTED, width=3)

    lane(d, (70, 720, 1530, 910), "3. Enforce everywhere", GREEN)
    small_box(d, 125, 785, 210, 90, "Pre-filter", "Tenant, ACL, classification.", BLUE)
    small_box(d, 380, 785, 210, 90, "Retrieve", "Permitted candidates only.", GREEN)
    small_box(d, 635, 785, 210, 90, "Re-check", "Chunk-level source policy.", PURPLE)
    small_box(d, 890, 785, 210, 90, "Assemble", "Redact, cite, minimize.", YELLOW)
    small_box(d, 1145, 785, 260, 90, "Audit", "Decision, sources, filters, answer.", RED)
    arrow(d, (1205, 625), (230, 780), fill=MUTED, width=3)
    for x1, x2 in [(335, 380), (590, 635), (845, 890), (1100, 1145)]:
        arrow(d, (x1, 830), (x2 - 12, 830), fill=MUTED, width=3)

    draw_text(d, (100, 938), "Design invariant: unauthorized chunks must not enter candidate pools, prompts, caches, or evaluator traces.", F_B, fill=INK, max_width=1380)
    img.save(OUT / "rag-policy-authorization-plane.png")


def multitenant_freshness():
    img = Image.new("RGB", (1600, 1000), BG)
    d = ImageDraw.Draw(img)
    draw_text(d, (70, 52), "Multi-Tenant and Freshness-Aware RAG", F_TITLE, max_width=1320)
    draw_text(
        d,
        (75, 126),
        "SaaS RAG needs isolation, deletion propagation, index versioning, and routing between indexed and live sources.",
        F_SUB,
        fill=MUTED,
        max_width=1320,
    )

    d.rounded_rectangle((75, 220, 760, 875), radius=26, fill=(236, 244, 250), outline=(187, 207, 222), width=2)
    d.text((110, 250), "Tenant isolation", font=F_H, fill=BLUE)
    tenants = [
        ("Tenant A", "namespace / shard / index A", BLUE),
        ("Tenant B", "namespace / shard / index B", GREEN),
        ("Tenant C", "namespace / shard / index C", PURPLE),
    ]
    for i, (t, b, c) in enumerate(tenants):
        y = 330 + i * 150
        small_box(d, 120, y, 245, 95, f"{t} sources", "Docs, tickets, DB rows, files.", c)
        small_box(d, 445, y, 245, 95, t, b, c)
        arrow(d, (365, y + 48), (435, y + 48), fill=MUTED, width=3)
    draw_text(d, (125, 792), "Negative tests should prove tenant B cannot retrieve tenant A evidence, even through caches or rerankers.", F_SM, fill=MUTED, max_width=550)

    d.rounded_rectangle((840, 220, 1525, 875), radius=26, fill=(246, 241, 232), outline=(220, 201, 164), width=2)
    d.text((875, 250), "Freshness and lifecycle", font=F_H, fill=(148, 102, 34))
    small_box(d, 890, 330, 245, 95, "Batch sync", "Scheduled crawl, chunk, embed, version.", BLUE)
    small_box(d, 1215, 330, 245, 95, "Event sync", "Webhooks, queues, tombstones.", GREEN)
    small_box(d, 890, 505, 245, 95, "Live retrieval", "Source-of-truth APIs for volatile facts.", PURPLE)
    small_box(d, 1215, 505, 245, 95, "Hybrid router", "Choose index or live path by query risk.", YELLOW)
    small_box(d, 1045, 690, 265, 105, "Governed answer", "Citations, policy obligations, source timestamps.", RED)
    arrow(d, (1135, 378), (1205, 378), fill=MUTED, width=3)
    arrow(d, (1135, 553), (1205, 553), fill=MUTED, width=3)
    arrow(d, (1338, 600), (1195, 685), fill=MUTED, width=3)
    arrow(d, (1012, 600), (1115, 685), fill=MUTED, width=3)
    draw_text(d, (875, 805), "Freshness is a product SLA: define acceptable staleness by source, risk, tenant, and answer type.", F_SM, fill=MUTED, max_width=560)

    arrow(d, (760, 550), (840, 550), fill=(80, 95, 110), width=5)
    d.text((765, 505), "tenant-scoped", font=F_SM, fill=MUTED)
    d.text((770, 530), "routing", font=F_SM, fill=MUTED)
    img.save(OUT / "rag-multitenant-freshness-architecture.png")


if __name__ == "__main__":
    hero()
    architecture()
    retrieval_eval()
    online_request_path()
    policy_authorization_plane()
    multitenant_freshness()
    for path in sorted(OUT.glob("*.png")):
        print(path)
