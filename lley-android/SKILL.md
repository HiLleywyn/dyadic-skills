---
name: lley-android
description: Build, sign and verify the Lley.cat Capacitor Android application spanning lley.cat, git.lley.cat and notes.lley.cat, including native haptics, notifications, document storage and app-link permissions.
---

# Lley.cat Android

Work in the `mobile/` directory of the lley-cat repository. The app encompasses all three domains in one shell. Keep the native origin allowlist exactly aligned with the platform's three HTTPS origins; third-party navigation leaves the app. App ID is `cat.lley.app`, Capacitor 8.5.2, minimum SDK 24, target/compile SDK 36 and JDK 21.

Dyadic is a read-only reference. Do not edit its repositories, services, signing keys, caches or Android resources. Use lley-named build images, caches and emulator resources. Source changes are confined to repositories the user actually authorized.

## Build and releases

1. Read `docs/ANDROID-DELIVERY.md`, `mobile/package.json` and the native configuration in lley-cat. Versioning begins at **0.1.0**, Android build **1**, by the owner's explicit reset. Keep root/mobile package versions and their lockfile roots aligned. Preserve signing identity and increase the numeric `versionCode` for subsequent updates.
2. Run `npm ci --prefix mobile` and `npm run sync --prefix mobile` after Capacitor configuration or dependency changes. The bundled `www/` assets provide offline recovery; the real application comes from the three production sites.
3. Build the SDK image from `mobile/Dockerfile` as `lley-android:36`, then run `node ops/build-android.mjs`. It uses the dedicated `lley-android-gradle` cache and exports signed APK, AAB and checksums under ignored `ops/test-results/android-VERSION/`.
4. `LLEY_SIGNING_DIR` defaults to private `ops/secrets/android`, containing `release.jks` alias `lley` and `keystore.properties`. Never print, commit, replace or expose the key/passwords to a pipeline job. Preserve this key for installable updates. Only public certificate fingerprints belong in `public/assetlinks.json`.
5. Verify `apksigner`, package ID/version/permissions, installation and actual native behavior. Build `assembleReleaseAndroidTest`; on a booted task-owned emulator with `mobile/` mounted at `/workspace`, run `node ops/test-android.mjs`. It tests the signed release APK and records its hash. Run `npm run test:login` against the newly built app image for isolated signed assertion/security checks. `ops/publish-android.mjs` requires matching APK evidence and passing login checks. Distinguish emulator assertions from physical vibration/touch testing. Upload the verified files to a draft Release, verify SHA-256, then publish within the authorized task. See [lley-delivery](../lley-delivery/SKILL.md). Do not enable Actions to build or publish an APK while delivery is required to remain paused.

## Native capabilities

The TypeScript client is `src/native.ts`; Java implementation is `mobile/android/app/src/main/java/cat/lley/app/`. `LleyNative` is an AndroidX origin-bound web-message listener. It accepts top-frame messages only. Do not replace it with an unrestricted JavaScript interface or enable remote debugging in a production release.

- Haptics: Android feedback constants and hardware effects; respect Android touch-feedback and the in-app setting; throttle drag/tap bursts. Never substitute browser vibration and call it native integration.
- Notifications: explicit Android 13+ permission, dedicated native channel, optional WorkManager activity polling. Polling runs approximately every 15 minutes and can be delayed by battery policy. It requires an owner session and stops receiving private API content after sign-out. There is no configured Firebase/FCM push service; do not claim immediate background push delivery.
- Storage: use Storage Access Framework open/create/folder intents. Selected-folder grants are persistable; broad storage and `MANAGE_EXTERNAL_STORAGE` are unnecessary. File reads are capped at 8 MB, native trusted-origin downloads at 256 MB. Cookie-bearing downloads must stay on the three HTTPS origins and refuse redirects.
- Passkeys/app links: serve `/.well-known/assetlinks.json` on all three origins with the same package and release certificate fingerprint. Keep that public metadata aligned with `shared/android-identity.json`. AndroidX WebView authentication support must remain enabled when available. The server separately accepts the pinned `android:apk-key-hash:<base64url SHA-256 certificate>` WebAuthn client-data origin; never add it to HTTP/CSRF allowed origins. Keep signature, challenge, RP ID and user-verification checks intact.
- Device UI: `/settings/app` exposes haptics, notifications and document permissions; `/app` redirects there. All Git and Notes routes must work inside the app. Respect safe-area insets, native back navigation, touch targets, image pinch and reduced motion.

## Sign-in and connection handling

`LleyWebViewClient` lets Chromium fetch the three remote HTTPS origins directly. `LleyNative` is independent of Capacitor's HTML injection proxy. Retain Capacitor's local asset handling for the bundled recovery page and normal page callbacks for system insets. Do not route an HTTP 401/403/5xx response or cancelled navigation to the offline page. A real main-frame connection error may show recovery, whose Retry link must return to the failed URL. Never bypass TLS validation.

Sign-in coverage must include all three domains, cancellation staying inline, shared owner cookies, signed native/browser assertions, replay rejection and denial of unknown APK certificates. The emulator tests simulate passkey cancellation; they do not prove the owner's biometric gesture succeeded. Keep that distinction in release notes.

Document build evidence, release URLs, real device/emulator limitations and deployment results in a notebook associated with lley-cat, using [lley-notes](../lley-notes/SKILL.md). Do not put credentials or signing material in notebook content.


## Back Navigation And UI

Version 0.1.1 / build 2 adds native `OnBackPressedDispatcher` handling. The app dispatches a cancelable `lley-android-back` event; the shared overlay registry closes the highest-priority/latest image dialog, modal or popup. Otherwise the native shell goes to a previous trusted WebView entry, including cross-domain history. It skips bundled/non-platform entries, returns an initial deep link to Home, and stays open at the root. Keep modal/image/menu hooks registered with cleanup; never let Back finish the activity by falling through to the default callback. Test hardware Back on a task-owned clean emulator using `BackNavigationTest`, alongside the prior native/login regressions (nine tests total).

Use normal English title case with lowercase internal minor words. The Android controls are Send Test, Add Folder and Add File. Access Tokens is inside Settings → Security on the same page; legacy token URLs still resolve there. Web UI changes deploy through the application; native Back changes require a newly signed APK/AAB. Increment versionCode for installable updates and retain the release certificate.
