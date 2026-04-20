from pydantic import BaseModel
from typing import List

class ProjectIn(BaseModel):
    title: str
    abbr: str
    description: str
    tags: List[str]       = []
    stack: List[str]      = []
    link: str             = "#"
    color: str            = "cyan"
    featured: bool        = False
    sort_order: int       = 0

class ServiceIn(BaseModel):
    title: str
    description: str
    list_items: List[str] = []
    sort_order: int       = 0

class SkillGroupIn(BaseModel):
    title: str
    color: str            = "cyan"
    skills: List[str]     = []
    sort_order: int       = 0

class ChipIn(BaseModel):
    name: str
    sort_order: int       = 0

class ValueIn(BaseModel):
    num: str
    title: str
    description: str
    sort_order: int       = 0

class ContactIn(BaseModel):
    abbr: str
    label: str
    href: str
    display: str
    is_external: bool     = True
    sort_order: int       = 0

class MessageIn(BaseModel):
    name: str
    email: str
    projectType: str
    message: str


# ── Row parsers ────────────────────────────────────────────────────────────────

def _base_parse(doc: dict) -> dict:
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

def parse_project(doc: dict) -> dict:
    d = _base_parse(doc)
    d["featured"] = bool(d.get("featured", False))
    return d

def parse_service(doc: dict) -> dict:
    return _base_parse(doc)

def parse_skill_group(doc: dict) -> dict:
    return _base_parse(doc)

def parse_contact(doc: dict) -> dict:
    d = _base_parse(doc)
    d["is_external"] = bool(d.get("is_external", True))
    return d

def parse_generic(doc: dict) -> dict:
    return _base_parse(doc)

def parse_message(doc: dict) -> dict:
    return _base_parse(doc)
