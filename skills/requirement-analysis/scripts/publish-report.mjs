#!/usr/bin/env node
// Publish the timestamped final report to a stable, easy-to-find project folder.
// Usage: node publish-report.mjs <RUN_DIR> <PROJECT_NAME> [PROJECT_ROOT]

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const [, , runDirArg, projectNameArg, projectRootArg] = process.argv;

if (!runDirArg || !projectNameArg) {
  console.error("Usage: node publish-report.mjs <RUN_DIR> <PROJECT_NAME> [PROJECT_ROOT]");
  process.exit(2);
}

const runDir = path.resolve(runDirArg);
const projectRoot = path.resolve(projectRootArg || process.cwd());
const source = path.join(runDir, "final-report.md");

if (!fs.existsSync(source) || !fs.statSync(source).isFile()) {
  console.error(`Publish failed: missing final report: ${source}`);
  process.exit(1);
}

const cleanName = projectNameArg
  .normalize("NFC")
  .replace(/[<>:"/\\|?*\u0000-\u001F]/g, "-")
  .replace(/[.\s]+$/g, "")
  .trim()
  .replace(/-需求分析$/u, "");

if (!cleanName) {
  console.error("Publish failed: project name becomes empty after filename sanitization.");
  process.exit(1);
}

const publishDir = path.join(projectRoot, "需求分析");
const destination = path.join(publishDir, `${cleanName}-需求分析.md`);
const relativeDestination = path.relative(projectRoot, destination);

if (relativeDestination.startsWith("..") || path.isAbsolute(relativeDestination)) {
  console.error(`Publish failed: destination escapes project root: ${destination}`);
  process.exit(1);
}

fs.mkdirSync(publishDir, { recursive: true });
const overwritten = fs.existsSync(destination);
fs.copyFileSync(source, destination);

const digest = (filePath) => crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
const sourceHash = digest(source);
const destinationHash = digest(destination);

if (sourceHash !== destinationHash) {
  console.error(`Publish failed: copied file hash mismatch: ${destination}`);
  process.exit(1);
}

console.log(JSON.stringify({
  source,
  destination,
  overwritten,
  size: fs.statSync(destination).size,
  sha256: destinationHash,
}, null, 2));
