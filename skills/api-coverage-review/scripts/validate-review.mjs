#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const runDirArg = process.argv[2];

if (!runDirArg) {
  console.error("用法: node validate-review.mjs <RUN_DIR>");
  process.exit(2);
}

const runDir = path.resolve(runDirArg);
const errors = [];

function readRequired(fileName) {
  const filePath = path.join(runDir, fileName);
  if (!fs.existsSync(filePath)) {
    errors.push(`缺少必需文件: ${fileName}`);
    return "";
  }

  const stat = fs.statSync(filePath);
  if (!stat.isFile() || stat.size === 0) {
    errors.push(`文件为空或不是普通文件: ${fileName}`);
    return "";
  }

  return fs.readFileSync(filePath, "utf8");
}

function requireMarkers(fileName, content, markers) {
  for (const marker of markers) {
    if (!content.includes(marker)) {
      errors.push(`${fileName} 缺少标记: ${marker}`);
    }
  }
}

function rejectPlaceholders(fileName, content) {
  const patterns = [
    { label: "[N]", regex: /\[N\]/i },
    { label: "[URL]", regex: /\[URL\]/i },
    { label: "TODO", regex: /\bTODO\b/i },
    { label: "TBD", regex: /\bTBD\b/i },
    { label: "补丁标记", regex: /^(?:<{7}|={7}|>{7})/m },
  ];

  for (const { label, regex } of patterns) {
    if (regex.test(content)) {
      errors.push(`${fileName} 含未解决占位或冲突内容: ${label}`);
    }
  }
}

if (!fs.existsSync(runDir) || !fs.statSync(runDir).isDirectory()) {
  console.error(`运行目录不存在或不是目录: ${runDir}`);
  process.exit(2);
}

const matrixName = "traceability-matrix.md";
const reportName = "final-report.md";
const matrix = readRequired(matrixName);
const report = readRequired(reportName);

if (matrix) {
  requireMarkers(matrixName, matrix, [
    "# ",
    "需求ID",
    "技术证据",
    "用例ID",
    "设计覆盖结论",
    "运行态结论",
  ]);
  if (!/\|\s*RQ-\d+/i.test(matrix)) {
    errors.push(`${matrixName} 至少需要一条 RQ 编号的矩阵记录`);
  }
  if (!/(?:满足|部分满足|不满足|无法判断|无需求依据|技术超范围)/.test(matrix)) {
    errors.push(`${matrixName} 未使用规定的设计覆盖结论`);
  }
  if (!/(?:已验证|未验证|验证失败)/.test(matrix)) {
    errors.push(`${matrixName} 未使用规定的运行态结论`);
  }
  rejectPlaceholders(matrixName, matrix);
}

if (report) {
  requireMarkers(reportName, report, [
    "# ",
    "## ",
    "执行结论",
    "覆盖统计",
    "接口评审",
    "差异与风险",
    "运行态验证",
    "来源",
  ]);
  rejectPlaceholders(reportName, report);
}

if (errors.length > 0) {
  console.error("一致性评审产物校验失败：");
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`一致性评审产物校验通过: ${runDir}`);

