# AI Development Log (BUILDLOG)

This document logs the usage of AI tools, corrections, and development iterations for the AI Image Understanding & Content Matching Engine capstone project.

---

## Phase 1: Repository Setup & Architecture Design

* **Task:** Initial environment setup, configuration files creation, and architecture planning.
* **AI Tools Used:** ChatGPT / Gemini

### Where AI Helped
* Generated standard baseline configuration files (`.gitignore`, `.env.example`, `capstone.yaml`, `README.md`, `EVIDENCE.md`).
* Formatted the architecture diagram and structured project checklist.

### Where AI Was Wrong or Needed Correction
* **Issue:** Initial file creation commands used Linux syntax (`touch`), which required adjustment for Windows PowerShell environments.
* **Correction:** Adjusted setup commands to be cross-platform compatible.

### Key Technical Decisions
* Framework: Python with FastAPI.
* Vision & Embedding Models: Gemini Flash API (free tier).
* Database: PostgreSQL via Docker.