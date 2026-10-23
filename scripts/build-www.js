// Builds www/ (the Capacitor webDir) from the game in the `web/` git submodule.
// The game lives ONLY in the web repo; nothing from it is committed in this repo.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const rootDir = path.resolve(__dirname, '..');
const webDir = path.join(rootDir, 'web');
const wwwDir = path.join(rootDir, 'www');

// Game files that make up the shipped bundle (paths relative to web/).
const itemsToCopy = ['index.html', 'src', 'data', 'stages'];

if (!fs.existsSync(path.join(webDir, 'index.html'))) {
  console.error(
    'web/ is empty or missing. Fetch the game first:\n' +
    '  git submodule update --init web'
  );
  process.exit(1);
}

console.log('Building www/ from the web submodule...');

if (fs.existsSync(wwwDir)) {
  fs.rmSync(wwwDir, { recursive: true, force: true });
}
fs.mkdirSync(wwwDir, { recursive: true });

for (const item of itemsToCopy) {
  const src = path.join(webDir, item);
  if (!fs.existsSync(src)) {
    console.error(`Missing web/${item}: the web repo layout changed. Update scripts/build-www.js.`);
    process.exit(1);
  }
  fs.cpSync(src, path.join(wwwDir, item), { recursive: true });
  console.log(`  copied web/${item} -> www/${item}`);
}

// Record which game version this bundle contains (shown in CI summary / in-app debugging).
let sha = 'unknown';
try {
  sha = execSync('git rev-parse HEAD', { cwd: webDir }).toString().trim();
} catch (e) { /* not a git checkout; keep "unknown" */ }
fs.writeFileSync(path.join(wwwDir, 'version.txt'), `web ${sha}\n`);

console.log(`\nDone. Game version: web ${sha.slice(0, 7)}`);
