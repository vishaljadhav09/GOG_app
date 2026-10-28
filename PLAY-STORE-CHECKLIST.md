# Google Play release checklist — Guardians of Gala (`com.gog.app`)

Status as of 2026-10-23. "Verified" below means checked in the files of this repo; **nothing in the
"needs a device / SDK" column could be tested when this was written** (no Android SDK, no phone, Java 17 only).
Google's dates and thresholds change; re-check the Play Console "Policy status" and "App content" pages before
submitting. Dates in section 1 are the ones given in the project brief.

Legend: **Done** = implemented in this repo | **Owner** = needs a human decision/account action |
**Follow-up** = optional or must be proven on a device first.

## 1. Technical requirements

| Requirement | Status | Notes |
|---|---|---|
| Target API 36 (Android 16) for new apps and updates, deadline 2026-08-31 | **Done** | `variables.gradle`: `compileSdk`/`targetSdk` 36, `minSdk` 24. |
| Android App Bundle (`.aab`) upload | **Done** | CI `release` job runs `bundleRelease` on `v*` tags. `bundle {}` splits by density + ABI, not language. |
| 16 KB memory page size (targetSdk 35+ apps with native code, deadline 2027-02-01) | **Done** (no native code) | The app and Capacitor 8.5 / App 8.1 / Status Bar 8.0 plugins ship no `.so`. CI lists `.so` files in the AAB (expects "none"). AGP 8.13 aligns any future libs. |
| Signed with an upload key; Play App Signing enabled | **Owner** | Create the keystore once, keep 2 offline backups, add the 4 repo secrets (section 4). Release builds now **fail** without it. |
| Unique, increasing `versionCode` per upload | **Done** | `-PversionCode` > `GITHUB_RUN_NUMBER` > 1. `versionName` = `package.json` version (tag `vX.Y.Z` must equal it; CI checks). |
| Debuggable off, WebView debugging off in release | **Done** | Capacitor defaults `webContentsDebuggingEnabled` to "build is debuggable", so release is off and debug builds can still use `chrome://inspect`. |
| No cleartext traffic | **Done** | `network_security_config.xml` + `usesCleartextTraffic=false`. |
| Android vitals "bad behaviour" thresholds: user-perceived crash rate 1.09 %, user-perceived ANR rate 0.47 % (per-device 8 %), excessive wake-ups / stuck wake locks | **Follow-up** | Nothing we do is near these (single WebView activity, no services/wake locks; `FLAG_KEEP_SCREEN_ON` is a window flag, not a wake lock). Watch Play Console > Android vitals after launch; test on a low-RAM phone. |
| Large screens (Android 16 ignores orientation/resizability locks on displays >= 600 dp wide) | **Follow-up** | `sensorLandscape` is honoured on phones; on tablets, foldables and Chromebooks the system may show the game in portrait or a resized window. The web layout is responsive, but check a tablet screenshot. |
| App is installable on supported devices (uses-feature filtering) | **Done** | Touchscreen required; landscape and portrait declared `required=false` so the lock does not hide the app from devices. |

## 2. Families policy / kids (audience 3-10: COPPA, GDPR-K)

| Requirement | Status | Notes |
|---|---|---|
| Target audience & content declaration | **Owner** | Play Console > App content > Target audience: select **5 and under, 6-8 and 9-12** (the game targets 3-10). Selecting any under-13 group puts the app under the Families policy. Answer "appeals to children". |
| Content rating (IARC questionnaire) | **Owner** | Answer truthfully: no violence, no user-generated content, no chat, no purchases, no location sharing. Expect an "Everyone"-type rating. |
| Privacy policy URL (mandatory for apps aimed at children, even with no data collected) | **Owner** | Host a public policy page (e.g. on the game's own site) saying: no accounts, no ads, no analytics, no data leaves the device; progress is stored locally (and optionally in Google's device backup). Paste the URL in Play Console > App content. |
| Data safety form | **Owner** | Expected answer: **no data collected, no data shared**. The only stored data is numeric progress in WebView localStorage. We opted that data into Android Auto Backup / device transfer (`data_extraction_rules.xml`, `backup_rules.xml`); check the Data safety help text on whether backup needs a disclosure and answer accordingly. |
| No ads, no ad SDKs, no advertising ID | **Done** | Manifest has only `INTERNET`; no `AD_ID`, no analytics/ads libraries (only Capacitor core, App, Status Bar). Re-check the merged manifest after any plugin change. |
| Only Families-certified SDKs; no precise location, contacts, camera, microphone | **Done** | No such permissions or SDKs. |
| No external links / purchases a child could tap | **Done** (verify) | `web/` contains no external URLs. Capacitor would hand off-origin links to the system browser, so keep it that way (or gate it behind a grown-up check). |
| Tap-to-start audio, no scary imagery, no dark patterns | **Done** | Game design rules in the web repo's `CLAUDE.md`. |
| Optional: join "Designed for Families" / Teacher Approved | **Owner** | Optional programs; require extra review. |
| New personal developer accounts may need a closed test (testers for N days) before production | **Owner** | Check the current rule for your account type in Play Console > Testing > Closed testing. |

## 3. Store listing

