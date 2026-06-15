from pathlib import Path
# pyrefly: ignore [missing-import]
import flet as ft

# Theme Color Palette (Navy/Electric Blue/Cyan/White)
BG = "#0B0F19"
PANEL = "#111827"
PANEL_2 = "#1F2937"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"
LINE = "#1E293B"
BLUE = "#3B82F6"      # Primary Electric Blue
CYAN = "#00D2FF"      # Accent Cyan
WHITE = "#FFFFFF"
DARK = "#030712"

ASSET_DIR = Path(__file__).resolve().parent / "assets"

# Student Metadata
STUDENT_NAME = "Shilivanus Amadhila"
STUDENT_NUMBER = "225119919"
STUDENT_EMAIL = "amadhilashilivanus@gmail.com"
GITHUB_USERNAME = "Silva051111"
GITHUB_PROFILE = f"https://github.com/{GITHUB_USERNAME}"
PROJECT_NAME = "MiningChecklistApp"
ROLE = "Documentation Lead"
TAGLINE = "Future engineer."

PROJECT_DESCRIPTION = (
    "A semester project focused on supporting mining/engineering workflows through digital checklists, "
    "task tracking, and safety-related reporting."
)

FEATURES = [
    ("Task tracking and dashboard", "Provides digital checklists and visual status dashboards for industrial tasks.", "Core"),
    ("Shift handover documentation", "Facilitates seamless logging and shift handover reports for team rotations.", "Core"),
    ("Hazard or emergency reporting", "Supports quick logging of safety hazards or emergencies directly from the field.", "Safety"),
    ("Firebase-based storage/authentication", "Powers secure user logins and stores active safety checklists safely.", "Infrastructure"),
]

TECHNOLOGIES = [
    "Python",
    "Flet",
    "Firebase Auth",
    "Firestore Database",
    "Firebase Storage",
    "GitHub",
    "Markdown",
]

CONTRIBUTIONS = [
    ("Helped organize and document", "Structured and consolidated the MiningChecklistApp project requirements and specs."),
    ("Supported clearer explanation", "Maintained clear written explanations for project presentations and team alignment."),
    ("Maintained evidence", "Curated documentation-focused contributions, checklists, and screenshots for records."),
    ("GitHub Activity & Commits", "Contributed commits to the pombilihamwoomo-dot/MiningChecklistApp repository."),
]

def pad(x=24, y=24):
    return ft.Padding(x, y, x, y)

def border(color=LINE):
    return ft.Border(ft.BorderSide(1, color))

def open_link(page: ft.Page, url: str):
    page.launch_url(url)

# Reusable Scanners
def find_profile_image() -> str:
    pictures_dir = ASSET_DIR / "pictures"
    if not pictures_dir.exists():
        return None
    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
    # Check directly inside pictures_dir first
    for p in sorted(pictures_dir.glob("*"), key=lambda x: x.name.lower()):
        if p.is_file() and p.suffix.lower() in allowed_exts:
            return p.relative_to(ASSET_DIR).as_posix()
    # Fallback to search recursively (excluding github screenshots folder)
    for p in sorted(pictures_dir.rglob("*"), key=lambda x: x.name.lower()):
        if "github" in p.parts:
            continue
        if p.is_file() and p.suffix.lower() in allowed_exts:
            return p.relative_to(ASSET_DIR).as_posix()
    return None

