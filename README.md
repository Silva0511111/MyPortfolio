# Shilivanus Amadhila MiningChecklistApp Portfolio

This repository contains Shilivanus Amadhila's Computer Programming I portfolio for MiningChecklistApp, a mobile app for supporting mining and engineering workflows.

The portfolio now uses a dark navy engineering visual system with electric blue and cyan accents, system cards, feature status badges, a responsive evidence gallery, dynamic certificate loading, and an animated splash screen.

## Portfolio Coverage

- About Shilivanus and the MiningChecklistApp semester project.
- Project overview for the mining safety checklist app.
- Feature matrix for task tracking, shift handover documentation, hazard reporting, and Firebase authentication.
- Individual SRS/documentation contribution.
- Dedicated SRS explanation and presentation contribution sections.
- Evidence gallery with active screenshots.
- Blog section for **My Contribution Video**.
- Reflection, challenges, lessons learned, certificates, and contact details.

## Local Preview

```powershell
python -m http.server 8000 --directory site
```

Open:

```text
http://localhost:8000
```

## Assets

Profile image:

```text
assets/pictures/profile.jpeg
```

Contribution video:

```text
assets/videos/contribution-video.mp4
```

If the video is missing, the site shows a polished placeholder.

Certificates:

```text
assets/certificates/**/*.pdf
```

Run the certificate sync script to clean PDF filenames, copy them into the static site, and regenerate `site/certificates.json`:

```powershell
python sync_assets.py
```

## Build Output

GitHub Pages deploys the finished static portfolio from `site/`. The workflow validates `main.py`, syncs assets, then copies `site/` to `build/web` for deployment.

To prepare the same artifact locally:

```powershell
New-Item -ItemType Directory -Force -Path build/web | Out-Null
Copy-Item -Path site/* -Destination build/web -Recurse -Force
```

## Optional Flet Web Build

Use the final GitHub repository name as the base URL:

```powershell
flet build web --yes --verbose --no-rich-output --skip-flutter-doctor --base-url <REPO_NAME> --route-url-strategy hash
```

## GitHub Pages Deployment

1. Push to `main`.
2. Open the GitHub repository settings.
3. Go to **Pages**.
4. Set **Source** to **GitHub Actions**.
5. Run the workflow or push a commit.
6. Open the deployed Pages URL from the workflow summary.
