"""Pydantic request/response models and SQLite row parsers."""
import json
from pydantic import BaseModel
from typing import List


# ── Request models ─────────────────────────────────────────────────────────────

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


# ── Row parsers ────────────────────────────────────────────────────────────────

def parse_project(row) -> dict:
    d = dict(row)
    d["tags"]    = json.loads(d["tags"])
    d["stack"]   = json.loads(d["stack"])
    d["featured"] = bool(d["featured"])
    return d

def parse_service(row) -> dict:
    d = dict(row)
    d["list_items"] = json.loads(d["list_items"])
    return d

def parse_skill_group(row) -> dict:
    d = dict(row)
    d["skills"] = json.loads(d["skills"])
    return d

def parse_contact(row) -> dict:
    d = dict(row)
    d["is_external"] = bool(d["is_external"])
    return d
