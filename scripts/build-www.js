const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const wwwDir = path.join(rootDir, 'www');

// List of source files and directories to include in the www build bundle
const itemsToCopy = [
  'index.html',
  'src',
  'data',
  'stages',
  'assets'
];

console.log('Building www directory for Capacitor...');

// 1. Clean existing www directory if it exists
if (fs.existsSync(wwwDir)) {
  fs.rmSync(wwwDir, { recursive: true, force: true });
  console.log('Cleaned existing www/ directory.');
}

// 2. Recreate fresh www directory
fs.mkdirSync(wwwDir, { recursive: true });

// 3. Copy each item while preserving relative folder structure
itemsToCopy.forEach((item) => {
  const srcPath = path.join(rootDir, item);
  const destPath = path.join(wwwDir, item);

  if (fs.existsSync(srcPath)) {
    fs.cpSync(srcPath, destPath, { recursive: true });
    console.log(`  ✓ Copied ${item} -> www/${item}`);
  } else {
    console.warn(`  ⚠ Warning: ${item} not found at ${srcPath}`);
  }
});

console.log('\nBuild complete! All Web assets copied to www/');
