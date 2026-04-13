import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .database.db import init_db, get_db
from .models.schema import (
    ProjectIn, parse_project,
    ServiceIn, parse_service,
    SkillGroupIn, parse_skill_group,
    ChipIn, ValueIn,
    ContactIn, parse_contact
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── Middleware ─────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Startup ────────────────────────────────────────────────────────────────────
@app.on_event("startup")
def startup():
    init_db()


# ── Aggregate endpoint (single fetch for the frontend) ─────────────────────────
@app.get("/api/site-data", tags=["site"])
def site_data():
    db = get_db()
    c = db.cursor()
    data = {
        "projects": [parse_project(r) for r in c.execute("SELECT * FROM projects ORDER BY sort_order").fetchall()],
        "services": [parse_service(r) for r in c.execute("SELECT * FROM services ORDER BY sort_order").fetchall()],
        "skillGroups": [parse_skill_group(r) for r in c.execute("SELECT * FROM skill_groups ORDER BY sort_order").fetchall()],
        "chips": [dict(r) for r in c.execute("SELECT * FROM about_chips ORDER BY sort_order").fetchall()],
        "values": [dict(r) for r in c.execute("SELECT * FROM about_values ORDER BY sort_order").fetchall()],
        "contactItems": [parse_contact(r) for r in c.execute("SELECT * FROM contact_items ORDER BY sort_order").fetchall()],
    }
    db.close()
    return data


# ── Projects ───────────────────────────────────────────────────────────────────
@app.get("/api/projects", tags=["projects"])
def list_projects():
    db = get_db()
    rows = db.execute("SELECT * FROM projects ORDER BY sort_order").fetchall()
    db.close()
    return [parse_project(r) for r in rows]

@app.post("/api/projects", status_code=201, tags=["projects"])
def create_project(p: ProjectIn):
    db = get_db()
    cur = db.execute(
        "INSERT INTO projects (title,abbr,description,tags,stack,link,color,featured,sort_order) VALUES(?,?,?,?,?,?,?,?,?)",
        (p.title, p.abbr, p.description, json.dumps(p.tags), json.dumps(p.stack),
         p.link, p.color, int(p.featured), p.sort_order),
    )
    db.commit()
    row = db.execute("SELECT * FROM projects WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return parse_project(row)

@app.put("/api/projects/{pid}", tags=["projects"])
def update_project(pid: int, p: ProjectIn):
    db = get_db()
    db.execute(
        "UPDATE projects SET title=?,abbr=?,description=?,tags=?,stack=?,link=?,color=?,featured=?,sort_order=? WHERE id=?",
        (p.title, p.abbr, p.description, json.dumps(p.tags), json.dumps(p.stack),
         p.link, p.color, int(p.featured), p.sort_order, pid),
    )
    db.commit()
    row = db.execute("SELECT * FROM projects WHERE id=?", (pid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Project not found")
    return parse_project(row)

@app.delete("/api/projects/{pid}", status_code=204, tags=["projects"])
def delete_project(pid: int):
    db = get_db()
    db.execute("DELETE FROM projects WHERE id=?", (pid,))
    db.commit()
    db.close()


# ── Services ───────────────────────────────────────────────────────────────────
@app.get("/api/services", tags=["services"])
def list_services():
    db = get_db()
    rows = db.execute("SELECT * FROM services ORDER BY sort_order").fetchall()
    db.close()
    return [parse_service(r) for r in rows]

@app.post("/api/services", status_code=201, tags=["services"])
def create_service(s: ServiceIn):
    db = get_db()
    cur = db.execute(
        "INSERT INTO services (title,description,list_items,sort_order) VALUES(?,?,?,?)",
        (s.title, s.description, json.dumps(s.list_items), s.sort_order),
    )
    db.commit()
    row = db.execute("SELECT * FROM services WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return parse_service(row)

@app.put("/api/services/{sid}", tags=["services"])
def update_service(sid: int, s: ServiceIn):
    db = get_db()
    db.execute(
        "UPDATE services SET title=?,description=?,list_items=?,sort_order=? WHERE id=?",
        (s.title, s.description, json.dumps(s.list_items), s.sort_order, sid),
    )
    db.commit()
    row = db.execute("SELECT * FROM services WHERE id=?", (sid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Service not found")
    return parse_service(row)

@app.delete("/api/services/{sid}", status_code=204, tags=["services"])
def delete_service(sid: int):
    db = get_db()
    db.execute("DELETE FROM services WHERE id=?", (sid,))
    db.commit()
    db.close()


# ── Skills ─────────────────────────────────────────────────────────────────────
@app.get("/api/skill-groups", tags=["skills"])
def list_skill_groups():
    db = get_db()
    rows = db.execute("SELECT * FROM skill_groups ORDER BY sort_order").fetchall()
    db.close()
    return [parse_skill_group(r) for r in rows]

@app.post("/api/skill-groups", status_code=201, tags=["skills"])
def create_skill_group(g: SkillGroupIn):
    db = get_db()
    cur = db.execute(
        "INSERT INTO skill_groups (title,color,skills,sort_order) VALUES(?,?,?,?)",
        (g.title, g.color, json.dumps(g.skills), g.sort_order),
    )
    db.commit()
    row = db.execute("SELECT * FROM skill_groups WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return parse_skill_group(row)

@app.put("/api/skill-groups/{gid}", tags=["skills"])
def update_skill_group(gid: int, g: SkillGroupIn):
    db = get_db()
    db.execute(
        "UPDATE skill_groups SET title=?,color=?,skills=?,sort_order=? WHERE id=?",
        (g.title, g.color, json.dumps(g.skills), g.sort_order, gid),
    )
    db.commit()
    row = db.execute("SELECT * FROM skill_groups WHERE id=?", (gid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Skill group not found")
    return parse_skill_group(row)

@app.delete("/api/skill-groups/{gid}", status_code=204, tags=["skills"])
def delete_skill_group(gid: int):
    db = get_db()
    db.execute("DELETE FROM skill_groups WHERE id=?", (gid,))
    db.commit()
    db.close()


# ── About ──────────────────────────────────────────────────────────────────────
@app.get("/api/chips", tags=["about"])
def list_chips():
    db = get_db()
    rows = db.execute("SELECT * FROM about_chips ORDER BY sort_order").fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/api/chips", status_code=201, tags=["about"])
def create_chip(ch: ChipIn):
    db = get_db()
    cur = db.execute("INSERT INTO about_chips (name,sort_order) VALUES(?,?)", (ch.name, ch.sort_order))
    db.commit()
    row = db.execute("SELECT * FROM about_chips WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return dict(row)

@app.put("/api/chips/{cid}", tags=["about"])
def update_chip(cid: int, ch: ChipIn):
    db = get_db()
    db.execute("UPDATE about_chips SET name=?,sort_order=? WHERE id=?", (ch.name, ch.sort_order, cid))
    db.commit()
    row = db.execute("SELECT * FROM about_chips WHERE id=?", (cid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Chip not found")
    return dict(row)

@app.delete("/api/chips/{cid}", status_code=204, tags=["about"])
def delete_chip(cid: int):
    db = get_db()
    db.execute("DELETE FROM about_chips WHERE id=?", (cid,))
    db.commit()
    db.close()


@app.get("/api/values", tags=["about"])
def list_values():
    db = get_db()
    rows = db.execute("SELECT * FROM about_values ORDER BY sort_order").fetchall()
    db.close()
    return [dict(r) for r in rows]

@app.post("/api/values", status_code=201, tags=["about"])
def create_value(v: ValueIn):
    db = get_db()
    cur = db.execute(
        "INSERT INTO about_values (num,title,description,sort_order) VALUES(?,?,?,?)",
        (v.num, v.title, v.description, v.sort_order),
    )
    db.commit()
    row = db.execute("SELECT * FROM about_values WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return dict(row)

@app.put("/api/values/{vid}", tags=["about"])
def update_value(vid: int, v: ValueIn):
    db = get_db()
    db.execute(
        "UPDATE about_values SET num=?,title=?,description=?,sort_order=? WHERE id=?",
        (v.num, v.title, v.description, v.sort_order, vid),
    )
    db.commit()
    row = db.execute("SELECT * FROM about_values WHERE id=?", (vid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Value not found")
    return dict(row)

@app.delete("/api/values/{vid}", status_code=204, tags=["about"])
def delete_value(vid: int):
    db = get_db()
    db.execute("DELETE FROM about_values WHERE id=?", (vid,))
    db.commit()
    db.close()


# ── Contact ────────────────────────────────────────────────────────────────────
@app.get("/api/contact", tags=["contact"])
def list_contacts():
    db = get_db()
    rows = db.execute("SELECT * FROM contact_items ORDER BY sort_order").fetchall()
    db.close()
    return [parse_contact(r) for r in rows]

@app.post("/api/contact", status_code=201, tags=["contact"])
def create_contact(ct: ContactIn):
    db = get_db()
    cur = db.execute(
        "INSERT INTO contact_items (abbr,label,href,display,is_external,sort_order) VALUES(?,?,?,?,?,?)",
        (ct.abbr, ct.label, ct.href, ct.display, int(ct.is_external), ct.sort_order),
    )
    db.commit()
    row = db.execute("SELECT * FROM contact_items WHERE id=?", (cur.lastrowid,)).fetchone()
    db.close()
    return parse_contact(row)

@app.put("/api/contact/{cid}", tags=["contact"])
def update_contact(cid: int, ct: ContactIn):
    db = get_db()
    db.execute(
        "UPDATE contact_items SET abbr=?,label=?,href=?,display=?,is_external=?,sort_order=? WHERE id=?",
        (ct.abbr, ct.label, ct.href, ct.display, int(ct.is_external), ct.sort_order, cid),
    )
    db.commit()
    row = db.execute("SELECT * FROM contact_items WHERE id=?", (cid,)).fetchone()
    db.close()
    if not row:
        raise HTTPException(404, "Contact not found")
    return parse_contact(row)

@app.delete("/api/contact/{cid}", status_code=204, tags=["contact"])
def delete_contact(cid: int):
    db = get_db()
    db.execute("DELETE FROM contact_items WHERE id=?", (cid,))
    db.commit()
    db.close()


# ── Frontend & Admin ───────────────────────────────────────────────────────────
index_html = os.path.join(settings.TEMPLATES_DIR, "index.html")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home_page():
    with open(index_html, "r", encoding="utf-8") as f:
        return f.read()

admin_html = os.path.join(settings.TEMPLATES_DIR, "admin.html")

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def admin_page():
    with open(admin_html, "r", encoding="utf-8") as f:
        return f.read()


# ── Static Files ───────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

