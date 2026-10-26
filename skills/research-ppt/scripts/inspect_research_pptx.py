#!/usr/bin/env python3
"""Inspect a PPTX without changing it; structural checks are not visual/edit tests."""

from __future__ import annotations

import argparse
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import BadZipFile, ZipFile


NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def target_part(source: str, target: str) -> str:
    part = posixpath.normpath(
        target.lstrip("/") if target.startswith("/")
        else posixpath.join(posixpath.dirname(source), target)
    )
    if part == ".." or part.startswith("../"):
        raise ValueError("relationship target leaves the package")
    return part


def relationships(package: ZipFile, source: str) -> dict[str, ET.Element]:
    part = posixpath.join(
        posixpath.dirname(source), "_rels", posixpath.basename(source) + ".rels"
    )
    if part not in package.namelist():
        return {}
    root = ET.fromstring(package.read(part))
    return {rel.attrib["Id"]: rel for rel in root.findall("pr:Relationship", NS)}


def notes_have_body(package: ZipFile, source: str) -> bool:
    for rel in relationships(package, source).values():
        if not rel.get("Type", "").endswith("/notesSlide"):
            continue
        if rel.get("TargetMode") == "External":
            raise ValueError("notes relationship must be internal")
        root = ET.fromstring(package.read(target_part(source, rel.attrib["Target"])))
        for shape in root.findall(".//p:sp", NS):
            placeholder = shape.find("p:nvSpPr/p:nvPr/p:ph", NS)
            if placeholder is None or placeholder.get("type") != "body":
                continue
            text = "".join(node.text or "" for node in shape.findall(".//a:t", NS))
            if text.strip():
                return True
    return False


def inspect_pptx(path: Path) -> dict:
    slides = []
    with ZipFile(path) as package:
        source = "ppt/presentation.xml"
        root = ET.fromstring(package.read(source))
        if root.tag != "{" + NS["p"] + "}presentation":
            raise ValueError("presentation.xml is not a PresentationML presentation")
        rels = relationships(package, source)
        for index, slide_id in enumerate(root.findall("p:sldIdLst/p:sldId", NS), 1):
            rel = rels[slide_id.attrib["{" + NS["r"] + "}id"]]
            if rel.get("TargetMode") == "External":
                raise ValueError("slide relationship must be internal")
            part = target_part(source, rel.attrib["Target"])
            slide = ET.fromstring(package.read(part))
            if slide.tag != "{" + NS["p"] + "}sld":
                raise ValueError("slide relationship does not target a slide")
            math_objects = [
                wrapper for wrapper in slide.findall(".//a14:m", NS)
                if any(len(math) > 0 for math in wrapper.findall(".//m:oMath", NS))
            ]
            fonts = sorted({
                node.attrib["typeface"]
                for tag in ("latin", "ea", "cs")
                for node in slide.findall(".//a:" + tag, NS)
                if node.get("typeface")
            })
            slides.append({
                "slide": index,
                "part": part,
                "native_equation_candidates": len(math_objects),
                "has_nonempty_notes_body": notes_have_body(package, part),
                "pictures": len(slide.findall(".//p:pic", NS)),
                "text_shapes": sum(
                    shape.find("p:txBody", NS) is not None
                    for shape in slide.findall(".//p:sp", NS)
                ),
                "tables": len(slide.findall(".//a:tbl", NS)),
                "declared_typefaces": fonts,
            })
    if not slides:
        raise ValueError("presentation contains no referenced slides")
    return {
        "file": str(path.resolve()),
        "scope": "Structural inspection only; no visual or PowerPoint editing verification",
        "slide_count": len(slides),
        "native_equation_candidates": sum(s["native_equation_candidates"] for s in slides),
        "slides": slides,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--expected-slides", type=int)
    parser.add_argument("--expected-equations", type=int)
    parser.add_argument("--require-notes", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    for name in ("expected_slides", "expected_equations"):
        value = getattr(args, name)
        if value is not None and value < 0:
            parser.error("expected counts must be nonnegative")
    errors = []
    try:
        report = inspect_pptx(args.pptx)
        if args.expected_slides is not None and report["slide_count"] != args.expected_slides:
            errors.append("slide count differs from the expected count")
        if (args.expected_equations is not None
                and report["native_equation_candidates"] < args.expected_equations):
            errors.append("native equation candidates are fewer than expected")
        if args.require_notes:
            missing = [str(s["slide"]) for s in report["slides"]
                       if not s["has_nonempty_notes_body"]]
            if missing:
                errors.append("missing nonempty notes body on slide(s): " + ", ".join(missing))
    except (OSError, BadZipFile, ET.ParseError, KeyError, ValueError) as exc:
        report = {"file": str(args.pptx), "scope": "Structural inspection only"}
        errors.append(str(exc))
    report["structural_checks_ok"] = not errors
    report["errors"] = errors
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        if args.json_out.resolve() == args.pptx.resolve():
            parser.error("JSON output must not overwrite the input PPTX")
        args.json_out.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
