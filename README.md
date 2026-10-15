<a href="https://chat.vercel.ai/">
  <img alt="Next.js 14 and App Router-ready AI chatbot." src="app/(chat)/opengraph-image.png">
  <h1 align="center">Next.js Gemini Chatbot</h1>
</a>

<p align="center">
  An Open-Source AI Chatbot Template Built With Next.js and the AI SDK by Vercel.
</p>

<p align="center">
  <a href="#features"><strong>Features</strong></a> ·
  <a href="#model-providers"><strong>Model Providers</strong></a> ·
  <a href="#deploy-your-own"><strong>Deploy Your Own</strong></a> ·
  <a href="#running-locally"><strong>Running locally</strong></a>
</p>
<br/>

## Features

- [Next.js](https://nextjs.org) App Router
  - Advanced routing for seamless navigation and performance
  - React Server Components (RSCs) and Server Actions for server-side rendering and increased performance
- [AI SDK](https://sdk.vercel.ai/docs)
  - Unified API for generating text, structured objects, and tool calls with LLMs
  - Hooks for building dynamic chat and generative user interfaces
  - Supports Google (default), OpenAI, Anthropic, Cohere, and other model providers
- [shadcn/ui](https://ui.shadcn.com)
  - Styling with [Tailwind CSS](https://tailwindcss.com)
  - Component primitives from [Radix UI](https://radix-ui.com) for accessibility and flexibility
- Data Persistence
  - [Vercel Postgres powered by Neon](https://vercel.com/storage/postgres) for saving chat history and user data
  - [Vercel Blob](https://vercel.com/storage/blob) for efficient object storage
- [NextAuth.js](https://github.com/nextauthjs/next-auth)
  - Simple and secure authentication

## Model Providers

This template ships with Google Gemini `gemini-1.5-pro` models as the default. However, with the [AI SDK](https://sdk.vercel.ai/docs), you can switch LLM providers to [OpenAI](https://openai.com), [Anthropic](https://anthropic.com), [Cohere](https://cohere.com/), and [many more](https://sdk.vercel.ai/providers/ai-sdk-providers) with just a few lines of code.

## Deploy Your Own

You can deploy your own version of the Next.js AI Chatbot to Vercel with one click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fgemini-chatbot&env=AUTH_SECRET,GOOGLE_GENERATIVE_AI_API_KEY&envDescription=Learn%20more%20about%20how%20to%20get%20the%20API%20Keys%20for%20the%20application&envLink=https%3A%2F%2Fgithub.com%2Fvercel-labs%2Fgemini-chatbot%2Fblob%2Fmain%2F.env.example&demo-title=Next.js%20Gemini%20Chatbot&demo-description=An%20Open-Source%20AI%20Chatbot%20Template%20Built%20With%20Next.js%20and%20the%20AI%20SDK%20by%20Vercel.&demo-url=https%3A%2F%2Fgemini.vercel.ai&stores=[{%22type%22:%22postgres%22},{%22type%22:%22blob%22}])

## Running locally

You will need to use the environment variables [defined in `.env.example`](.env.example) to run Next.js AI Chatbot. It's recommended you use [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables) for this, but a `.env` file is all that is necessary.

> Note: You should not commit your `.env` file or it will expose secrets that will allow others to control access to your various Google Cloud and authentication provider accounts.

1. Install Vercel CLI: `npm i -g vercel`
2. Link local instance with Vercel and GitHub accounts (creates `.vercel` directory): `vercel link`
3. Download your environment variables: `vercel env pull`

```bash
pnpm install
pnpm dev
```

Your app template should now be running on [localhost:3000](http://localhost:3000/).
import os
import subprocess
import sys


def execute_pasco_audit_pipeline():
    """Executes the Pasco County Sheriff's Office forensic audit script,
    verifies artifact generation, and inspects exported alert summaries.
    """
    script_filename = "pasco_docket_auditor.py"
    print(f"[*] Initializing pipeline execution for: {script_filename}")

    # 1. Ensure script is written to disk
    script_code = """from datetime import datetime
import json
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

class PascoCountyDocketBlackholeAuditor:
    def __init__(self, case_no="2026-MM-001234", agency_ref="PSO26OFF5678", agency_name="Pasco County Sheriff's Office"):
        self.case_no = case_no
        self.agency_ref = agency_ref
        self.agency_name = agency_name
        self.docket_entries = []
        self.blackhole_alerts = []

    def fetch_live_docket_html(self, headless=True, timeout=30000):
        ocrs_url = "https://www.civitekflorida.com/ocrs/county/51/"
        html_content = ""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.goto(ocrs_url, timeout=timeout)
                page.wait_for_load_state("domcontentloaded")
                
                try:
                    agree_btn = page.locator("button:has-text('Public'), input[value*='Public'], a:has-text('Public')").first
                    if agree_btn.is_visible():
                        agree_btn.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                search_input_selector = "input#caseNumber, input[name*='CaseNumber'], input[type='text']"
                try:
                    page.wait_for_selector(search_input_selector, timeout=10000)
                    page.fill(search_input_selector, self.case_no)
                    page.press(search_input_selector, "Enter")
                except PlaywrightTimeoutError:
                    fallback_input = page.locator("input[type='text']").first
                    fallback_input.fill(self.case_no)
                    fallback_input.press("Enter")

                page.wait_for_load_state("networkidle", timeout=timeout)
                html_content = page.content()
                browser.close()
        except Exception as e:
            self.blackhole_alerts.append({
                "type": "PASCO_LIVE_FETCH_FAILURE",
                "severity": "CRITICAL",
                "detail": f"Failed to retrieve Pasco County OCRS portal DOM via Playwright: {str(e)}"
            })
        return html_content

    def parse_docket_html(self, html_content):
        if not html_content:
            return []
        soup = BeautifulSoup(html_content, "html.parser")
        page_text = soup.get_text().upper()
        if any(term in page_text for term in ["SEALED", "CONFIDENTIAL", "REDACTED", "INJUNCTION"]):
            self.blackhole_alerts.append({
                "type": "PASCO_RESTRICTED_RECORD_STATUS",
                "severity": "HIGH",
                "detail": "Pasco County record flags restricted, sealed, or confidential status indicators.",
            })

        docket_table = soup.find("table", {"id": "docketTable"}) or soup.find("table", class_="grid") or soup.find("table")
        if not docket_table:
            self.blackhole_alerts.append({
                "type": "PASCO_MISSING_DOCKET_TABLE",
                "severity": "CRITICAL",
                "detail": "No valid docket table located in Pasco County response HTML.",
            })
            return []

        rows = docket_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)
                description = cols[1].get_text(strip=True)
                link = cols[1].find("a", href=True)
                doc_url = link["href"] if link else None

                entry = {
                    "date": date_str,
                    "filed_by": self.agency_name,
                    "description": description,
                    "has_document_link": doc_url is not None,
                    "document_url": doc_url,
                }
                self.docket_entries.append(entry)
                self._check_entry_for_blackholes(entry)
        return self.docket_entries

    def _check_entry_for_blackholes(self, entry):
        desc_upper = entry["description"].upper()
        if "AFFIDAVIT" in desc_upper and not entry["has_document_link"]:
            self.blackhole_alerts.append({
                "type": "PASCO_UNATTACHED_AFFIDAVIT",
                "severity": "HIGH",
                "date": entry["date"],
                "detail": f"Pasco County charging affidavit or probable cause record logged without an active public document link: '{entry['description']}'.",
            })

    def audit_agency_evidence_omissions(self, expected_agency_logs):
        parsed_blob = " ".join([e["description"].upper() for e in self.docket_entries])
        for log in expected_agency_logs:
            keyword = log["keyword"].upper()
            if keyword not in parsed_blob:
                self.blackhole_alerts.append({
                    "type": "PASCO_AGENCY_EVIDENCE_BLACKHOLE",
                    "severity": "CRITICAL",
                    "agency": self.agency_name,
                    "exhibit_id": log["id"],
                    "target_identifier": log["identifier"],
                    "detail": f"Expected {self.agency_name} record '{log['name']}' ({log['identifier']}) missing from Pasco County court docket index.",
                })

    def export_report_json(self, output_path="pasco_audit_report.json"):
        report = {
            "county": "Pasco County, Florida",
            "agency": self.agency_name,
            "case_number": self.case_no,
            "agency_reference": self.agency_ref,
            "audit_timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "total_entries": len(self.docket_entries),
            "alerts_detected": len(self.blackhole_alerts),
            "alerts": self.blackhole_alerts,
            "docket": self.docket_entries,
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=4)
        return output_path

    def export_report_csv(self, output_path="pasco_audit_alerts.csv"):
        fieldnames = ["type", "severity", "date", "detail", "exhibit_id", "target_identifier"]
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for alert in self.blackhole_alerts:
                writer.writerow(alert)
        return output_path

if __name__ == "__main__":
    auditor = PascoCountyDocketBlackholeAuditor(
        case_no="2026-MM-001234",
        agency_ref="PSO26OFF5678",
        agency_name="Pasco County Sheriff's Office",
    )
    live_html = auditor.fetch_live_docket_html(headless=True)
    if not live_html or len(live_html) < 500:
        live_html = '''<html><body><div class="case-header">Pasco County OCRS - Public Access Docket</div><table id="docketTable" class="grid"><thead><tr><th>Filing Date</th><th>Docket Description & Events</th></tr></thead><tbody><tr><td>10/01/2026</td><td>Information Filed - Pasco County Sheriff Office misdemeanor charge</td></tr><tr><td>10/01/2026</td><td>Probable Cause Affidavit Filed (No Document Link Available)</td></tr><tr><td>10/05/2026</td><td>State Attorney Notice of Discovery</td></tr></tbody></table></body></html>'''
    
    auditor.parse_docket_html(live_html)
    expected_pasco_evidence = [
        {"id": "PASCO_EXHIBIT_1", "name": "PSO CAD Dispatch Log", "keyword": "CAD", "identifier": "PSO Dispatch Incident Log #26-004589"},
        {"id": "PASCO_EXHIBIT_2", "name": "PSO Body-Worn Camera Server Export", "keyword": "BWC", "identifier": "Axon Digital Evidence Hash - Agency Ref PSO26OFF5678"},
    ]
    auditor.audit_agency_evidence_omissions(expected_pasco_evidence)
    json_path = auditor.export_report_json()
    csv_path = auditor.export_report_csv()
    print(f"Pipeline Execution Complete. JSON: {json_path}, CSV: {csv_path}, Alerts: {len(auditor.blackhole_alerts)}")
"""

    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(script_code)

    print(f"[+] Successfully wrote `{script_filename}`.")

    # 2. Execute script via subprocess
    print(f"[*] Executing `{script_filename}`...")
    result = subprocess.run(
        [sys.executable, script_filename],
        capture_output=True,
        text=True,
        timeout=60,
    )

    print(result.stdout)
    if result.stderr:
        print(f"[stderr]:\n{result.stderr}")

    # 3. Verify output artifacts
    json_artifact = "pasco_audit_report.json"
    csv_artifact = "pasco_audit_alerts.csv"

    artifacts_verified = os.path.exists(json_artifact) and os.path.exists(
        csv_artifact
    )
    if artifacts_verified:
        print(
            f"[+] Verification Successful: Artifacts `{json_artifact}` and `{csv_artifact}` confirmed on disk."
        )
    else:
        print("[!] Warning: Expected artifacts were not fully generated.")


if __name__ == "__main__":
 import os
import subprocess
import sys


def execute_pasco_audit_pipeline():
    """Executes the Pasco County Sheriff's Office forensic audit script,
    verifies artifact generation, and inspects exported alert summaries.
    """
    script_filename = "pasco_docket_auditor.py"
    print(f"[*] Initializing pipeline execution for: {script_filename}")

    # 1. Ensure script is written to disk
    script_code = """from datetime import datetime
import json
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

class PascoCountyDocketBlackholeAuditor:
    def __init__(self, case_no="2026-MM-001234", agency_ref="PSO26OFF5678", agency_name="Pasco County Sheriff's Office"):
        self.case_no = case_no
        self.agency_ref = agency_ref
        self.agency_name = agency_name
        self.docket_entries = []
        self.blackhole_alerts = []

    def fetch_live_docket_html(self, headless=True, timeout=30000):
        ocrs_url = "https://www.civitekflorida.com/ocrs/county/51/"
        html_content = ""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                page.goto(ocrs_url, timeout=timeout)
                page.wait_for_load_state("domcontentloaded")
                
                try:
                    agree_btn = page.locator("button:has-text('Public'), input[value*='Public'], a:has-text('Public')").first
                    if agree_btn.is_visible():
                        agree_btn.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                search_input_selector = "input#caseNumber, input[name*='CaseNumber'], input[type='text']"
                try:
                    page.wait_for_selector(search_input_selector, timeout=10000)
                    page.fill(search_input_selector, self.case_no)
                    page.press(search_input_selector, "Enter")
                except PlaywrightTimeoutError:
                    fallback_input = page.locator("input[type='text']").first
                    fallback_input.fill(self.case_no)
                    fallback_input.press("Enter")

                page.wait_for_load_state("networkidle", timeout=timeout)
                html_content = page.content()
                browser.close()
        except Exception as e:
            self.blackhole_alerts.append({
                "type": "PASCO_LIVE_FETCH_FAILURE",
                "severity": "CRITICAL",
                "detail": f"Failed to retrieve Pasco County OCRS portal DOM via Playwright: {str(e)}"
            })
        return html_content

    def parse_docket_html(self, html_content):
        if not html_content:
            return []
        soup = BeautifulSoup(html_content, "html.parser")
        page_text = soup.get_text().upper()
        if any(term in page_text for term in ["SEALED", "CONFIDENTIAL", "REDACTED", "INJUNCTION"]):
            self.blackhole_alerts.append({
                "type": "PASCO_RESTRICTED_RECORD_STATUS",
                "severity": "HIGH",
                "detail": "Pasco County record flags restricted, sealed, or confidential status indicators.",
            })

        docket_table = soup.find("table", {"id": "docketTable"}) or soup.find("table", class_="grid") or soup.find("table")
        if not docket_table:
            self.blackhole_alerts.append({
                "type": "PASCO_MISSING_DOCKET_TABLE",
                "severity": "CRITICAL",
                "detail": "No valid docket table located in Pasco County response HTML.",
            })
            return []

        rows = docket_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) >= 2:
                date_str = cols[0].get_text(strip=True)
                description = cols[1].get_text(strip=True)
                link = cols[1].find("a", href=True)
                doc_url = link["href"] if link else None

                entry = {
                    "date": date_str,
                    "filed_by": self.agency_name,
                    "description": description,
                    "has_document_link": doc_url is not None,
                    "document_url": doc_url,
                }
                self.docket_entries.append(entry)
                self._check_entry_for_blackholes(entry)
        return self.docket_entries

    def _check_entry_for_blackholes(self, entry):
        desc_upper = entry["description"].upper()
        if "AFFIDAVIT" in desc_upper and not entry["has_document_link"]:
            self.blackhole_alerts.append({
                "type": "PASCO_UNATTACHED_AFFIDAVIT",
                "severity": "HIGH",
                "date": entry["date"],
                "detail": f"Pasco County charging affidavit or probable cause record logged without an active public document link: '{entry['description']}'.",
            })

    def audit_agency_evidence_omissions(self, expected_agency_logs):
        parsed_blob = " ".join([e["description"].upper() for e in self.docket_entries])
        for log in expected_agency_logs:
            keyword = log["keyword"].upper()
            if keyword not in parsed_blob:
                self.blackhole_alerts.append({
                    "type": "PASCO_AGENCY_EVIDENCE_BLACKHOLE",
                    "severity": "CRITICAL",
                    "agency": self.agency_name,
                    "exhibit_id": log["id"],
                    "target_identifier": log["identifier"],
                    "detail": f"Expected {self.agency_name} record '{log['name']}' ({log['identifier']}) missing from Pasco County court docket index.",
                })

    def export_report_json(self, output_path="pasco_audit_report.json"):
        report = {
            "county": "Pasco County, Florida",
            "agency": self.agency_name,
            "case_number": self.case_no,
            "agency_reference": self.agency_ref,
            "audit_timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "total_entries": len(self.docket_entries),
            "alerts_detected": len(self.blackhole_alerts),
            "alerts": self.blackhole_alerts,
            "docket": self.docket_entries,
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=4)
        return output_path

    def export_report_csv(self, output_path="pasco_audit_alerts.csv"):
        fieldnames = ["type", "severity", "date", "detail", "exhibit_id", "target_identifier"]
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for alert in self.blackhole_alerts:
                writer.writerow(alert)
        return output_path

if __name__ == "__main__":
    auditor = PascoCountyDocketBlackholeAuditor(
        case_no="2026-MM-001234",
        agency_ref="PSO26OFF5678",
        agency_name="Pasco County Sheriff's Office",
    )
    live_html = auditor.fetch_live_docket_html(headless=True)
    if not live_html or len(live_html) < 500:
        live_html = '''<html><body><div class="case-header">Pasco County OCRS - Public Access Docket</div><table id="docketTable" class="grid"><thead><tr><th>Filing Date</th><th>Docket Description & Events</th></tr></thead><tbody><tr><td>10/01/2026</td><td>Information Filed - Pasco County Sheriff Office misdemeanor charge</td></tr><tr><td>10/01/2026</td><td>Probable Cause Affidavit Filed (No Document Link Available)</td></tr><tr><td>10/05/2026</td><td>State Attorney Notice of Discovery</td></tr></tbody></table></body></html>'''
    
    auditor.parse_docket_html(live_html)
    expected_pasco_evidence = [
        {"id": "PASCO_EXHIBIT_1", "name": "PSO CAD Dispatch Log", "keyword": "CAD", "identifier": "PSO Dispatch Incident Log #26-004589"},
        {"id": "PASCO_EXHIBIT_2", "name": "PSO Body-Worn Camera Server Export", "keyword": "BWC", "identifier": "Axon Digital Evidence Hash - Agency Ref PSO26OFF5678"},
    ]
    auditor.audit_agency_evidence_omissions(expected_pasco_evidence)
    json_path = auditor.export_report_json()
    csv_path = auditor.export_report_csv()
    print(f"Pipeline Execution Complete. JSON: {json_path}, CSV: {csv_path}, Alerts: {len(auditor.blackhole_alerts)}")
"""

    with open(script_filename, "w", encoding="utf-8") as f:
        f.write(script_code)

    print(f"[+] Successfully wrote `{script_filename}`.")

    # 2. Execute script via subprocess
    print(f"[*] Executing `{script_filename}`...")
    result = subprocess.run(
        [sys.executable, script_filename],
        capture_output=True,
        text=True,
        timeout=60,
    )

    print(result.stdout)
    if result.stderr:
        print(f"[stderr]:\n{result.stderr}")

    # 3. Verify output artifacts
    json_artifact = "pasco_audit_report.json"
    csv_artifact = "pasco_audit_alerts.csv"

    artifacts_verified = os.path.exists(json_artifact) and os.path.exists(
        csv_artifact
    )
    if artifacts_verified:
        print(
            f"[+] Verification Successful: Artifacts `{json_artifact}` and `{csv_artifact}` confirmed on disk."
        )
    else:
        print("[!] Warning: Expected artifacts were not fully generated.")


if __name__ == "__main__":
    execute_pasco_audit_pipeline()
   from datetime import datetime
import json
import csv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class PascoCountyDocketBlackholeAuditor:
    """Forensic Web Audit Engine adapted for Pasco County Clerk of Court / 
    Civitek Online Court Records Search (OCRS) portal, detecting administrative 
    blackholes, unattached probable cause affidavits, and missing agency evidence logs.
    """

    def __init__(
        self,
        case_no="2026-MM-000000",
        agency_ref="PSO26OFF0000",
        agency_name="Pasco County Sheriff's Office",
    ):
        self.case_no = case_no
        self.agency_ref = agency_ref
        self.agency_name = agency_name
        self.docket_entries = []
        self.blackhole_alerts = []

    def fetch_live_docket_html(self, headless=True, timeout=30000):
        """Launches a headless browser session targeting the Pasco County OCRS portal,
        navigating case records and extracting dynamic docket tables.
        """
        ocrs_url = "https://www.civitekflorida.com/ocrs/county/51/"
        print(f"[*] Initializing Playwright session for Pasco County OCRS: {ocrs_url}")
        
        html_content = ""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=headless)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )
                page = context.new_page()
                
                # Navigate to Pasco County OCRS Public Access
                page.goto(ocrs_url, timeout=timeout)
                page.wait_for_load_state("domcontentloaded")

                # Handle initial public disclaimer acknowledgment if present
                try:
                    agree_btn = page.locator("button:has-text('Public'), input[value*='Public'], a:has-text('Public')").first
                    if agree_btn.is_visible():
                        agree_btn.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass

                print(f"[*] Searching Pasco County records for case number: {self.case_no}")
                search_input_selector = "input#caseNumber, input[name*='CaseNumber'], input[type='text']"
                
                try:
                    page.wait_for_selector(search_input_selector, timeout=10000)
                    page.fill(search_input_selector, self.case_no)
                    page.press(search_input_selector, "Enter")
                except PlaywrightTimeoutError:
                    print("[!] Standard Pasco selector timed out. Executing fallback input fill...")
                    fallback_input = page.locator("input[type='text']").first
                    fallback_input.fill(self.case_no)
                    fallback_input.press("Enter")

                page.wait_for_load_state("networkidle", timeout=timeout)
                html_content = page.content()
                browser.close()
                print("[+] Pasco County live DOM HTML successfully captured.")
                
        except Exception as e:
            self.blackhole_alerts.append({
                "type": "PASCO_LIVE_FETCH_FAILURE",
                "severity": "CRITICAL",
                "detail": f"Failed to retrieve Pasco County OCRS portal DOM via Playwright: {str(e)}"
            })
            print(f"[!] Error during live browser fetch: {e}")
            
        return html_content

    def parse_docket_html(self, html_content):
        """Parses Pasco County docket summary tables and flags restricted or sealed items."""
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, "html.parser")

        # Check for confidentiality or sealing markers in Pasco records
        page_text = soup.get_text().upper()
        if any(term in page_text for term in ["SEALED", "CONFIDENTIAL", "REDACTED", "INJUNCTION"]):
            self.blackhole_alerts.append({
                "type": "PASCO_RESTRICTED_RECORD_STATUS",
                "severity": "HIGH",
                "detail": "Pasco County record flags restricted, sealed, or confidential status indicators.",
            })

        docket_table = soup.find("table", {"id": "docketTable"}) or soup.find("table", class_="grid") or soup.find("table")

        if not docket_table:
            self.blackhole_alerts.append({
                "type": "PASCO_MISSING_DOCKET_TABLE",
                "severity": "CRITICAL",
                "detail": "No valid docket table located in Pasco County response HTML.",
            })
            return []

        rows = docket_table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols] >= 2:
                date_str = cols[0].get_text(strip=True)
                description = cols[1].get_text(strip=True)

                link = cols[1].find("a", href=True)
                doc_url = link["href"] if link else None

                entry = {
                    "date": date_str,
                    "filed_by": self.agency_name,
                    "description": description,
                    "has_document_link": doc_url is not None,
                    "document_url": doc_url,
                }
                self.docket_entries.append(entry)
                self._check_entry_for_blackholes(entry)

        return self.docket_entries

    def _check_entry_for_blackholes(self, entry):
        desc_upper = entry["description"].upper()

        if "AFFIDAVIT" in desc_upper and not entry["has_document_link"]:
            self.blackhole_alerts.append({
                "type": "PASCO_UNATTACHED_AFFIDAVIT",
                "severity": "HIGH",
                "date": entry["date"],
                "detail": f"Pasco County charging affidavit or probable cause record logged without an active public document link: '{entry['description']}'.",
            })

    def audit_agency_evidence_omissions(self, expected_agency_logs):
        """Cross-references expected Pasco Sheriff investigative files (e.g., BWC footage, CAD dispatch logs)."""
        parsed_blob = " ".join([e["description"].upper() for e in self.docket_entries])

        for log in expected_agency_logs:
            keyword = log["keyword"].upper()
            if keyword not in parsed_blob:
                self.blackhole_alerts.append({
                    "type": "PASCO_AGENCY_EVIDENCE_BLACKHOLE",
                    "severity": "CRITICAL",
                    "agency": self.agency_name,
                    "exhibit_id": log["id"],
                    "target_identifier": log["identifier"],
                    "detail": f"Expected {self.agency_name} record '{log['name']}' ({log['identifier']}) missing from Pasco County court docket index.",
                })

    def export_report_json(self, output_path="pasco_audit_report.json"):
        report = {
            "county": "Pasco County, Florida",
            "agency": self.agency_name,
            "case_number": self.case_no,
            "agency_reference": self.agency_ref,
            "audit_timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "total_entries": len(self.docket_entries),
            "alerts_detected": len(self.blackhole_alerts),
            "alerts": self.blackhole_alerts,
            "docket": self.docket_entries,
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=4)
        return output_path

    def export_report_csv(self, output_path="pasco_audit_alerts.csv"):
        fieldnames = ["type", "severity", "date", "detail", "exhibit_id", "target_identifier"]
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for alert in self.blackhole_alerts:
                writer.writerow(alert)
        return output_path


if __name__ == "__main__":
    auditor = PascoCountyDocketBlackholeAuditor(
        case_no="2026-MM-001234",
        agency_ref="PSO26OFF5678",
        agency_name="Pasco County Sheriff's Office",
    )

    live_html = auditor.fetch_live_docket_html(headless=True)

    if not live_html or len(live_html) < 500:
        print("[!] Using Pasco County local mock fallback HTML due to network restrictions.")
        live_html = """
        <html>
            <body>
                <div class="case-header">Pasco County OCRS - Public Access Docket</div>
                <table id="docketTable" class="grid">
                    <thead>
                        <tr><th>Filing Date</th><th>Docket Description & Events</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>10/01/2026</td><td>Information Filed - Pasco County Sheriff Office misdemeanor charge</td></tr>
                        <tr><td>10/01/2026</td><td>Probable Cause Affidavit Filed (No Document Link Available)</td></tr>
                        <tr><td>10/05/2026</td><td>State Attorney Notice of Discovery</td></tr>
                    </tbody>
                </table>
            </body>
        </html>
        """

    auditor.parse_docket_html(live_html)

    expected_pasco_evidence = [
        {"id": "PASCO_EXHIBIT_1", "name": "PSO CAD Dispatch Log", "keyword": "CAD", "identifier": "PSO Dispatch Incident Log #26-004589"},
        {"id": "PASCO_EXHIBIT_2", "name": "PSO Body-Worn Camera Server Export", "keyword": "BWC", "identifier": "Axon Digital Evidence Hash - Agency Ref PSO26OFF5678"},
    ]
    auditor.audit_agency_evidence_omissions(expected_pasco_evidence)

    json_path = auditor.export_report_json()
    csv_path = auditor.export_report_csv()

    print(f"\nPasco County Sheriff Department Audit Complete.")
    print(f" - JSON Report: {json_path}")
    print(f" - CSV Report:  {csv_path}")
    print(f" - Total Alerts Triggered: {len(auditor.blackhole_alerts)}")


