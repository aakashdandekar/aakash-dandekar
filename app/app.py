import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from bson.errors import InvalidId
from app.core.config import settings
from app.database.db import init_db, get_db
from app.models.schema import ProjectIn, parse_project, ServiceIn, parse_service, SkillGroupIn, parse_skill_group, ChipIn, ValueIn, parse_generic, ContactIn, parse_contact, MessageIn, parse_message

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

def _valid_id(pid: str):
    try:
        return ObjectId(pid)
    except InvalidId:
        raise HTTPException(400, "Invalid ID format")

# ── Aggregate endpoint (single fetch for the frontend) ─────────────────────────
@app.get("/api/site-data", tags=["site"])
def site_data():
    db = get_db()
    data = {
        "projects": [parse_project(doc) for doc in db.projects.find().sort("sort_order", 1)],
        "services": [parse_service(doc) for doc in db.services.find().sort("sort_order", 1)],
        "skillGroups": [parse_skill_group(doc) for doc in db.skill_groups.find().sort("sort_order", 1)],
        "chips": [parse_generic(doc) for doc in db.about_chips.find().sort("sort_order", 1)],
        "values": [parse_generic(doc) for doc in db.about_values.find().sort("sort_order", 1)],
        "contactItems": [parse_contact(doc) for doc in db.contact_items.find().sort("sort_order", 1)],
    }
    return data


# ── Projects ───────────────────────────────────────────────────────────────────
@app.get("/api/projects", tags=["projects"])
def list_projects():
    db = get_db()
    return [parse_project(doc) for doc in db.projects.find().sort("sort_order", 1)]

@app.post("/api/projects", status_code=201, tags=["projects"])
def create_project(p: ProjectIn):
    db = get_db()
    payload = p.dict()
    res = db.projects.insert_one(payload)
    doc = db.projects.find_one({"_id": res.inserted_id})
    return parse_project(doc)

