# AttendAI – Classroom Presence Intelligence
## Official Final Attendance & Verification Session Report

> **Demo Session Presentation for Judicial Review**  
> *Session evaluated and verified on NVIDIA Jetson AGX Orin Edge AI Platform.*

---

### 1. Executive Summary & Session Metadata

| Parameter | Details |
| :--- | :--- |
| **System Name** | AttendAI – Classroom Presence Intelligence |
| **Target Platform** | NVIDIA Jetson AGX Orin Developer Kit (Local Edge AI) |
| **Session ID** | `b2c71f3dd99f` |
| **Session Title** | **AI-DS Classroom Test 01** |
| **Class / Section** | 24AD5A (AI&DS, Year 3, Section A) |
| **Classroom Venue** | Hall 010 |
| **Session Started (UTC)** | `2026-10-23T08:27:30Z` |
| **Session Started (IST)** | **23 Oct 2026, 01:57:30 PM IST** |
| **Session Ended (IST)** | **23 Oct 2026, 02:00:09 PM IST** |
| **Session Status** | **`CLOSED` & `FORMALLY FINALIZED`** |
| **Faculty Reviewer** | **INDHIRAN S** |
| **Finalization Time (IST)** | **23 Oct 2026, 02:58:30 PM IST** |

---

### 2. High-Level Attendance Metrics

| Metric Description | Value |
| :--- | :--- |
| **Total Registered Roster Size** | **58 Students** |
| **Auto-Detected & Verified Present** | **5 Students** |
| **Confirmed Absent / Unattended** | **53 Students** |
| **Verified Session Attendance Rate** | **8.6%** |
| **Total System Audit Events Recorded** | **46 Events** |
| **Edge Privacy / Cloud Transmission** | **0% (100% On-Device Jetson Edge Inference)** |

---

### 3. Faculty-Verified Present Attendance Register

The following students were observed by the edge camera system, verified through multi-frame face tracking and recognition, and formally confirmed by the faculty reviewer:

| Roll Number | Student Name | Dept | Year | Sec | Marked Time (IST) | Sim. Score | Track ID | Verification | Reviewer |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| `732924ADR044` | **INDHIRAN S** | AI&DS | 3 | A | 23 Oct 2026, 01:57:39 PM IST | `0.704` | `P1` | **VERIFIED_PRESENT** | INDHIRAN S |
| `732924ADR031` | **GOUTHAM SIDDARTH A** | AI&DS | 3 | A | 23 Oct 2026, 01:57:51 PM IST | `0.693` | `P4` | **VERIFIED_PRESENT** | INDHIRAN S |
| `732924ADR013` | **DEEPAK G** | AI&DS | 3 | A | 23 Oct 2026, 01:57:56 PM IST | `0.657` | `P5` | **VERIFIED_PRESENT** | INDHIRAN S |
| `732924ADR035` | **GUGAN E** | AI&DS | 3 | A | 23 Oct 2026, 01:58:19 PM IST | `0.687` | `P10` | **VERIFIED_PRESENT** | INDHIRAN S |
| `732924ADR050` | **JIVITESH G D** | AI&DS | 3 | A | 23 Oct 2026, 01:58:32 PM IST | `0.703` | `P35` | **VERIFIED_PRESENT** | INDHIRAN S |

---

### 4. Computer Vision & Edge Intelligence Evidence Details

Each automatic attendance decision is backed by strict multi-evidence criteria computed locally on Jetson AGX Orin:

| Roll Number | Student Name | Frames Evid. | Evid. Share | Similarity | Face Age | Association Score | Decision |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `732924ADR044` | INDHIRAN S | 3 | 100.0% | 0.7037 | 0.42s | 0.8277 | `AUTO_PRESENT` |
| `732924ADR031` | GOUTHAM SIDDARTH A | 3 | 100.0% | 0.6931 | 0.44s | 0.7684 | `AUTO_PRESENT` |
| `732924ADR013` | DEEPAK G | 3 | 100.0% | 0.6567 | 0.86s | 0.4950 | `AUTO_PRESENT` |
| `732924ADR035` | GUGAN E | 3 | 100.0% | 0.6867 | 0.42s | 0.5626 | `AUTO_PRESENT` |
| `732924ADR050` | JIVITESH G D | 3 | 100.0% | 0.7033 | 0.54s | 0.5773 | `AUTO_PRESENT` |