def find_certificates():
    cert_dir = ASSET_DIR / "certificates"
    if not cert_dir.exists():
        return []
    allowed_exts = {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
    certs = []
    # Recursively find certificate files
    for p in sorted(cert_dir.rglob("*"), key=lambda x: x.name.lower()):
        if p.is_file() and p.suffix.lower() in allowed_exts:
            clean_title = p.stem.replace("_", " ").replace("-", " ").title()
            clean_title = clean_title.replace("Matlab", "MATLAB").replace("Pdf", "PDF")
            certs.append({
                "title": clean_title,
                "file": p.relative_to(ASSET_DIR).as_posix(),
                "is_pdf": p.suffix.lower() == ".pdf"
            })
    return certs

def find_github_screenshots():
    paths_to_check = [ASSET_DIR / "pictures" / "github", ASSET_DIR / "github"]
    allowed_exts = {".png", ".jpg", ".jpeg", ".webp"}
    screenshots = []
    for path in paths_to_check:
        if path.exists():
            for p in sorted(path.rglob("*"), key=lambda x: x.name.lower()):
                if p.is_file() and p.suffix.lower() in allowed_exts:
                    screenshots.append(p.relative_to(ASSET_DIR).as_posix())
    return screenshots

def find_video() -> str:
    video_dirs = [ASSET_DIR / "video", ASSET_DIR / "videos"]
    allowed_exts = {".mp4", ".mov", ".webm"}
    for video_dir in video_dirs:
        if video_dir.exists():
            for p in sorted(video_dir.glob("*"), key=lambda x: x.name.lower()):
                if p.is_file() and p.suffix.lower() in allowed_exts:
                    return p.relative_to(ASSET_DIR).as_posix()
    return None

# Reusable Components
def text(value, size=14, color=MUTED, weight=None, **kwargs):
    return ft.Text(value, size=size, color=color, weight=weight, **kwargs)

def eyebrow(value):
    return text(value.upper(), size=12, color=CYAN, weight=ft.FontWeight.W_900)

def pill(value, accent=BLUE):
    return ft.Container(
        content=text(value, size=12, color=TEXT, weight=ft.FontWeight.W_700),
        bgcolor="#1E293B" if accent == BLUE else "#0F172A",
        border=border("#3B82F6" if accent == BLUE else "#1E293B"),
        border_radius=999,
        padding=ft.Padding(12, 7, 12, 7),
    )

def card(title, body, accent=BLUE, icon=None):
    controls = []
    if icon:
        controls.append(
            ft.Container(
                width=46,
                height=46,
                border_radius=8,
                alignment=ft.Alignment.CENTER,
                bgcolor="#1E293B" if accent == BLUE else "#0F172A",
                content=text(icon, size=13, color=accent, weight=ft.FontWeight.W_900),
            )
        )
    else:
        controls.append(ft.Container(width=46, height=4, bgcolor=accent, border_radius=99))
    controls.append(text(title, size=19, color=TEXT, weight=ft.FontWeight.W_900))
    for item in body:
        controls.append(item if isinstance(item, ft.Control) else text(item, size=14))
    return ft.Container(
        bgcolor=PANEL,
        border=border(),
        border_radius=12,
        padding=pad(22, 22),
        content=ft.Column(controls, spacing=12, tight=True),
    )

def section(title, label, controls, tinted=False):
    return ft.Container(
        bgcolor=PANEL_2 if tinted else None,
        border=ft.Border(top=ft.BorderSide(1, LINE), bottom=ft.BorderSide(1, LINE)) if tinted else None,
        padding=pad(28, 52),
        content=ft.Column(
            [
                eyebrow(label),
                text(title, size=32, color=TEXT, weight=ft.FontWeight.W_900),
                *controls,
            ],
            spacing=16,
        ),
    )

def profile_visual():
    prof_img = find_profile_image()
    if prof_img:
        return ft.Container(
            width=180,
            height=180,
            border_radius=90,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=border(BLUE),
            content=ft.Image(src=prof_img, fit=ft.BoxFit.COVER),
        )

    return ft.Container(
        width=180,
        height=180,
        border_radius=90,
        bgcolor=PANEL_2,
        border=border(BLUE),
        alignment=ft.Alignment.CENTER,
        content=text("No profile image found", size=13, text_align=ft.TextAlign.CENTER),
    )

def shield_panel():
    return ft.Container(
        bgcolor=PANEL,
        border=border(BLUE),
        border_radius=12,
        padding=pad(24, 24),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column([eyebrow("System Overview"), text("Mining workflow tracking", size=22, color=TEXT, weight=ft.FontWeight.W_900)], spacing=2, expand=True),
                        pill("Mobile App", CYAN),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    width=220,
                    height=220,
                    border_radius=110,
                    bgcolor="#0F172A",
                    border=border(BLUE),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Container(
                        width=120,
                        height=138,
                        alignment=ft.Alignment.CENTER,
                        border=border(CYAN),
                        border_radius=26,
                        bgcolor="#1E293B",
                        content=text("MC", size=30, color=CYAN, weight=ft.FontWeight.W_900),
                    ),
                ),
                ft.Row([pill(item) for item in ["Checklist", "Report", "Handover", "Sync"]], wrap=True, spacing=8, run_spacing=8),
                ft.Row([pill(item) for item in TECHNOLOGIES], wrap=True, spacing=8, run_spacing=8),
            ],
            spacing=18,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

