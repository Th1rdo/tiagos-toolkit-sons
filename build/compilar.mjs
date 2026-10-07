// Compila packs/_source/sons/*.json num LevelDB (formato de compêndio do Foundry v11+).
import { ClassicLevel } from "classic-level";
import fs from "node:fs";
import path from "node:path";
const raiz = path.resolve(import.meta.dirname, "..");
const fonte = path.join(raiz, "packs/_source/sons");
const destino = path.join(raiz, "packs/sons");
fs.rmSync(destino, { recursive: true, force: true });
fs.mkdirSync(destino, { recursive: true });
const db = new ClassicLevel(destino, { keyEncoding: "utf8", valueEncoding: "json" });
await db.open();
const lote = db.batch(); let n = 0;
for (const f of fs.readdirSync(fonte).filter(f => f.endsWith(".json"))) {
  const doc = JSON.parse(fs.readFileSync(path.join(fonte, f), "utf8"));
  const chave = doc._key; delete doc._key;
  lote.put(chave, doc); n++;
}
await lote.write();
await db.compactRange("!", "~");
await db.close();
fs.rmSync(path.join(destino, "LOCK"), { force: true });
console.log(`sons: ${n} documentos`);
