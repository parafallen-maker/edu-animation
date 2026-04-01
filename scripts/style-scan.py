#!/usr/bin/env python3
"""
style-scan.py — Static style compliance scanner for Manim scene files.

Scans all .py files in a project directory against design system rules.
Outputs Markdown report with severity levels.

Usage:
    python3 style-scan.py <project-dir> [--output report.md]
"""

import re
import os
import sys
import glob


def get_arg(flag):
    idx = sys.argv.index(flag) if flag in sys.argv else -1
    return sys.argv[idx + 1] if idx != -1 and idx + 1 < len(sys.argv) else None


class Issue:
    def __init__(self, severity, filepath, line_num, message, fix):
        self.severity = severity
        self.filepath = filepath
        self.line_num = line_num
        self.message = message
        self.fix = fix

    @property
    def icon(self):
        return {"critical": "🔴", "important": "🟡", "minor": "🟢"}.get(self.severity, "⚪")

    def __str__(self):
        return f"{self.icon} [{self.severity.upper()}] {self.filepath}:{self.line_num} — {self.message}\n   Fix: {self.fix}"


# ── Extract approved palette from design_system.py ──
def extract_palette(project_dir):
    ds_path = os.path.join(project_dir, "design_system.py")
    if not os.path.exists(ds_path):
        return set(["#000000", "#ffffff", "#fff", "#000"])

    content = open(ds_path).read()
    hex_colors = set(re.findall(r'"(#[0-9a-fA-F]{3,6})"', content))
    hex_colors.update(["#000000", "#ffffff", "#fff", "#000"])
    return hex_colors


