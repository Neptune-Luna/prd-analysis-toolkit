# -*- coding: utf-8 -*-
"""Generate XMind test cases with the required seven-level hierarchy.

Hierarchy:
    所属目录 -> 所属页面 -> 功能点 -> 测试场景 -> 前置条件 -> 操作步骤 -> 预期结果

Cases sharing directory, page, feature point, and scenario are grouped under
the same nodes. The input may be a flat case array or the section-based JSON
used by PrdToTestCaseProject.
"""

import argparse
import json
import os
import re
import struct
import uuid
import zipfile
import zlib
from collections import OrderedDict
from datetime import datetime


def new_id():
    return str(uuid.uuid4())


def topic(title, children=None, *, root=False, folded=False, notes=None):
    value = {
        "id": new_id(),
        "class": "topic",
        "title": title,
        "titleUnedited": True,
    }
    if root:
        value["structureClass"] = "org.xmind.ui.map.unbalanced"
    if children:
        value["children"] = {"attached": children}
        if folded:
            value["branch"] = "folded"
    if notes:
        value["notes"] = {"plain": {"content": notes}}
    return value


def tiny_png():
    def chunk(name, payload):
        raw = struct.pack(">I", len(payload)) + name + payload
        return raw + struct.pack(">I", zlib.crc32(name + payload) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"\x00\xFF\xFF\xFF"))
        + chunk(b"IEND", b"")
    )


def theme():
    return {
        "map": {
            "id": new_id(),
            "properties": {"svg:fill": "#FFFFFF", "line-tapered": "none"},
        },
        "centralTopic": {
            "id": new_id(),
            "properties": {
                "fo:font-family": "NeverMind",
                "fo:font-size": "24pt",
                "fo:font-weight": "600",
                "svg:fill": "#233ED9",
                "fill-pattern": "solid",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedfold",
            },
        },
        "mainTopic": {
            "id": new_id(),
            "properties": {
                "fo:font-family": "NeverMind",
                "fo:font-size": "16pt",
                "fo:font-weight": "600",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
            },
        },
        "subTopic": {
            "id": new_id(),
            "properties": {
                "fo:font-family": "NeverMind",
                "fo:font-size": "12pt",
                "fo:font-weight": "400",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-class": "org.xmind.branchConnection.roundedElbow",
            },
        },
    }


def clean_feature_name(value):
    return re.sub(r"^\(\d+\)\s*", "", str(value or "").strip())


def flatten_cases(data):
    if isinstance(data, list):
        project = "测试用例"
        cases = data
    elif isinstance(data, dict) and isinstance(data.get("sections"), list):
        project = data.get("project") or "测试用例"
        cases = []
        for section in data["sections"]:
            for feature in section.get("feature_points", []):
                feature_name = clean_feature_name(feature.get("name"))
                for item in feature.get("cases", []):
                    case = dict(item)
                    case.setdefault("feature_point", feature_name)
                    case.setdefault("test_scenario", case.get("title"))
                    cases.append(case)
    elif isinstance(data, dict):
        project = data.get("project") or "测试用例"
        cases = data.get("testcases") or data.get("cases") or []
    else:
        raise ValueError("输入 JSON 必须是用例数组或包含 sections/testcases/cases 的对象")

    if not cases:
        raise ValueError("输入 JSON 中没有测试用例")
    return project, cases


def required_text(case, key, fallback=None):
    value = case.get(key)
    if (value is None or str(value).strip() == "") and fallback:
        value = case.get(fallback)
    value = "" if value is None else str(value).strip()
    if not value:
        raise ValueError(f"用例缺少必填字段 {key}: {case.get('title', '<无标题>')}")
    return value


def group_cases(cases):
    grouped = OrderedDict()
    for case in cases:
        directory = required_text(case, "directory")
        page = required_text(case, "page")
        feature = required_text(case, "feature_point")
        scenario = required_text(case, "test_scenario", "title")
        preconditions = required_text(case, "preconditions")
        steps = required_text(case, "steps")
        expected = required_text(case, "expected")
        level = str(case.get("level") or "").strip()

        by_page = grouped.setdefault(directory, OrderedDict())
        by_feature = by_page.setdefault(page, OrderedDict())
        by_scenario = by_feature.setdefault(feature, OrderedDict())
        entries = by_scenario.setdefault(scenario, [])
        entries.append(
            {
                "preconditions": preconditions,
                "steps": steps,
                "expected": expected,
                "level": level,
            }
        )
    return grouped


def build_tree(project, grouped, source_note=None):
    directory_nodes = []
    for directory, pages in grouped.items():
        page_nodes = []
        for page, features in pages.items():
            feature_nodes = []
            for feature, scenarios in features.items():
                scenario_nodes = []
                for scenario, entries in scenarios.items():
                    levels = sorted({entry["level"] for entry in entries if entry["level"]})
                    level_suffix = f"（{'/'.join(levels)}）" if levels else ""
                    precondition_nodes = []
                    for entry in entries:
                        expected_node = topic(f"预期结果：\n{entry['expected']}")
                        steps_node = topic(
                            f"操作步骤：\n{entry['steps']}",
                            children=[expected_node],
                        )
                        precondition_nodes.append(
                            topic(
                                f"前置条件：{entry['preconditions']}",
                                children=[steps_node],
                            )
                        )
                    scenario_nodes.append(
                        topic(
                            f"测试场景：{scenario}{level_suffix}",
                            children=precondition_nodes,
                            folded=True,
                        )
                    )
                feature_nodes.append(
                    topic(f"功能点：{feature}", children=scenario_nodes, folded=True)
                )
            page_nodes.append(
                topic(f"所属页面：{page}", children=feature_nodes, folded=True)
            )
        directory_nodes.append(
            topic(f"所属目录：{directory}", children=page_nodes, folded=True)
        )
    return topic(project, children=directory_nodes, root=True, notes=source_note)


