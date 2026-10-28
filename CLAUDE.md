# Guardians of Gaia — Android app repo

Build wrapper only. The game is in the web repo (`guardians_web`), mounted as the git submodule
`web/`. **Never edit, copy or commit game files here** (`web/`, `www/` are not ours to change).
Bug in the game, phone layout, fonts, audio, Back-button logic (`src/native.js`)? Fix it in the web repo,
then `npm run update-web` here and commit the new `web` pin.

What belongs here: `android/` (manifest, gradle, MainActivity), `capacitor.config.json`,
`resources/` (icon/splash), `scripts/build-www.js`, `.github/workflows/android.yml`, README.

Facts:
- App id `com.gog.app` (permanent once on Play). Display name "Guardians of Gala" is intentional (do not rename).
- Orientation is **locked to landscape** (`sensorLandscape`); `MainActivity` also makes the window immersive (bars hidden,
  swipe shows them), keeps the screen on, and pauses/resumes the WebView with the activity.
- Version: `versionName` = `package.json` version, `versionCode` = `-PversionCode` or `GITHUB_RUN_NUMBER` or 1.
- Play Store requirements and owner actions: `PLAY-STORE-CHECKLIST.md`.
- `MainActivity` relaxes the WebView media-gesture rule; the game still asks for a first tap.
- Release builds fail without the keystore (`-PallowUnsignedRelease` for throw-away local tests). Signing reads `KEYSTORE_PATH`/`KEYSTORE_PASSWORD`/`KEY_ALIAS`/`KEY_PASSWORD` from the
  environment (GitHub secrets). Never commit keystores.
- `www/` is generated (`npm run build`) and gitignored; it also gets `version.txt` with the web commit.