# ── Scan a single file ──
def scan_file(filepath, approved_palette, project_dir):
    issues = []
    try:
        lines = open(filepath).readlines()
    except Exception as e:
        issues.append(Issue("important", filepath, 0, f"Cannot read file: {e}", ""))
        return issues

    rel_path = os.path.relpath(filepath, project_dir)
    has_ds_import = False

    for i, line in enumerate(lines):
        ln = i + 1
        stripped = line.strip()

        # Skip comments and imports
        if stripped.startswith("#") or stripped.startswith("import") or stripped.startswith("from"):
            if "design_system" in stripped or "design system" in stripped:
                has_ds_import = True
            continue
        if stripped.startswith('"""') or stripped.startswith("'''"):
            continue

        # ── 1. Hardcoded colors ──
        hex_matches = re.findall(r'"(#[0-9a-fA-F]{3,6})"', stripped)
        hex_matches += re.findall(r"'(#[0-9a-fA-F]{3,6})'", stripped)
        for h in hex_matches:
            if h.lower() not in approved_palette:
                issues.append(Issue(
                    "important", rel_path, ln,
                    f'Color "{h}" not in approved palette',
                    "Use color from design_system.py T class instead"
                ))

        # ── 2. Hardcoded font_size ──
        fs_matches = re.findall(r'font_size\s*=\s*(\d+)', stripped)
        allowed_sizes = {13, 16, 20, 24, 36, 56}
        for fs_str in fs_matches:
            fs = int(fs_str)
            if fs < 13:
                issues.append(Issue(
                    "critical", rel_path, ln,
                    f"font_size={fs} below absolute minimum (13)",
                    "Increase to at least 13"
                ))
            elif fs not in allowed_sizes and fs > 0:
                issues.append(Issue(
                    "minor", rel_path, ln,
                    f"font_size={fs} not in standard scale (13,16,20,24,36,56)",
                    f"Consider using T.H1(56), T.H2(36), T.H3(24), T.H4(20), T.BODY_S(16), T.CAP(13)"
                ))

        # ── 3. Direct mobject property changes without Animation ──
        # Warn about direct .set_color() / .move_to() outside play()
        if re.search(r'\.\s*set_(color|fill|stroke|opacity)\s*\(', stripped):
            issues.append(Issue(
                "minor", rel_path, ln,
                "Direct property change detected — consider wrapping in self.play()",
                "Use self.play(mobject.animate.set_color(...), ...)"
            ))

        # ── 4. Hardcoded corner_radius ──
        cr_matches = re.findall(r'corner_radius\s*=\s*([0-9.]+)', stripped)
        allowed_cr = {0.05, 0.1, 0.2, 0.3, 0.5}
        for cr_str in cr_matches:
            cr = float(cr_str)
            if cr not in allowed_cr:
                issues.append(Issue(
                    "minor", rel_path, ln,
                    f"corner_radius={cr} not in standard set ({sorted(allowed_cr)})",
                    "Use one of T.RADIUS values: 0.05, 0.1, 0.2, 0.3, 0.5"
                ))

        # ── 5. Hardcoded stroke_width ──
        sw_matches = re.findall(r'stroke_width\s*=\s*(\d+)', stripped)
        allowed_sw = {1, 2, 3, 4}
        for sw_str in sw_matches:
            sw = int(sw_str)
            if sw not in allowed_sw:
                issues.append(Issue(
                    "minor", rel_path, ln,
                    f"stroke_width={sw} not in standard set ({sorted(allowed_sw)})",
                    "Use one of T.STROKE values: 1, 2, 3, 4"
                ))

        # ── 6. wait(0) warning ──
        if re.search(r'\.wait\s*\(\s*0\s*\)', stripped):
            issues.append(Issue(
                "important", rel_path, ln,
                "self.wait(0) — zero wait may cause timing issues",
                "Set wait duration to match audio gap, or remove if unnecessary"
            ))

        # ── 7. Extremely long wait ──
        wait_matches = re.findall(r'\.wait\s*\(\s*([\d.]+)\s*\)', stripped)
        for w_str in wait_matches:
            w = float(w_str)
            if w > 15:
                issues.append(Issue(
                    "important", rel_path, ln,
                    f"self.wait({w}) — very long wait, verify this matches audio",
                    "Check audio duration; consider splitting into sub-animations"
                ))

    # ── 8. Missing design_system import ──
    if not has_ds_import and filepath.endswith(".py"):
        basename = os.path.basename(filepath)
        if basename not in ("design_system.py", "__init__.py"):
            issues.append(Issue(
                "critical", rel_path, 0,
                "No design_system import found — risk of hardcoded values",
                "Add: from design_system import *"
            ))

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 style-scan.py <project-dir> [--output report.md]")
        sys.exit(1)

    project_dir = sys.argv[1]
    output_path = get_arg("--output")

    if not os.path.isdir(project_dir):
        print(f"[ERROR] Not a directory: {project_dir}")
        sys.exit(1)

    palette = extract_palette(project_dir)
    py_files = glob.glob(os.path.join(project_dir, "*.py"))
    py_files = [f for f in py_files if os.path.basename(f) != "design_system.py"]

    if not py_files:
        print("[WARN] No .py files found to scan")
        sys.exit(0)

    all_issues = []
    for f in sorted(py_files):
        all_issues.extend(scan_file(f, palette, project_dir))

    # Count by severity
    critical = [i for i in all_issues if i.severity == "critical"]
    important = [i for i in all_issues if i.severity == "important"]
    minor = [i for i in all_issues if i.severity == "minor"]

    # Generate report
    report_lines = [
        "# Style Scan Report\n",
        f"**Project**: `{project_dir}`",
        f"**Files scanned**: {len(py_files)}",
        f"**Issues found**: 🔴 {len(critical)} critical · 🟡 {len(important)} important · 🟢 {len(minor)} minor",
        "",
    ]

    if critical:
        report_lines.append("## 🔴 Critical Issues\n")
        for issue in critical:
            report_lines.append(f"- {issue}")
        report_lines.append("")

    if important:
        report_lines.append("## 🟡 Important Issues\n")
        for issue in important:
            report_lines.append(f"- {issue}")
        report_lines.append("")

    if minor:
        report_lines.append("## 🟢 Minor Issues\n")
        for issue in minor:
            report_lines.append(f"- {issue}")
        report_lines.append("")

    if not all_issues:
        report_lines.append("✅ **All checks passed!**\n")

    report = "\n".join(report_lines)

    if output_path:
        with open(output_path, "w") as f:
            f.write(report)
        print(f"[OK] Report written to {output_path}")
    else:
        print(report)

    sys.exit(1 if critical else 0)


if __name__ == "__main__":
    main()