@app.put("/api/projects/{pid}", tags=["projects"])
def update_project(pid: str, p: ProjectIn):
    db = get_db()
    oid = _valid_id(pid)
    res = db.projects.update_one({"_id": oid}, {"$set": p.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Project not found")
    return parse_project(db.projects.find_one({"_id": oid}))

@app.delete("/api/projects/{pid}", status_code=204, tags=["projects"])
def delete_project(pid: str):
    db = get_db()
    db.projects.delete_one({"_id": _valid_id(pid)})


# ── Services ───────────────────────────────────────────────────────────────────
@app.get("/api/services", tags=["services"])
def list_services():
    db = get_db()
    return [parse_service(doc) for doc in db.services.find().sort("sort_order", 1)]

@app.post("/api/services", status_code=201, tags=["services"])
def create_service(s: ServiceIn):
    db = get_db()
    res = db.services.insert_one(s.dict())
    return parse_service(db.services.find_one({"_id": res.inserted_id}))

@app.put("/api/services/{sid}", tags=["services"])
def update_service(sid: str, s: ServiceIn):
    db = get_db()
    oid = _valid_id(sid)
    res = db.services.update_one({"_id": oid}, {"$set": s.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Service not found")
    return parse_service(db.services.find_one({"_id": oid}))

@app.delete("/api/services/{sid}", status_code=204, tags=["services"])
def delete_service(sid: str):
    db = get_db()
    db.services.delete_one({"_id": _valid_id(sid)})


# ── Skills ─────────────────────────────────────────────────────────────────────
@app.get("/api/skill-groups", tags=["skills"])
def list_skill_groups():
    db = get_db()
    return [parse_skill_group(doc) for doc in db.skill_groups.find().sort("sort_order", 1)]

@app.post("/api/skill-groups", status_code=201, tags=["skills"])
def create_skill_group(g: SkillGroupIn):
    db = get_db()
    res = db.skill_groups.insert_one(g.dict())
    return parse_skill_group(db.skill_groups.find_one({"_id": res.inserted_id}))

@app.put("/api/skill-groups/{gid}", tags=["skills"])
def update_skill_group(gid: str, g: SkillGroupIn):
    db = get_db()
    oid = _valid_id(gid)
    res = db.skill_groups.update_one({"_id": oid}, {"$set": g.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Skill group not found")
    return parse_skill_group(db.skill_groups.find_one({"_id": oid}))

@app.delete("/api/skill-groups/{gid}", status_code=204, tags=["skills"])
def delete_skill_group(gid: str):
    db = get_db()
    db.skill_groups.delete_one({"_id": _valid_id(gid)})


# ── About ──────────────────────────────────────────────────────────────────────
@app.get("/api/chips", tags=["about"])
def list_chips():
    db = get_db()
    return [parse_generic(doc) for doc in db.about_chips.find().sort("sort_order", 1)]

@app.post("/api/chips", status_code=201, tags=["about"])
def create_chip(ch: ChipIn):
    db = get_db()
    res = db.about_chips.insert_one(ch.dict())
    return parse_generic(db.about_chips.find_one({"_id": res.inserted_id}))

@app.put("/api/chips/{cid}", tags=["about"])
def update_chip(cid: str, ch: ChipIn):
    db = get_db()
    oid = _valid_id(cid)
    res = db.about_chips.update_one({"_id": oid}, {"$set": ch.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Chip not found")
    return parse_generic(db.about_chips.find_one({"_id": oid}))

@app.delete("/api/chips/{cid}", status_code=204, tags=["about"])
def delete_chip(cid: str):
    db = get_db()
    db.about_chips.delete_one({"_id": _valid_id(cid)})

@app.get("/api/values", tags=["about"])
def list_values():
    db = get_db()
    return [parse_generic(doc) for doc in db.about_values.find().sort("sort_order", 1)]

@app.post("/api/values", status_code=201, tags=["about"])
def create_value(v: ValueIn):
    db = get_db()
    res = db.about_values.insert_one(v.dict())
    return parse_generic(db.about_values.find_one({"_id": res.inserted_id}))

@app.put("/api/values/{vid}", tags=["about"])
def update_value(vid: str, v: ValueIn):
    db = get_db()
    oid = _valid_id(vid)
    res = db.about_values.update_one({"_id": oid}, {"$set": v.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Value not found")
    return parse_generic(db.about_values.find_one({"_id": oid}))

@app.delete("/api/values/{vid}", status_code=204, tags=["about"])
def delete_value(vid: str):
    db = get_db()
    db.about_values.delete_one({"_id": _valid_id(vid)})


# ── Contact ────────────────────────────────────────────────────────────────────
@app.get("/api/contact", tags=["contact"])
def list_contacts():
    db = get_db()
    return [parse_contact(doc) for doc in db.contact_items.find().sort("sort_order", 1)]

@app.post("/api/contact", status_code=201, tags=["contact"])
def create_contact(ct: ContactIn):
    db = get_db()
    res = db.contact_items.insert_one(ct.dict())
    return parse_contact(db.contact_items.find_one({"_id": res.inserted_id}))

@app.put("/api/contact/{cid}", tags=["contact"])
def update_contact(cid: str, ct: ContactIn):
    db = get_db()
    oid = _valid_id(cid)
    res = db.contact_items.update_one({"_id": oid}, {"$set": ct.dict()})
    if res.matched_count == 0:
        raise HTTPException(404, "Contact item not found")
    return parse_contact(db.contact_items.find_one({"_id": oid}))

@app.delete("/api/contact/{cid}", status_code=204, tags=["contact"])
def delete_contact(cid: str):
    db = get_db()
    db.contact_items.delete_one({"_id": _valid_id(cid)})


# ── Messages ───────────────────────────────────────────────────────────────────
@app.get("/api/messages", tags=["messages"])
def list_messages():
    db = get_db()
    # Sort backwards by _id to always put newest messages at the top
    return [parse_message(doc) for doc in db.messages.find().sort("_id", -1)]

@app.post("/api/messages", status_code=201, tags=["messages"])
def create_message(msg: MessageIn):
    db = get_db()
    db.messages.insert_one(msg.dict())
    return {"success": True}

@app.delete("/api/messages/{mid}", status_code=204, tags=["messages"])
def delete_message(mid: str):
    db = get_db()
    db.messages.delete_one({"_id": _valid_id(mid)})


# ── Static Mappings ────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse, tags=["site"])
def index_page():
    index_html = os.path.join(settings.TEMPLATES_DIR, "index.html")
    with open(index_html, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/admin", response_class=HTMLResponse, tags=["site"])
def admin_page():
    admin_html = os.path.join(settings.TEMPLATES_DIR, "admin.html")
    with open(admin_html, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
