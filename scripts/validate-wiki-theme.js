import fs from "node:fs";
import path from "node:path";

const htmlDir = path.join(process.cwd(), "wiki_html");
const files = fs.readdirSync(htmlDir).filter((name) => name.endsWith(".html")).sort();
const required = [
  ['id="theme-init"', "early initializer"],
  [':root[data-theme="dark"]', "dark token overrides"],
  ['class="theme-toggle"', "theme toggle"],
  ['id="theme-controller"', "theme controller"],
  ["knowledge-vault-theme", "shared storage key"],
];
const failures = [];

for (const name of files) {
  const html = fs.readFileSync(path.join(htmlDir, name), "utf8");
  for (const [needle, label] of required) {
    if (!html.includes(needle)) failures.push(`${name}: missing ${label}`);
  }
  const init = html.indexOf('id="theme-init"');
  const style = html.search(/<style>/i);
  const body = html.search(/<body/i);
  if (!(init > -1 && init < style && style < body)) failures.push(`${name}: initializer must appear before styles and body`);
}

if (failures.length) {
  console.error("Theme validation failed:");
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Theme validation passed for ${files.length} HTML files`);
