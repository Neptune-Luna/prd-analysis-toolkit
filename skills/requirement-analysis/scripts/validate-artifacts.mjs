#!/usr/bin/env node
// Cross-platform artifact quality gate.
// Usage: node validate-artifacts.mjs <RUN_DIR> [--stage parse|extract|clarify|review|aggregate|all]

import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const runDir = process.env.RUN_DIR || args.find((arg) => !arg.startsWith("--"));
const stageIndex = args.indexOf("--stage");
const stage = stageIndex >= 0 ? args[stageIndex + 1] : "all";
const allowedStages = new Set(["parse", "extract", "clarify", "review", "aggregate", "all"]);

if (!runDir || !allowedStages.has(stage)) {
  console.error("Usage: node validate-artifacts.mjs <RUN_DIR> [--stage parse|extract|clarify|review|aggregate|all]");
  process.exit(2);
}

const checks = {
  parse: { file: "_parsed-content.md", required: ["# ", "## ", "["] },
  extract: {
    file: "_extraction.md",
    required: ["# ", "> ", "1.1", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "2.3", "2.4"],
  },
  clarify: {
    file: "_clarifications.md",
    required: ["# ", "## ", "| # |", "|---"],
    regex: [/\u6587\u6863\u6210\u719F\u5EA6/u, /\u963B\u585E/u, /\u5F71\u54CD\u8986\u76D6/u, /\u4F18\u5316\u5EFA\u8BAE/u],
  },
  review: {
    file: "_review.md",
    required: ["# ", "## ", "| # |", "|---"],
    regex: [/\u9700\u6C42\u7C7B\u578B/u, /\u6D41\u7A0B\u5408\u7406\u6027/u, /\u91CF\u5316/u, /\u9690\u6027\u9700\u6C42/u, /\u53D1\u8A00\u7A3F/u],
  },
  aggregate: {
    file: "final-report.md",
    required: ["# ", "## ", "| # |"],
    regex: [/\u9879\u76EE\u6982[\u89C8\u8FF0]/u, /\u9700\u6C42\u8403\u53D6/u, /\u5206\u6790\u4E0E\u8BC4\u4EF7/u, /\u6F84\u6E05/u, /\u8BC4\u5BA1/u],
  },
};

const placeholderPatterns = [
  /\[N\]/,
  /\[URL\]/,
  /\[[^\]\r\n]*[\uFF1A\uFF0C][^\]\r\n]*\]/u,
  /\[\u4F4D\u7F6E\]/u,
  /\[\u5177\u4F53\u4F4D\u7F6E\]/u,
  /\[\u5177\u4F53\u95EE\u9898\]/u,
  /\[\u539F\u578B\u4F4D\u7F6E\]/u,
  /\[\u63CF\u8FF0\]/u,
  /\[\u6458\u8981\]/u,
  /\[\u8DEF\u5F84\]/u,
  /\[\u65F6\u95F4\]/u,
  /\[\u5F53\u524D\u65F6\u95F4\]/u,
  /\[\u63A2\u7D22\u65F6\u95F4\]/u,
  /\[\u6587\u4EF6\u540D\]/u,
  /\[\u9879\u76EE\u540D\]/u,
  /\[\u89D2\u8272\u540D\]/u,
  /\[\u9875\u9762\u540D\]/u,
];
const markerPatterns = [/\*\*\*\s+(Add|Update|Delete)\s+File:/, /\*\*\*\s+(Begin|End)\s+Patch/];
const aggregateSummaryOnlyPatterns = [
  /完整(?:问句|清单)(?:和来源)?见\s*[`[]?_clarifications\.md/u,
  /澄清结论[\s\S]{0,800}重点包括/u,
];

function fail(message) {
  console.error(`Artifact validation FAILED: ${message}`);
  process.exit(1);
}

function validate(check, optional = false) {
  const filePath = path.join(path.resolve(runDir), check.file);
  if (!fs.existsSync(filePath)) {
    if (optional) return;
    fail(`Missing artifact: ${filePath}`);
  }
  const content = fs.readFileSync(filePath, "utf8");
  if (!content.trim()) fail(`Empty artifact: ${filePath}`);
  for (const marker of check.required) {
    if (!content.includes(marker)) fail(`${check.file} missing required marker: ${marker}`);
  }
  for (const pattern of check.regex || []) {
    if (!pattern.test(content)) fail(`${check.file} missing required section matching: ${pattern}`);
  }
  for (const pattern of placeholderPatterns) {
    if (pattern.test(content)) fail(`${check.file} contains unresolved placeholder: ${pattern}`);
  }
  for (const pattern of markerPatterns) {
    if (pattern.test(content)) fail(`${check.file} contains stray patch marker: ${pattern}`);
  }
  if (check.file === "final-report.md") {
    for (const pattern of aggregateSummaryOnlyPatterns) {
      if (pattern.test(content)) fail(`${check.file} summarizes clarification items instead of embedding details: ${pattern}`);
    }
  }
}

if (stage === "all") {
  validate(checks.parse, true);
  validate(checks.extract);
  validate(checks.clarify);
  validate(checks.review);
  validate(checks.aggregate);
} else {
  validate(checks[stage]);
}

console.log(`Artifact validation passed (${stage}): ${path.resolve(runDir)}`);
