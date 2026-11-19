// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The program copies POST.json — the address of the X post that carries
// this repository's GTA 6 meme — from the repository root into /output,
// where the gate reads it. The post itself is the entry: the house reads
// it from X (its first picture, then its text) and hands that to the judge,
// so nothing this program writes about the post is judged. POST.json ships
// with a placeholder address until the meme is posted on X; the finalize
// step replaces it with the real post address before submit.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const src = join(botDir, "POST.json");
const post = JSON.parse(readFileSync(src, "utf8"));
if (typeof post.url !== "string" || !post.url.startsWith("https://")) {
  throw new Error(`POST.json holds no https post address: ${JSON.stringify(post)}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "POST.json"));
