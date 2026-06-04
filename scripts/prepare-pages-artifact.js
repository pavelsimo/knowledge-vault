import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const sourceDir = path.join(root, "wiki_html");
const rawDir = path.join(root, "raw");
const artifactDir = path.join(root, ".pages-artifact");
const artifactRawDir = path.join(artifactDir, "assets", "raw");

const imageSrcPattern = /(<img\s+[^>]*?src=")\.\.\/raw\/([^"#?]+)(["#?])/g;

function assertInside(parent, child, label) {
  const relative = path.relative(parent, child);
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`${label} resolves outside ${path.relative(root, parent) || "."}: ${child}`);
  }
}

function copyDirectory(source, destination) {
  fs.rmSync(destination, { recursive: true, force: true });
  fs.cpSync(source, destination, { recursive: true });
}

function rewriteHtmlFiles() {
  const missing = [];
  const copied = new Set();
  let rewrittenRefs = 0;
  let changedFiles = 0;

  const htmlFiles = fs
    .readdirSync(artifactDir)
    .filter((name) => name.endsWith(".html"))
    .map((name) => path.join(artifactDir, name));

  for (const file of htmlFiles) {
    const original = fs.readFileSync(file, "utf8");
    const updated = original.replace(imageSrcPattern, (match, prefix, encodedRawPath, suffix) => {
      const decodedRawPath = decodeURIComponent(encodedRawPath);
      const sourceImage = path.join(rawDir, decodedRawPath);
      const artifactImage = path.join(artifactRawDir, decodedRawPath);

      assertInside(rawDir, sourceImage, "Image source");
      assertInside(artifactRawDir, artifactImage, "Artifact image");

      if (!fs.existsSync(sourceImage)) {
        missing.push(`${path.relative(root, file)} -> raw/${decodedRawPath}`);
      } else if (!copied.has(artifactImage)) {
        fs.mkdirSync(path.dirname(artifactImage), { recursive: true });
        fs.copyFileSync(sourceImage, artifactImage);
        copied.add(artifactImage);
      }

      rewrittenRefs += 1;
      return `${prefix}assets/raw/${encodedRawPath}${suffix}`;
    });

    if (updated !== original) {
      fs.writeFileSync(file, updated);
      changedFiles += 1;
    }
  }

  if (missing.length > 0) {
    console.error("Missing raw image assets referenced by wiki_html:");
    for (const item of missing) {
      console.error(`- ${item}`);
    }
    process.exit(1);
  }

  console.log(`Prepared ${path.relative(root, artifactDir)} from wiki_html`);
  console.log(`Rewritten image references: ${rewrittenRefs}`);
  console.log(`HTML files changed in artifact: ${changedFiles}`);
  console.log(`Raw image files copied into artifact: ${copied.size}`);
}

copyDirectory(sourceDir, artifactDir);
fs.rmSync(artifactRawDir, { recursive: true, force: true });
rewriteHtmlFiles();