def write_xmind(output_path, root_topic):
    content = [
        {
            "id": new_id(),
            "revisionId": new_id(),
            "class": "sheet",
            "rootTopic": root_topic,
            "title": "测试用例",
            "topicOverlapping": "overlap",
            "arrangeableLayerOrder": [root_topic["id"]],
            "zones": [],
            "extensions": [
                {
                    "provider": "org.xmind.ui.skeleton.structure.style",
                    "content": {"centralTopic": "org.xmind.ui.map.unbalanced"},
                }
            ],
            "theme": theme(),
        }
    ]
    metadata = {
        "dataStructureVersion": "3",
        "creator": {"name": "XMind", "version": "23.11.3682"},
        "layoutEngineVersion": "5",
    }
    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
            "manifest.json": {},
            "Thumbnails/thumbnail.png": {},
        }
    }
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        archive.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False))
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False))
        archive.writestr("Thumbnails/thumbnail.png", tiny_png())


def validate_xmind(output_path, expected_cases, expected_scenarios):
    required_entries = {
        "content.json",
        "metadata.json",
        "manifest.json",
        "Thumbnails/thumbnail.png",
    }
    prefixes = {
        1: "所属目录：",
        2: "所属页面：",
        3: "功能点：",
        4: "测试场景：",
        5: "前置条件：",
        6: "操作步骤：",
        7: "预期结果：",
    }
    old_categories = {
        "基础功能用例",
        "异常功能用例",
        "边界值用例",
        "接口交互用例",
        "数据校验用例",
        "权限校验用例",
        "兼容性用例",
        "恢复/异常场景用例",
    }
    counts = {depth: 0 for depth in range(1, 8)}
    errors = []

    with zipfile.ZipFile(output_path) as archive:
        names = set(archive.namelist())
        missing_entries = required_entries - names
        if missing_entries:
            errors.append(f"XMind 缺少文件: {sorted(missing_entries)}")
        content = json.loads(archive.read("content.json").decode("utf-8"))

    root_topic = content[0]["rootTopic"]

    def walk(node, depth):
        if depth > 0:
            if depth > 7:
                errors.append(f"存在超过七级的节点: {node.get('title')}")
            else:
                counts[depth] += 1
                title = node.get("title", "")
                if not title.startswith(prefixes[depth]):
                    errors.append(f"第 {depth} 级节点前缀错误: {title}")
                if title in old_categories:
                    errors.append(f"存在旧版分类节点: {title}")
        children = node.get("children", {}).get("attached", [])
        if depth == 7 and children:
            errors.append("预期结果节点下存在多余子节点")
        for child in children:
            walk(child, depth + 1)

    walk(root_topic, 0)
    if counts[4] != expected_scenarios:
        errors.append(f"测试场景节点数 {counts[4]} != 唯一分组数 {expected_scenarios}")
    for depth in (5, 6, 7):
        if counts[depth] != expected_cases:
            errors.append(f"第 {depth} 级节点数 {counts[depth]} != 用例数 {expected_cases}")
    if errors:
        raise ValueError("; ".join(errors[:20]))
    return {
        "directories": counts[1],
        "pages": counts[2],
        "feature_points": counts[3],
        "scenarios": counts[4],
        "case_chains": counts[7],
        "hierarchy_errors": 0,
    }


def safe_name(value):
    return re.sub(r'[/\\:*?"<>|]', "", value)


def main():
    parser = argparse.ArgumentParser(description="生成七级分组结构的 XMind 测试用例")
    parser.add_argument("input", help="测试用例 JSON")
    parser.add_argument("--output", help="输出 .xmind 路径")
    parser.add_argument("--force", action="store_true", help="允许覆盖指定输出文件")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as source:
        data = json.load(source)
    project, cases = flatten_cases(data)
    grouped = group_cases(cases)

    if args.output:
        output = os.path.abspath(args.output)
    else:
        name = safe_name(project)
        output = os.path.abspath(os.path.join("test-cases", name, f"{name}.xmind"))

    if os.path.exists(output) and not args.force:
        stem, ext = os.path.splitext(output)
        output = f"{stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"

    root = build_tree(project, grouped, data.get("test_address") if isinstance(data, dict) else None)
    write_xmind(output, root)
    scenario_count = sum(
        len(scenarios)
        for pages in grouped.values()
        for features in pages.values()
        for scenarios in features.values()
    )
    validation = validate_xmind(output, len(cases), scenario_count)
    print(
        json.dumps(
            {
                "output": output,
                "cases": len(cases),
                "hierarchy": "所属目录-所属页面-功能点-测试场景-前置条件-操作步骤-预期结果",
                "validation": validation,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
