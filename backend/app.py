#!/usr/bin/env python3
"""
IAM Learning Platform Backend
=============================
Flask REST API serving:
- Section content and metadata
- Simulation execution endpoints
- User progress tracking

Run: python app.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SECTIONS_DIR = PROJECT_ROOT


def get_sections():
    """Get all available IAM sections."""
    sections = []
    for i in range(1, 16):
        folder_name = f"{i}. " if i < 10 else f"{i}. "
        # Find the actual folder
        for item in PROJECT_ROOT.iterdir():
            if item.is_dir() and item.name.startswith(f"{i}."):
                sections.append({
                    "id": i,
                    "folder": item.name,
                    "title": item.name.split(". ", 1)[1] if ". " in item.name else item.name
                })
                break
    return sections


def get_section_content(section_id: int):
    """Read README.md content for a section."""
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and item.name.startswith(f"{section_id}."):
            readme_path = item / "README.md"
            if readme_path.exists():
                return readme_path.read_text(encoding="utf-8")
    return None


def get_section_projects(section_id: int):
    """List available Python projects for a section."""
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and item.name.startswith(f"{section_id}."):
            projects_dir = item / "projects"
            if projects_dir.exists():
                return [
                    {"name": f.name, "path": str(f.relative_to(PROJECT_ROOT))}
                    for f in projects_dir.glob("*.py")
                ]
    return []


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


@app.route("/api/sections", methods=["GET"])
def list_sections():
    return jsonify(get_sections())


@app.route("/api/sections/<int:section_id>", methods=["GET"])
def get_section(section_id):
    content = get_section_content(section_id)
    if content is None:
        return jsonify({"error": "Section not found"}), 404
    
    return jsonify({
        "id": section_id,
        "content": content,
        "projects": get_section_projects(section_id)
    })


@app.route("/api/sections/<int:section_id>/run", methods=["POST"])
def run_simulation(section_id):
    """Run a Python simulation for a section."""
    data = request.get_json() or {}
    project_name = data.get("project")
    
    if not project_name:
        return jsonify({"error": "Project name required"}), 400
    
    # Find the project file
    project_path = None
    for item in PROJECT_ROOT.iterdir():
        if item.is_dir() and item.name.startswith(f"{section_id}."):
            potential = item / "projects" / project_name
            if potential.exists():
                project_path = potential
                break
    
    if project_path is None:
        return jsonify({"error": "Project not found"}), 404
    
    # Run the simulation
    try:
        result = subprocess.run(
            [sys.executable, str(project_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "project": project_name
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Simulation timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/search", methods=["GET"])
def search():
    """Search across all section content."""
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify([])
    
    results = []
    for section in get_sections():
        content = get_section_content(section["id"])
        if content and query in content.lower():
            # Find context around match
            idx = content.lower().find(query)
            start = max(0, idx - 100)
            end = min(len(content), idx + 200)
            context = content[start:end]
            
            results.append({
                "section_id": section["id"],
                "section_title": section["title"],
                "context": context
            })
    
    return jsonify(results)


if __name__ == "__main__":
    print("🚀 IAM Learning Platform API starting...")
    print("   Sections loaded:", len(get_sections()))
    app.run(host="0.0.0.0", port=5000, debug=True)
