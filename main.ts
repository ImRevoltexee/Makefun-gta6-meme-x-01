// gta6-meme-x-01 entrypoint (Node 22, standard library only).
// Reads POST.json at the repository root, checks it names an X post,
// and writes it to /output/POST.json for the gate to read.
// The post itself is the entry: the house fetches it from X and
// judges its first picture plus its text. This program's output
// is never judged; it only hands the post's address to the gate.
//
// Local check: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const raw = readFileSync(join(botDir, 'POST.json'), 'utf8');
const post = JSON.parse(raw) as { url?: unknown };
const X_POST = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/(status|statuses)\/\d+|^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/i\/web\/status\/\d+/;
if (typeof post.url !== 'string' || !X_POST.test(post.url)) {
  console.error('POST.json does not name an X post URL');
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'POST.json'), JSON.stringify(post) + '\n');
console.log(`entry post: ${post.url}`);
