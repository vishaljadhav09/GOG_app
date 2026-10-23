# Guardians of Gaia — Android app (build wrapper)

This repo only contains what is needed to package the game as an Android APK/AAB
(Capacitor + GitHub Actions). **The game itself is not in this repo.** It lives in the web repo,
[`guardians_web`](https://github.com/vishaljadhav09/guardians_web), and is pulled in here as a git
submodule at `web/`.

| Where | What |
|-------|------|
| `web/` | Submodule → the game (pinned to an exact commit). **Never edit files here.** |
| `android/` | Capacitor Android project (manifest, gradle, `MainActivity.java`) |
| `capacitor.config.json` | App id, name, colours |
| `resources/` | `icon.png` / `splash.png` source art (`scripts/generate_assets.py`) |
| `scripts/build-www.js` | Copies `web/{index.html,src,data,stages}` → `www/` (Capacitor `webDir`) |
| `.github/workflows/android.yml` | Debug APK on every push; signed APK + AAB on `v*` tags |

## Daily workflow

1. Change the game **in the web repo** and push it.
2. Here, pull the newest game and commit the new pin:
   ```sh
   npm run update-web
   git add web && git commit -m "Update game to <what changed>" && git push
   ```
3. GitHub Actions builds the debug APK → Actions tab → run → Artifacts. The run summary shows
   which web commit is inside it.

Android-only changes (icon, manifest, gradle, status bar, app name) are made here.

## First clone

```sh
git clone --recurse-submodules https://github.com/vishaljadhav09/GOG_app.git
cd GOG_app && npm ci
npm run build          # web/ → www/
npx cap sync android   # www/ → android project
```
Forgot `--recurse-submodules`? `git submodule update --init`.

## Release

1. Bump `versionCode` and `versionName` in `android/app/build.gradle`.
2. `git tag vX.Y.Z && git push --tags` (the tag must equal `v<versionName>`).
3. The release job builds the signed APK + AAB from the web commit pinned at that tag.

Repo secrets: `KEYSTORE_B64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`.
Keep a backup of the keystore; without it the Play Store app cannot be updated. Never commit it.

To try an unreleased web branch without bumping the pin: Actions → *Build Android APK* →
*Run workflow* → fill `web_ref`.
