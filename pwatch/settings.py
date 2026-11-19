"""Paths and constants. DEV never points at a production host or database."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
ROSTER_DIR = DATA_DIR / "roster"
SCHEMA_PATH = REPO_ROOT / "schemas" / "profile.schema.json"
DRAFTS_ROR_DIR = REPO_ROOT / "drafts" / "right-of-reply"
PROFILES_DIR = DATA_DIR / "profiles" / "joburg-2026"
# Profiles on hold (CHG-PW-003 fix 1) live in this subdirectory and/or carry status "on_hold".
# They are kept for the record but are not part of any batch: dq and render skip them.
HOLD_DIRNAME = "_hold"
# South Africa Standard Time (UTC+2, no daylight saving). Used to read date-only retrieved_at values
# and to write retrieved_at from fetch provenance.
SAST_OFFSET_HOURS = 2
# Raw copies of web pages fetched as profile sources (kept out of git; the manifest is committed).
PROFILE_SOURCES_ID = "profile-sources"
HOLD_STATUS = "on_hold"

USER_AGENT = "PoliticianWatchSA/0.1 public-interest research (politicianwatch.grokforum.site)"

# Primary sources (LGE 2026)
GAZETTE_NUMBER = "55741"
GAZETTE_DATE = "2026-11-13"
GAZETTE_NOTICE = "8183"
GAZETTE_PDF_URL = (
    "https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55741/"
    "government-gazette-55741-2026-11-13.pdf"
)
GAZETTE_LANDING_URL = "https://www.gazettefinder.co.za/gazettes/government-gazette/2026/55741/"
GAZETTE_SHA256 = "cd544faf2a703a81eb4466bbfcd3618f5ade03c7b456538116b385c266058798"

IEC_EVENT_ID = "1887"
IEC_RESULTS_HOME = "https://results.elections.org.za/home/"
IEC_JHB_SEAT_CALC_URL = (
    "https://results.elections.org.za/home/LGEPublicReports/1887/"
    "Seat%20Calculation%20Detail/GP/JHB.pdf"
)
IEC_JHB_SEAT_CALC_SHA256 = "6cc25c2d0814b9dfa88e1066129df2c65b34cf0dc9ba36d497f18c4d21347aac"
IEC_NEWS_GAZETTE_URL = "https://www.elections.org.za/pw/News-And-Media/News-List/News/IECNews/5726"

COUNCIL_NAME = "City of Johannesburg"
MUNICIPALITY_ID = "JHB"
EXPECTED_SEATS = 270
EXPECTED_WARDS = 135
MAJORITY = 136

LABELS = ("Confirmed", "Reported", "Alleged", "Disputed", "Unknown")
SEAT_TYPES = ("ward", "PR")
ROR_STATUSES = ("pending", "sent", "replied", "no_response")
ADVERSE_FIELDS = ("court_matters", "scandals")
# Owner-only field value for RoR status changes (the bot never records a send or reply).
ROR_RECORDED_BY_OWNER = "owner"

# Every right-of-reply draft must carry this line at the top (CHG-PW-002).
DRAFT_MARKER = "DRAFT: NOT SENT. The owner sends personally. The bot never sends."
CV_FIELDS = ("position", "career", "candidacy", "education")
OPTIONAL_FACT_FIELDS = ("known_as", "given_names", "full_name_surname")
# Minimum independent details that must match before a non-gazette source is linked to a person.
IDENTITY_MIN_DETAILS = 2

# CHG-PW-011 (owner decision, 19 Nov 2026 16:27 SAST): rule 6 default is that a source carrying
# private personal details is not linked and the fact is Unknown. A fact may link such a source
# only with an explicit per-fact owner approval and exactly this note; no private detail is copied.
PI_SOURCE_APPROVAL_FIELD = "owner_approved_pi_source"
PI_SOURCE_NOTE = "Personal details in the source are not recorded here."