def video_block(page: ft.Page):
    video_path = find_video()
    video_available = video_path is not None
    return ft.Container(
        bgcolor=DARK,
        border=border(BLUE),
        border_radius=12,
        padding=pad(26, 26),
        content=ft.Column(
            [
                text("Contribution Video" if video_available else "Contribution Video Pending", size=22, color=TEXT, weight=ft.FontWeight.W_900),
                text(
                    "A short video presenting Shilivanus Amadhila’s project contribution and portfolio evidence.",
                    size=14,
                    color=MUTED
                ),
                ft.OutlinedButton(
                    "Watch Video" if video_available else "Video Pending",
                    icon=ft.Icons.PLAY_CIRCLE,
                    disabled=not video_available,
                    on_click=lambda e, p=video_path: open_link(page, p),
                ),
            ],
            spacing=14,
        ),
    )

def main(page: ft.Page):
    page.title = f"{STUDENT_NAME} | {PROJECT_NAME} Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window_min_width = 360

    # Sticky Header
    header = ft.Container(
        bgcolor=DARK,
        border=ft.Border(bottom=ft.BorderSide(1, LINE)),
        padding=pad(28, 14),
        content=ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 12, "md": 5},
                    content=ft.Row(
                        [
                            ft.Container(
                                width=44,
                                height=44,
                                border_radius=8,
                                bgcolor="#1E293B",
                                border=border(BLUE),
                                alignment=ft.Alignment.CENTER,
                                content=text("MC", size=13, color=CYAN, weight=ft.FontWeight.W_900),
                            ),
                            ft.Column(
                                [
                                    text(STUDENT_NAME, size=20, color=TEXT, weight=ft.FontWeight.W_900),
                                    text(f"{PROJECT_NAME} Portfolio | Computer Programming I", size=12),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "md": 7},
                    content=ft.Row(
                        [
                            ft.TextButton("Project", on_click=lambda e: open_link(page, "#project")),
                            ft.TextButton("Role", on_click=lambda e: open_link(page, "#role")),
                            ft.TextButton("Evidence", on_click=lambda e: open_link(page, "#evidence")),
                            ft.TextButton("Video", on_click=lambda e: open_link(page, "#video")),
                            ft.TextButton("Certificates", on_click=lambda e: open_link(page, "#certificates")),
                            ft.TextButton("Contact", on_click=lambda e: open_link(page, "#contact")),
                        ],
                        wrap=True,
                        alignment=ft.MainAxisAlignment.END,
                        spacing=2,
                        run_spacing=4,
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        ),
    )

    # Hero / Header Section
    hero = ft.Container(
        padding=pad(28, 64),
        content=ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 12, "md": 7},
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    pill(PROJECT_NAME),
                                    pill(ROLE, CYAN),
                                    pill(f"SN: {STUDENT_NUMBER}", BLUE),
                                ],
                                wrap=True,
                                spacing=9,
                                run_spacing=9,
                            ),
                            ft.Column(
                                [
                                    text(STUDENT_NAME, size=50, color=TEXT, weight=ft.FontWeight.W_900),
                                    text(TAGLINE, size=22, color=CYAN, weight=ft.FontWeight.W_800),
                                ],
                                spacing=2,
                            ),
                            text(PROJECT_DESCRIPTION, size=17),
                            ft.Row(
                                [
                                    ft.ElevatedButton("View GitHub Evidence", icon=ft.Icons.IMAGE_SEARCH, on_click=lambda e: open_link(page, "#evidence")),
                                    ft.OutlinedButton("Email Me", icon=ft.Icons.EMAIL, on_click=lambda e: open_link(page, f"mailto:{STUDENT_EMAIL}")),
                                    ft.OutlinedButton("GitHub Profile", icon=ft.Icons.OPEN_IN_NEW, on_click=lambda e: open_link(page, GITHUB_PROFILE)),
                                    ft.OutlinedButton("Watch Video", icon=ft.Icons.PLAY_ARROW, on_click=lambda e: open_link(page, "#video")),
                                ],
                                wrap=True,
                                spacing=12,
                                run_spacing=12,
                            ),
                            ft.ResponsiveRow(
                                [
                                    ft.Container(card("Student", [STUDENT_NAME], BLUE), col={"xs": 12, "sm": 4}),
                                    ft.Container(card("Project", [PROJECT_NAME], CYAN), col={"xs": 12, "sm": 4}),
                                    ft.Container(card("Focus", [ROLE], BLUE), col={"xs": 12, "sm": 4}),
                                ],
                                spacing=12,
                                run_spacing=12,
                            ),
                        ],
                        spacing=18,
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "md": 5},
                    content=ft.Column(
                        [
                            profile_visual(),
                            shield_panel()
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ),
            ],
            spacing=28,
            run_spacing=28,
        ),
    )

    # About Section
    about = section(
        "Shilivanus Amadhila is the Documentation Lead.",
        "About",
        [
            text(
                "Shilivanus Amadhila is a Computer Programming I student and the Documentation Lead for the "
                "MiningChecklistApp semester project. His portfolio highlights his project documentation work, "
                "GitHub activity, certificates, and contribution evidence.",
                size=15,
            )
        ],
    )

    # Project Section
    project = section(
        "MiningChecklistApp - Mining & Engineering Safety Workflow Tool",
        "Project Overview",
        [
            text(
                "A semester project focused on supporting mining/engineering workflows through digital checklists, "
                "task tracking, and safety-related reporting.",
                size=15,
            ),
            ft.ResponsiveRow(
                [
                    ft.Container(card("Checklist Workflow", ["Digitally verify site operations and equipment integrity."], CYAN, "C"), col={"xs": 12, "md": 3}),
                    ft.Container(card("Safety Tracking", ["Track active checklists and pending inspections in real-time."], BLUE, "T"), col={"xs": 12, "md": 3}),
                    ft.Container(card("Hazard Reporting", ["Record site emergencies and hazardous incidents dynamically."], CYAN, "H"), col={"xs": 12, "md": 3}),
                    ft.Container(card("Firebase Sync", ["Sync safety logs and user profiles to Firebase Firestore securely."], BLUE, "S"), col={"xs": 12, "md": 3}),
                ],
                spacing=14,
                run_spacing=14,
            )
        ],
        tinted=True,
    )

    # Feature Matrix Section
    features = section(
        "Core App Capabilities",
        "Feature Matrix",
        [
            ft.ResponsiveRow(
                [
                    ft.Container(card(title, [body, pill(status, CYAN)], BLUE, f"{index:02}"), col={"xs": 12, "md": 6})
                    for index, (title, body, status) in enumerate(FEATURES, start=1)
                ],
                spacing=14,
                run_spacing=14,
            )
        ],
    )

    # Project Role Section
    role_section = section(
        "Documentation Lead Contribution",
        "Project Role",
        [
            text(
                "My key responsibilities and deliverables for the MiningChecklistApp project, focusing on "
                "SRS management, documentation evidence, and presentation layout support.",
                size=15,
            ),
            ft.ResponsiveRow(
                [
                    ft.Container(card(title, [body], BLUE if index % 2 else CYAN, f"{index:02}"), col={"xs": 12, "sm": 6, "lg": 3})
                    for index, (title, body) in enumerate(CONTRIBUTIONS, start=1)
                ],
                spacing=14,
                run_spacing=14,
            ),
        ],
        tinted=True,
    )

    # GitHub Evidence Section
    screenshots = find_github_screenshots()
    captions = [
        "GitHub profile overview showing username Silva051111.",
        "Repository contribution activity showing commits in pombilihamwoomo-dot/MiningChecklistApp.",
        "Commit/activity evidence details of code contributions."
    ]
    screenshot_cards = []
    for i, src in enumerate(screenshots):
        cap = captions[i] if i < len(captions) else "GitHub evidence screenshot."
        screenshot_cards.append(
            ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            height=200,
                            border_radius=8,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            border=border(BLUE),
                            content=ft.Image(src=src, fit=ft.BoxFit.COVER)
                        ),
                        text(cap, size=13, color=MUTED)
                    ],
                    spacing=8,
                ),
                col={"xs": 12, "md": 4}
            )
        )
    if not screenshot_cards:
        screenshot_cards.append(
            ft.Container(card("GitHub Evidence Pending", ["No screenshots found under assets/pictures/github/"], BLUE), col={"xs": 12})
        )

    evidence = section(
        f"Contribution Evidence (GitHub: {GITHUB_USERNAME})",
        "GitHub Evidence",
        [
            text(
                f"Screenshots documenting commit history and contributions to pombilihamwoomo-dot/{PROJECT_NAME}.",
                size=15,
            ),
            ft.ResponsiveRow(screenshot_cards, spacing=14, run_spacing=14)
        ],
    )

    # Contribution Video Section
    video = section(
        "Project Contribution & Walkthrough Video",
        "Contribution Video",
        [
            ft.ResponsiveRow(
                [
                    ft.Container(video_block(page), col={"xs": 12, "md": 7}),
                    ft.Container(
                        card(
                            "Video Summary",
                            [
                                "Presents Shilivanus Amadhila's project contributions.",
                                f"Covers SRS documentation mapping, database schema records, pombilihamwoomo-dot/{PROJECT_NAME} git commits, and validation details.",
                            ],
                            CYAN,
                        ),
                        col={"xs": 12, "md": 5},
                    ),
                ],
                spacing=18,
                run_spacing=18,
            )
        ],
        tinted=True,
    )

    # Certificates Section
    cert_items = find_certificates()
    cert_cards = []
    for item in cert_items:
        card_content = []
        if item["is_pdf"]:
            card_content.append(text("Format: PDF Document", size=13, color=MUTED))
            card_content.append(
                ft.OutlinedButton(
                    "View Certificate",
                    icon=ft.Icons.PICTURE_AS_PDF,
                    on_click=lambda e, path=item["file"]: open_link(page, path)
                )
            )
        else:
            card_content.append(
                ft.Container(
                    height=130,
                    border_radius=8,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    border=border(),
                    content=ft.Image(src=item["file"], fit=ft.BoxFit.CONTAIN)
                )
            )
        cert_cards.append(
            ft.Container(
                card(item["title"], card_content, CYAN),
                col={"xs": 12, "md": 4}
            )
        )
    if not cert_cards:
        cert_cards.append(
            ft.Container(card("Certificates Pending", ["Add PDF/Image files under assets/certificates/ and rerun sync."], CYAN), col={"xs": 12})
        )

    certificate_section = section(
        "Certificates and Supporting Files",
        "Certificates",
        [ft.ResponsiveRow(cert_cards, spacing=14, run_spacing=14)],
        tinted=True,
    )

    # Contact Section
    contact = section(
        "Submission & Academic Verification Details",
        "Contact",
        [
            ft.ResponsiveRow(
                [
                    ft.Container(card("Student Details", [f"Name: {STUDENT_NAME}", f"Student number: {STUDENT_NUMBER}", f"Email: {STUDENT_EMAIL}"], BLUE), col={"xs": 12, "md": 6}),
                    ft.Container(card("Repository Details", [f"GitHub username: {GITHUB_USERNAME}", f"Project: {PROJECT_NAME}", f"Course: UNAM Computer Programming I"], CYAN), col={"xs": 12, "md": 6}),
                ],
                spacing=14,
                run_spacing=14,
            )
        ],
    )

    # Footer
    footer = ft.Container(
        bgcolor=DARK,
        border=ft.Border(top=ft.BorderSide(1, LINE)),
        padding=pad(28, 28),
        content=text(f"{STUDENT_NAME} - {PROJECT_NAME} Portfolio | University of Namibia | 2026", size=14, color=MUTED),
    )

    # Add components to page layout (mapping IDs using anchor tags)
    page.add(
        header,
        ft.Container(content=hero, key="hero"),
        ft.Container(content=about, key="about"),
        ft.Container(content=project, key="project"),
        ft.Container(content=features, key="features"),
        ft.Container(content=role_section, key="role"),
        ft.Container(content=evidence, key="evidence"),
        ft.Container(content=video, key="video"),
        ft.Container(content=certificate_section, key="certificates"),
        ft.Container(content=contact, key="contact"),
        footer
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