---

### 5. Audit Trail & Chain of Custody (Key Session Events)

Every camera detection, tracking association, faculty review outcome, and finalization action is logged to an immutable SQLite audit log:

| Event ID | Timestamp (IST) | Event Type | Target Reg ID | Track | Details / Context |
| :---: | :--- | :--- | :---: | :---: | :--- |
| #1 | 23 Oct 2026, 01:57:37 PM IST | `STALE_FACE_RESULT_IGNORED` | `—` | `—` | {"age_seconds": 4.412, "limit_seconds": 1.5} |
| #2 | 23 Oct 2026, 01:57:37 PM IST | `FACE_NOT_ASSOCIATED_TO_PERSON` | `732924ADR044` | `—` | {"geometry_score": 0.0, "result_age_seconds": 0.353} |
| #3 | 23 Oct 2026, 01:57:38 PM IST | `IDENTITY_NOT_STABLE_OR_MISMATCH` | `732924ADR044` | `P1` | {"result_age_seconds": 0.407, "stable_reg_id": null} |
| #4 | 23 Oct 2026, 01:57:39 PM IST | `AUTO_PRESENT_MARKED` | `732924ADR044` | `P1` | {"association_score": 0.8277, "evidence_count": 3, "evidence_s... |
| #5 | 23 Oct 2026, 01:57:49 PM IST | `IDENTITY_NOT_STABLE_OR_MISMATCH` | `732924ADR031` | `P4` | {"result_age_seconds": 0.715, "stable_reg_id": null} |
| #6 | 23 Oct 2026, 01:57:51 PM IST | `AUTO_PRESENT_MARKED` | `732924ADR031` | `P4` | {"association_score": 0.7684, "evidence_count": 3, "evidence_s... |
| #7 | 23 Oct 2026, 01:57:53 PM IST | `PERSON_TRACK_NOT_CURRENT` | `732924ADR031` | `P4` | {"result_age_seconds": 0.398} |
| #8 | 23 Oct 2026, 01:57:54 PM IST | `IDENTITY_NOT_STABLE_OR_MISMATCH` | `732924ADR013` | `P5` | {"result_age_seconds": 0.534, "stable_reg_id": null} |
| #9 | 23 Oct 2026, 01:57:56 PM IST | `AUTO_PRESENT_MARKED` | `732924ADR013` | `P5` | {"association_score": 0.495, "evidence_count": 3, "evidence_sh... |
| #10 | 23 Oct 2026, 01:57:59 PM IST | `PERSON_TRACK_NOT_CURRENT` | `732924ADR013` | `P5` | {"result_age_seconds": 0.624} |
| #11 | 23 Oct 2026, 01:58:02 PM IST | `FACE_NOT_ASSOCIATED_TO_PERSON` | `732924ADR035` | `—` | {"geometry_score": 0.0, "result_age_seconds": 0.689} |
| #12 | 23 Oct 2026, 01:58:03 PM IST | `IDENTITY_NOT_STABLE_OR_MISMATCH` | `732924ADR035` | `P5` | {"result_age_seconds": 0.509, "stable_reg_id": "732924ADR013"} |

*(Showing first 12 of 46 audit events recorded for this session. Complete audit history is preserved in SQLite and the exported CSV.)*

---

### 6. Official Data Export Files for Verification

The formal CSV files for this session are exported and ready on disk:

1. **Finalized Attendance Roster CSV:**  
   `reports/attendai_finalized_session_b2c71f3dd99f.csv`
2. **Raw System Attendance Logs CSV:**  
   `reports/attendai_attendance_b2c71f3dd99f.csv`
3. **Comprehensive Audit Trail CSV:**  
   `reports/attendai_audit_b2c71f3dd99f.csv`

---

### 7. Judicial Verification Sign-off

- **System:** AttendAI Edge Presence Intelligence System
- **Hardware:** NVIDIA Jetson AGX Orin Developer Kit (64GB)
- **Language Assistant:** ClassVision AI Assistant (Local Qwen 2.5 3B via Ollama)
- **Faculty Reviewer:** `INDHIRAN S`
- **Verification Status:** **APPROVED & LOCKED**
