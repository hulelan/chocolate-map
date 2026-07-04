// Parses an approved GitHub issue body, validates the embedded pin-data,
// and appends a clean pin to data/pins.json. Writes step outputs for the workflow.
import { readFileSync, writeFileSync, appendFileSync } from 'node:fs';

const PINS_PATH = 'data/pins.json';

function out(key, value) {
  if (process.env.GITHUB_OUTPUT) {
    // Multiline-safe output using a heredoc delimiter
    const delim = 'EOF_' + Math.random().toString(36).slice(2);
    appendFileSync(process.env.GITHUB_OUTPUT, `${key}<<${delim}\n${value}\n${delim}\n`);
  }
  console.log(`${key}: ${value}`);
}

const body = process.env.ISSUE_BODY || '';

// Extract the machine-readable block: <!-- pin-data { ... } -->
const m = body.match(/<!--\s*pin-data\s*([\s\S]*?)-->/);
if (!m) {
  out('added', 'false');
  out('reason', 'No `pin-data` block found in the issue. It may have been created without the suggestion form.');
  process.exit(0);
}

let data;
try {
  data = JSON.parse(m[1].trim());
} catch (e) {
  out('added', 'false');
  out('reason', 'The `pin-data` block is not valid JSON, so it could not be parsed.');
  process.exit(0);
}

// Validate + sanitize every field (never trust issue input)
const name = String(data.name || '').trim().slice(0, 120);
const type = data.type === 'facility' ? 'facility' : 'farm';
const lat = Number(data.lat);
const lng = Number(data.lng);
const notes = String(data.notes || '').trim().slice(0, 2000);
const source = String(data.source || '').trim().slice(0, 120);

if (!name) { out('added', 'false'); out('reason', 'Missing a place name.'); process.exit(0); }
if (!Number.isFinite(lat) || !Number.isFinite(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
  out('added', 'false'); out('reason', 'Missing or out-of-range coordinates.'); process.exit(0);
}

let pins = [];
try { pins = JSON.parse(readFileSync(PINS_PATH, 'utf8')); } catch { pins = []; }

// Reject near-duplicates (same name within ~2km)
const dup = pins.find(p =>
  p.name.toLowerCase() === name.toLowerCase() &&
  Math.abs(p.lat - lat) < 0.02 && Math.abs(p.lng - lng) < 0.02);
if (dup) {
  out('added', 'false');
  out('reason', `A very similar pin already exists ("${dup.name}"). Not adding a duplicate.`);
  process.exit(0);
}

const id = 'c_' + Date.now().toString(36) + Math.floor(Math.random() * 1e5).toString(36);
const pin = { id, name, type, lat: +lat.toFixed(5), lng: +lng.toFixed(5), notes };
if (source) pin.source = source;

pins.push(pin);
writeFileSync(PINS_PATH, JSON.stringify(pins, null, 2) + '\n');

out('added', 'true');
out('reason', name);
out('name', name);
