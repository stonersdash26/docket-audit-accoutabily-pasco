python plug_in_audit.py
mkdir -p legal_filings/case_2026_mm_001234
cp PASCO_COURT_EXHIBIT_REPORT.md pasco_audit_report.json pasco_audit_alerts.csv pasco_audit_hashes.json legal_filings/case_2026_mm_001234/
ls -la legal_filings/case_2026_mm_001234/

git add legal_filings/
git commit -m "chore: organize verified audit artifacts into formal legal filing directory for Case #2026-MM-001234"
git push origin main
git log -n 1 --oneline

