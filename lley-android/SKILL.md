---
name: lley-android
description: Build, sign and verify the Lley.cat Capacitor Android application spanning lley.cat, git.lley.cat and notes.lley.cat, including native haptics, notifications, document storage and app-link permissions.
---

# Lley.cat Android

Work in the `mobile/` directory of the lley-cat repository. The app encompasses all three domains in one shell. Keep the native origin allowlist exactly aligned with the platform's three HTTPS origins; third-party navigation leaves the app. App ID is `cat.lley.app`, Capacitor 8.5.2, minimum SDK 24, target/compile SDK 36 and JDK 21.

Dyadic is a read-only reference. Do not edit its repositories, services, signing keys, caches or Android resources. Use lley-named build images, caches and emulator resources. Source changes are confined to repositories the user actually authorized.

## Build and releases

1. Read `docs/ANDROID-DELIVERY.md`, `mobile/package.json` and the native configuration in lley-cat. Preserve signing identity and increment `version` / numeric `versionCode` for updates.
2. Run `npm ci --prefix mobile` and `npm run sync --prefix mobile` after Capacitor configuration or dependency changes. The bundled `www/` assets provide offline recovery; the real application comes from the three production sites.
3. Build the SDK image from `mobile/Dockerfile` as `lley-android:36`, then run `node ops/build-android.mjs`. It uses the dedicated `lley-android-gradle` cache and exports signed APK, AAB and checksums under ignored `ops/test-results/android-VERSION/`.
4. `LLEY_SIGNING_DIR` defaults to private `ops/secrets/android`, containing `release.jks` alias `lley` and `keystore.properties`. Never print, commit, replace or expose the key/passwords to a pipeline job. Preserve this key for installable updates. Only public certificate fingerprints belong in `public/assetlinks.json`.
5. Verify `apksigner`, package ID/version/permissions, installation and actual native behavior. Distinguish emulator assertions from physical vibration/touch testing. Upload the verified files to a draft Release, verify SHA-256, then publish within the authorized task. See [lley-delivery](../lley-delivery/SKILL.md). Do not enable Actions to build or publish an APK while delivery is required to remain paused.

## Native capabilities

The TypeScript client is `src/native.ts`; Java implementation is `mobile/android/app/src/main/java/cat/lley/app/`. `LleyNative` is an AndroidX origin-bound web-message listener. It accepts top-frame messages only. Do not replace it with an unrestricted JavaScript interface or enable remote debugging in a production release.

- Haptics: Android feedback constants and hardware effects; respect Android touch-feedback and the in-app setting; throttle drag/tap bursts. Never substitute browser vibration and call it native integration.
- Notifications: explicit Android 13+ permission, dedicated native channel, optional WorkManager activity polling. Polling runs approximately every 15 minutes and can be delayed by battery policy. It requires an owner session and stops receiving private API content after sign-out. There is no configured Firebase/FCM push service; do not claim immediate background push delivery.
- Storage: use Storage Access Framework open/create/folder intents. Selected-folder grants are persistable; broad storage and `MANAGE_EXTERNAL_STORAGE` are unnecessary. File reads are capped at 8 MB, native trusted-origin downloads at 256 MB. Cookie-bearing downloads must stay on the three HTTPS origins and refuse redirects.
- Passkeys/app links: serve `/.well-known/assetlinks.json` on all three origins with the same package and release certificate fingerprint. AndroidX WebView authentication support must remain enabled when available.
- Device UI: `/app` exposes haptics, notifications and document permissions. All Git and Notes routes must work inside the app. Respect safe-area insets, native back navigation, touch targets, image pinch and reduced motion.

Document build evidence, release URLs, real device/emulator limitations and deployment results in a notebook associated with lley-cat, using [lley-notes](../lley-notes/SKILL.md). Do not put credentials or signing material in notebook content.