| Asset | Spec | Status |
|---|---|---|
| App name | up to 30 characters. Currently **"Guardians of Gala"** | **Owner**: see naming note below. |
| Short description | up to 80 characters | **Owner** |
| Full description | up to 4000 characters, kid/parent friendly, no unverifiable claims | **Owner** |
| App icon | 512 x 512 PNG, 32-bit, <= 1 MB (export from `resources/icon.png`, 1024 px) | **Owner** (source art exists; the in-app launcher icon is already generated) |
| Feature graphic | 1024 x 500 PNG/JPEG | **Owner** (not created) |
| Phone screenshots | 2-8, JPEG/PNG, 16:9 sides 320-3840 px. **Take them in LANDSCAPE** (the game is landscape-only) | **Owner** |
| 7" / 10" tablet screenshots | recommended | **Owner** (optional) |
| Category / tags / contact email | Education or Games > Educational; support email required | **Owner** |

## 4. Owner actions (cannot be done from the repo)

1. **Upload keystore + secrets.** Generate once, e.g.
   `keytool -genkeypair -v -keystore upload.jks -alias gog-upload -keyalg RSA -keysize 2048 -validity 10000`,
   back it up (two places), then in GitHub > Settings > Secrets > Actions add `KEYSTORE_B64`
   (`base64 -w0 upload.jks`), `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`. Never commit the file.
   Opt in to Play App Signing on first upload.
2. **Privacy policy URL** (section 2) and the Data safety / Target audience / Content rating forms.
3. **Store assets** (section 3), including landscape phone screenshots.
4. **Confirm the app name "Guardians of Gala" vs the project name "Guardians of Gaia".** The app label, `appName`
   and `strings.xml` say "Gala" (the owner said Gala is the world's name); the repos, docs and CLAUDE.md say "Gaia".
   Pick one for the store listing, launcher label and in-game titles before the first upload; it is cheap to change
   now (`capacitor.config.json`, `strings.xml`) and annoying after launch.
5. **Application id `com.gog.app` is permanent** once the first build is uploaded to Play. Confirm it is the final id.
6. **Stray outer git repo.** `D:\Vishal\work\GOG\repo\app\.git` sits one level above this project
   (`...\app\guardians-of-gaia`, whose own `.git` is the real GOG_app repo). It was left untouched. Git commands run
   from the parent folder (or an IDE opened there) hit the wrong repo. Decide whether to delete it; do not delete it
   by accident.
7. **Run the device checks below.**

## 5. Follow-ups that need a device / SDK

| Item | Why it is not done | How to finish |
|---|---|---|
| Remove the `INTERNET` permission | Capacitor serves `https://localhost` from inside the app via `shouldInterceptRequest`, which should not need it, but that could not be proven without a device. Removing it makes the Data safety/Families story simplest. | Remove the `<uses-permission>` line, install a debug build on a phone in airplane mode and on Wi-Fi; if the game loads, audio plays and the Back button works, keep it removed. |
| R8 / resource shrinking | No Android SDK on the build machine. Off by default; switch exists. | `cd android && ./gradlew assembleRelease -Pminify=true -PallowUnsignedRelease`, install, play every stage (touch, narration, Back, rotate), then set the default in `app/build.gradle`. Also shrinks the ~2 MB of now-unreferenced `drawable*/splash.png` files. |
| Prove the backup restore of progress | Needs two devices or `adb`. | `adb shell bmgr backupnow com.gog.app`, uninstall, reinstall, `adb shell bmgr restore`; stars should return. Edit the rules if localStorage lives elsewhere on a given WebView version. |
| Predictive back (`enableOnBackInvokedCallback=true`) | Capacitor's App plugin uses `OnBackPressedDispatcher`, which AndroidX routes through the new callback, and targetSdk 36 enables predictive back anyway. Not run on a device. | On Android 13-16: in a stage press Back -> world map; on the map press twice -> exit. |
| Remove the unused `@capacitor/status-bar` plugin | Not used by the game (`web/` has no `StatusBar` calls); removal touches `package.json`/lock and the generated gradle. | `npm uninstall @capacitor/status-bar`, `npm run sync`, drop the `StatusBar` block in `capacitor.config.json`. |

## 6. How to verify landscape / immersive behaviour on a device

```sh
npm run sync && cd android && ./gradlew assembleDebug          # needs JDK 21 + Android SDK 36
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.gog.app/.MainActivity
adb shell settings put system accelerometer_rotation 1         # auto-rotate on
```
* Hold the phone upright: the game must stay landscape. Rotate 180 degrees in landscape: it should flip (sensorLandscape).
* Status bar and navigation bar hidden; swipe from the top/bottom edge shows them briefly, then they hide again.
* Notch: Settings > Developer options > Drawing > Display cutout > pick a "tall/corner/double" cutout. Game art and
  HUD should fill the screen and the HUD must stay clear of the cut-out (web `env(safe-area-inset-*)`).
  In a debug build open `chrome://inspect` and run
  `getComputedStyle(document.documentElement).getPropertyValue('--safe-area-inset-left')` to see the inset Capacitor injects.
* Press Home: music/narration must stop; return: the game resumes. Leave the game idle: the screen must not sleep.
* Splash: cold start shows cream background + owl, then the game, no white flash (also with system dark mode on).
* Themed icon (Android 13+): Settings > Wallpaper & style > Themed icons.
* `adb shell dumpsys window | grep -i mCurrentRotation` and `adb shell dumpsys activity activities | grep -i screenOrientation` to confirm the lock.

## 7. What changed in the wrapper for this checklist

Manifest: landscape lock, uses-feature, network security config, backup rules, predictive back flag, narrower FileProvider.
`MainActivity`: Android 12 splash, immersive mode, keep-screen-on, WebView pause/resume, overscroll/long-press off.
Resources: cream splash + owl, themed (monochrome) icon layer, cutout mode, cream window background.
Gradle: release fails without keystore, derived version, bundle splits, parallel/caching, optional `-Pminify`.
Not compiled or run here (no SDK): Java sources, resource linking, the AAB.
