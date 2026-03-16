#!/usr/bin/env python3
"""Parse Supported Software Matrix .docx files into core catalog JSON (MVP stage 1)."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from docx import Document

HEADER_ALIASES = {
    "component": "component",
    "description": "description",
    "version": "version",
    "applicable idit version": "applicableIditVersions",
    "applicable idit versions": "applicableIditVersions",
    "comments": "comments",
}

TARGET_COLUMNS = [
    "component",
    "description",
    "version",
    "applicableIditVersions",
    "comments",
]


def normalize_header(value: str) -> str:
    compact = re.sub(r"\s+", " ", value.strip().lower())
    return re.sub(r"[^a-z0-9 ]", "", compact)


def extract_core_version(file_name: str) -> str | None:
    match = re.search(r"(?:^|[^\d])v?(\d{2}\.\d)(?:[^\d]|$)", file_name, flags=re.IGNORECASE)
    return match.group(1) if match else None


def parse_document(path: Path) -> Dict:
    doc = Document(path)
    imports: List[Dict[str, str]] = []

    for table in doc.tables:
        if not table.rows:
            continue

        headers = [normalize_header(cell.text) for cell in table.rows[0].cells]
        mapped_headers = [HEADER_ALIASES.get(header) for header in headers]

        if "component" not in mapped_headers or "version" not in mapped_headers:
            continue

        for row in table.rows[1:]:
            item: Dict[str, str] = {key: "" for key in TARGET_COLUMNS}
            has_data = False

            for idx, cell in enumerate(row.cells):
                mapped = mapped_headers[idx] if idx < len(mapped_headers) else None
                if not mapped:
                    continue

                text = re.sub(r"\s+", " ", cell.text).strip()
                item[mapped] = text
                has_data = has_data or bool(text)

            if has_data:
                imports.append(item)

    return {
        "coreVersion": extract_core_version(path.name),
        "sourceFile": str(path),
        "rows": imports,
    }


def build_catalog(source_docs: Path) -> Dict:
    docs = sorted(source_docs.rglob("*.docx"))
    parsed = [parse_document(path) for path in docs]

    valid_versions = sorted({entry["coreVersion"] for entry in parsed if entry["coreVersion"]})

    versions = [
        {
            "key": f"core{version.replace('.', '_')}",
            "label": f"core {version}",
        }
        for version in valid_versions
    ]

    core_tech_stack = {entry["key"]: {} for entry in versions}

    return {
        "metadata": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "sourceDir": str(source_docs),
            "documentsProcessed": len(parsed),
        },
        "versions": versions,
        "coreTechStack": core_tech_stack,
        "imports": parsed,
    }


def to_app_catalog(catalog: Dict) -> Dict:
    return {
        "versions": catalog.get("versions", []),
        "techStack": catalog.get("coreTechStack", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse Supported Software Matrix .docx files")
    parser.add_argument("--source", default="data/source-docs", help="Source folder for .docx files")
    parser.add_argument("--output", default="data/generated/core-catalog.json", help="Output JSON path")
    parser.add_argument(
        "--app-output",
        default="core-catalog.json",
        help="Optional app catalog output path (UI-compatible versions + techStack)",
    )
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)
    app_output = Path(args.app_output) if args.app_output else None

    output.parent.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog(source)

    output.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    if app_output and catalog["metadata"]["documentsProcessed"] > 0:
        app_output.write_text(json.dumps(to_app_catalog(catalog), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output} from {catalog['metadata']['documentsProcessed']} document(s).")


if __name__ == "__main__":
    main()
