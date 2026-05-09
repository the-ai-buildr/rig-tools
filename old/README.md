# Rig Tools

Oilfield drilling calculators — standalone desktop app built with [stlite](https://github.com/whitphx/stlite) (Streamlit + WebAssembly + Electron).

No server, no internet required. Runs fully offline.

## Development

### Prerequisites
- Node.js 18+
- npm

### Setup

```bash
npm install
```

### Run locally

```bash
npm run dump    # build artifacts
npm run serve   # open Electron window
```

### Package for distribution

By default, electron-builder builds for the **current platform only** (Mac → .dmg; Windows → .exe). From Mac:

```bash
npm run app:dist       # current platform only (Mac when on Mac)
npm run app:dist:mac   # macOS only → dist/Rig Tools-x.x.x.dmg
npm run app:dist:win   # Windows only → dist/Rig Tools Setup x.x.x.exe + Rig Tools x.x.x.exe (portable)
npm run app:dist:all   # macOS + Windows + Linux
```

For Windows builds on Mac, electron-builder uses Wine internally (no extra install needed).

### Code signing & notarization (macOS)

macOS Gatekeeper will block or delete unsigned apps. To build an app that opens without “malware” warnings:

1. **Apple Developer Program**  
   Enroll at [developer.apple.com](https://developer.apple.com) ($99/year).

2. **Developer ID certificate**  
   In [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/list), create a **Developer ID Application** certificate. Download it and double‑click to add it to **Keychain Access**.

3. **Build**  
   From a Mac with that identity in your keychain, run:
   ```bash
   npm run app:dist
   ```
   electron-builder will use your Developer ID to sign the app.

4. **Notarization (recommended)**  
   So Gatekeeper accepts the app (no “cannot be opened” / quarantine):
   - Create an [app-specific password](https://support.apple.com/HT204397) for your Apple ID.
   - Find your [Team ID](https://developer.apple.com/help/account/manage-your-team/locate-your-team-id/).
   - Set env vars and build:
   ```bash
   export APPLE_ID="your@email.com"
   export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   export APPLE_TEAM_ID="XXXXXXXXXX"
   npm run app:dist
   ```
   The `afterSign` script will submit the app to Apple for notarization and staple the ticket.

Without notarization, users can right‑click the app → **Open** once to bypass the warning, but signing + notarization is the proper fix.

### Code signing (Windows)

To reduce SmartScreen “Windows protected your PC” warnings, sign the .exe with a code signing certificate:

1. **Certificate**  
   Buy a **Code Signing** or **EV Code Signing** certificate from a CA (DigiCert, Sectigo, etc.). EV certs give immediate trust but require a hardware dongle and can’t be used in CI. Standard certs work with electron-builder; trust builds over time as users install.

2. **Export as .pfx**  
   Export your cert from Windows (or the CA’s tools) as a `.pfx` or `.p12` file with a password.

3. **Build with signing**  
   Set env vars and build (from Mac or Windows):

   ```bash
   export WIN_CSC_LINK="/path/to/your-cert.pfx"
   export WIN_CSC_KEY_PASSWORD="your-cert-password"
   npm run app:dist:win
   ```

   Or use `CSC_LINK` and `CSC_KEY_PASSWORD` if you prefer the generic vars.

## Project Structure

```
app.py              # Home screen
pages/              # Calculator pages (one file = one page)
calcs/              # Pure Python calculation modules
data/               # Reference data (pipe specs, etc.)
assets/             # App icons
```

## Adding a New Calculator

1. Copy `pages/01_template.py` → `pages/NN_my_calc.py`
2. Update the title, inputs, and calculation logic
3. Add any new Python deps to `requirements.txt` and `package.json → stlite.desktop.dependencies`
4. Run `npm run dump && npm run serve` to test
