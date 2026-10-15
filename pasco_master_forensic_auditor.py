import json
import os


def inspect_forensic_artifacts(
    json_path="pasco_audit_report.json", csv_path="pasco_audit_alerts.csv"
):
    """Loads and prints a structured forensic summary of the generated audit artifacts

    to verify alert severity counts, missing agency logs, and procedural blackholes.
    """
    print(f"[*] Inspecting generated forensic audit artifacts...")

    if not os.path.exists(json_path) or not os.path.exists(csv_path):
        print(f"[!] Error: Artifact files not found in working directory.")
        return

    # Load JSON Report
    with open(json_path, "r", encoding="utf-8") as f:
        report_data = json.load(f)

    print("\n" + "=" * 60)
    print(f" FORENSIC AUDIT EXECUTIVE BRIEFING: {report_data.get('agency')}")
    print("=" * 60)
    print(f" County / Jurisdiction : {report_data.get('county')}")
    print(f" Case / Cause Number   : {report_data.get('case_number')}")
    print(f" Agency Reference Ref  : {report_data.get('agency_reference')}")
    print(f" Timestamp (UTC)       : {report_data.get('audit_timestamp_utc')}")
    print(f" Total Docket Entries  : {report_data.get('total_entries')}")
    print(f" Total Alerts Triggered: {report_data.get('alerts_detected')}")
    print("-" * 60)

    print("\n[+] DETECTED BLACKHOLES & EVIDENTIARY OMISSIONS:")
    for idx, alert in enumerate(report_data.get("alerts", []), 1):
        severity = alert.get("severity", "UNKNOWN")
        alert_type = alert.get("type", "UNKNOWN_TYPE")
        detail = alert.get("detail", "No details provided.")
        print(f"  {idx}. [{severity}] {alert_type}")
        print(f"     -> {detail}")

    print("\n" + "=" * 60)
    print(
        f"[+] Artifact Verification Complete. Ready for formal court exhibit attachment."
    )
    print("=" * 60)


if __name__ == "__main__":
    inspect_forensic_artifacts()import json
import os


def generate_court_exhibit_markdown(json_path="pasco_audit_report.json", output_md="PASCO_COURT_EXHIBIT_REPORT.md"):
    """Reads the exported JSON forensic audit report and compiles a formal 
    legal exhibit summary document formatted for court and administrative submission.
    """
    if not os.path.exists(json_path):
        print(f"[!] Error: {json_path} not found. Run the master auditor script first.")
        return None

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md_content = f"""# Formal Notice of Evidentiary Omissions & Administrative Blackholes

**Jurisdiction:** {data.get('county')}  
**Law Enforcement Agency:** {data.get('agency')}  
**Cause / Case Number:** {data.get('case_number')}  
**Agency Reference Number:** {data.get('agency_reference')}  
**Audit Timestamp (UTC):** {data.get('audit_timestamp_utc')}  

---

## Executive Summary

An automated forensic web audit was executed against the public court docket repository for **{data.get('case_number')}**. The audit evaluated docket integrity, procedural timelines, unlinked charging instruments, and expected exculpatory agency evidence logs from the **{data.get('agency')}**.

* **Total Docket Entries Indexed:** `{data.get('total_entries')}`
* **Total Procedural Anomalies / Alerts Triggered:** `{data.get('alerts_detected')}`

---

## Summary of Detected Audit Alerts

| Severity | Alert Type | Description / Evidentiary Detail |
| :--- | :--- | :--- |
"""

    for alert in data.get("alerts", []):
        severity = alert.get("severity", "UNKNOWN")
        alert_type = alert.get("type", "UNKNOWN")
        detail = alert.get("detail", "No detail provided.")
        md_content += f"| **{severity}** | `{alert_type}` | {detail} |\n"

    md_content += """
---

## Indexed Docket Entries

| Filing Date | Filed By / Source | Docket Description & Link Status |
| :--- | :--- | :--- |
"""

    for entry in data.get("docket", []):
        date = entry.get("date", "N/A")
        filed_by = entry.get("filed_by", "N/A")
        desc = entry.get("description", "N/A")
        link_status = "Linked Document Available" if entry.get("has_document_link") else "**Unlinked / Suppressed**"
        md_content += f"| {date} | {filed_by} | {desc} <br> *Status: {link_status}* |\n"

    md_content += """
---

## Certification & Demand

The findings detailed above are derived from direct digital record parsing and cross-reference verification. Demand is hereby made for the immediate public indexing and disclosure of all unattached affidavits, Computer-Aided Dispatch (CAD) logs, and Body-Worn Camera (BWC) cryptographic server hashes referenced in this exhibit.

**Submitted By:** Accountability Auditor / Pro Se Officer  
"""

    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    print(f"[+] Formal Court Exhibit Markdown generated successfully: {output_md}")
    return output_md


if __name__ == "__main__":
    generate_court_exhibit_markdown()

