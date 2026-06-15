import json
import shutil
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
SRC_ASSET_DIR = BASE_DIR / "assets"
SITE_ASSET_DIR = BASE_DIR / "site" / "assets"

def clean_title(stem):
    # Clean up name: remove extension, replace dashes/underscores, title-case
    title = stem.replace("_", " ").replace("-", " ").title()
    title = title.replace("Matlab", "MATLAB").replace("Pdf", "PDF")
    return title

def sync_certificates():
    src_cert = SRC_ASSET_DIR / "certificates"
    dest_cert = SITE_ASSET_DIR / "certificates"
    
    # Remove dest certificates folder if it exists, to clean old files
    if dest_cert.exists():
        shutil.rmtree(dest_cert)
    dest_cert.mkdir(parents=True, exist_ok=True)
    
    allowed_exts = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
    certs_data = []
    
    if src_cert.exists():
        # Find all certificates recursively
        for p in sorted(src_cert.rglob("*"), key=lambda x: x.name.lower()):
            if p.is_file() and p.suffix.lower() in allowed_exts:
                # Get path relative to src_cert
                rel_to_cert = p.relative_to(src_cert)
                dest_file_path = dest_cert / rel_to_cert
                dest_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(p, dest_file_path)
                
                # Prepare JSON representation
                file_url_path = f"assets/certificates/{rel_to_cert.as_posix()}"
                is_pdf = p.suffix.lower() == ".pdf"
                
                certs_data.append({
                    "title": clean_title(p.stem),
                    "file": file_url_path,
                    "type": "PDF" if is_pdf else "IMAGE",
                    "source": file_url_path,
                    "needsReview": False
                })
                
    # Write site/certificates.json
    cert_json_path = BASE_DIR / "site" / "certificates.json"
    with open(cert_json_path, "w", encoding="utf-8") as f:
        json.dump(certs_data, f, indent=4)
        
    print(f"Synced {len(certs_data)} certificates to site/certificates.json")

def sync_profile_and_video():
    # Sync profile image
    src_profile = SRC_ASSET_DIR / "pictures" / "profile.jpeg"
    dest_profile = SITE_ASSET_DIR / "profile-picture.jpeg"
    
    if src_profile.exists():
        shutil.copy2(src_profile, dest_profile)
        # Also copy it under the name profile.jpeg in dest just in case
        shutil.copy2(src_profile, SITE_ASSET_DIR / "profile.jpeg")
        print("Synced profile image.")
    else:
        print("Warning: src profile image not found at assets/pictures/profile.jpeg")

    # Sync video
    # Check both assets/videos/contribution-video.mp4 and assets/video/...
    src_video = SRC_ASSET_DIR / "videos" / "contribution-video.mp4"
    if not src_video.exists():
        src_video = SRC_ASSET_DIR / "video" / "contribution-video.mp4"
    
    dest_video = SITE_ASSET_DIR / "contribution-video.mp4"
    
    if src_video.exists():
        shutil.copy2(src_video, dest_video)
        print("Synced contribution video.")
    else:
        print("Warning: contribution video not found at assets/videos/contribution-video.mp4 or assets/video/contribution-video.mp4")

def sync_github_evidence():
    src_github = SRC_ASSET_DIR / "pictures" / "github"
    if not src_github.exists():
        src_github = SRC_ASSET_DIR / "github"
        
    dest_github = SITE_ASSET_DIR / "screenshots"
    dest_github.mkdir(parents=True, exist_ok=True)
    
    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
    github_files = []
    
    if src_github.exists():
        for p in sorted(src_github.rglob("*"), key=lambda x: x.name.lower()):
            if p.is_file() and p.suffix.lower() in allowed_exts:
                # Copy file to site/assets/screenshots
                shutil.copy2(p, dest_github / p.name)
                github_files.append(p.name)
                
    # Create evidence data
    # We want exactly 3 screenshots mapping to GitHub Evidence
    evidence_data = []
    
    captions = [
        "GitHub profile overview showing username Silva051111.",
        "Repository contribution activity showing commit frequency and history.",
        "Commit and activity evidence showing contributions to the project."
    ]
    
    titles = [
        "GitHub Profile Overview",
        "Repository Contribution Activity",
        "Commit/Activity Evidence"
    ]
    
    groups = [
        "GitHub Profile",
        "GitHub Repository",
        "GitHub Commits"
    ]
    
    for i, fname in enumerate(github_files[:3]):
        category = "documentation" if i == 0 else ("app" if i == 1 else "firebase")
        # However, for GitHub evidence, category filters are usually:
        # documentation, app, presentation, design, firebase.
        # Let's categorize them appropriately so they are visible under the filters:
        # 1. GitHub Profile (documentation)
        # 2. Repository Contribution Activity (firebase / workflow)
        # 3. Commit/Activity Evidence (firebase / workflow)
        cat = "documentation" if i == 0 else "firebase"
        evidence_data.append({
            "category": cat,
            "group": groups[i],
            "title": titles[i],
            "caption": captions[i] if i < len(captions) else "GitHub evidence screenshot.",
            "image": f"assets/screenshots/{fname}"
        })
        
    # Write site/evidence.json
    evidence_json_path = BASE_DIR / "site" / "evidence.json"
    with open(evidence_json_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, indent=4)
        
    print(f"Synced {len(evidence_data)} GitHub evidence screenshots to site/evidence.json")

if __name__ == "__main__":
    sync_profile_and_video()
    sync_certificates()
    sync_github_evidence()
    print("Asset synchronization complete.")
