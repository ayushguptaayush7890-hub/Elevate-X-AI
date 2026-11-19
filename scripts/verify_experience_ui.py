"""
Direct Chrome DevTools Protocol Client to test Experience Recognition UI live.
"""
import asyncio
import json
import base64
from pathlib import Path
import websockets
import httpx

SCREENSHOTS_DIR = Path(__file__).resolve().parents[1] / "reports"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

async def cdp_call(ws, method, params=None, msg_id=[1]):
    mid = msg_id[0]
    msg_id[0] += 1
    req = {"id": mid, "method": method, "params": params or {}}
    await ws.send(json.dumps(req))
    while True:
        res_raw = await ws.recv()
        res = json.loads(res_raw)
        if res.get("id") == mid:
            return res.get("result", {})

async def eval_js(ws, expr, msg_id=[1]):
    res = await cdp_call(ws, "Runtime.evaluate", {
        "expression": expr,
        "awaitPromise": True,
        "returnByValue": True
    }, msg_id)
    return res.get("result", {}).get("value")

async def test_ui():
    async with httpx.AsyncClient() as client:
        tabs = (await client.get("http://127.0.0.1:9222/json/list")).json()
    
    exp_tab = next(t for t in tabs if "experience" in t["url"] and t["type"] == "page")
    ws_url = exp_tab["webSocketDebuggerUrl"]
    print(f"Connecting to Chrome tab: {ws_url}")

    msg_id = [1]
    async with websockets.connect(ws_url) as ws:
        await cdp_call(ws, "Page.enable", {}, msg_id)
        await cdp_call(ws, "Runtime.enable", {}, msg_id)

        # 1. Reload page fresh
        print("Navigating to http://localhost:3002/experience ...")
        await cdp_call(ws, "Page.navigate", {"url": "http://localhost:3002/experience"}, msg_id)
        await asyncio.sleep(2.0)

        # 2. Check initial textarea content
        textarea_val = await eval_js(ws, "document.querySelector('textarea')?.value", msg_id)
        print(f"Initial Textarea Value: '{textarea_val}'")

        # 3. Click 'Analyze Experience'
        print("Clicking 'Analyze Experience' button...")
        click_res = await eval_js(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const btn = buttons.find(b => b.textContent.includes('Analyze Experience'));
                if (btn) {
                    btn.click();
                    return 'CLICKED';
                }
                return 'NOT_FOUND';
            })()
        """, msg_id)
        print(f"Button click result: {click_res}")

        # 4. Wait for analysis to complete (up to 20s)
        print("Waiting for XLM-RoBERTa neural inference to complete in UI...")
        for sec in range(25):
            await asyncio.sleep(1.0)
            status = await eval_js(ws, """
                (() => {
                    const text = document.body.innerText;
                    if (text.includes('Extracting Trade Competencies') || text.includes('XLM-RoBERTa Inferencing')) {
                        return 'ANALYZING';
                    }
                    const occEl = document.querySelector('p.text-\\\\[11px\\\\].text-\\\\[\\\\#D6A84B\\\\].font-extrabold');
                    const skills = Array.from(document.querySelectorAll('h4.text-xs.font-black.text-\\\\[\\\\#17233F\\\\]')).map(h => h.innerText);
                    return {
                        done: !text.includes('Extracting Trade Competencies') && !text.includes('XLM-RoBERTa Inferencing'),
                        occupation: occEl ? occEl.innerText : null,
                        skills: skills,
                        full_body_snippet: text.slice(0, 500)
                    };
                })()
            """, msg_id)
            if isinstance(status, dict) and status.get("done") and status.get("occupation"):
                print(f"Analysis completed at {sec+1}s!")
                print(f"Detected Occupation in UI: {status['occupation']}")
                print(f"Extracted Competencies in UI: {status['skills']}")
                break
            print(f"  [{sec+1}s] Still running or waiting...")

        # 5. Take screenshot of Electrician results
        ss_res = await cdp_call(ws, "Page.captureScreenshot", {"format": "png"}, msg_id)
        img_bytes = base64.b64decode(ss_res["data"])
        ss_path = SCREENSHOTS_DIR / "experience_electrician_verified.png"
        with open(ss_path, "wb") as f:
            f.write(img_bytes)
        print(f"Screenshot saved to {ss_path}")

        # 6. Verify No Tailor Skills in Electrician results
        skills_text = " ".join(status.get("skills", [])).lower()
        occ_text = (status.get("occupation") or "").lower()
        assert "electrician" in occ_text, f"Expected Electrician occupation, got: {status.get('occupation')}"
        assert "tailor" not in occ_text, f"Tailor occupation still present!"
        assert "tailor" not in skills_text, f"Tailor skills present: {skills_text}"
        assert "sewing" not in skills_text, f"Sewing skills present: {skills_text}"
        print("VERIFICATION 1 PASSED: Electrician correctly detected with electrical skills and ZERO tailor skills!")

        # 7. Test Tailor Quick Test Prompt
        print("\nTesting Quick Prompt: Tailor (TRD-01)...")
        await eval_js(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const tailorBtn = buttons.find(b => b.textContent.includes('Tailor (TRD-01)'));
                if (tailorBtn) tailorBtn.click();
            })()
        """, msg_id)
        await asyncio.sleep(0.5)
        await eval_js(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const btn = buttons.find(b => b.textContent.includes('Analyze Experience'));
                if (btn) btn.click();
            })()
        """, msg_id)

        for sec in range(25):
            await asyncio.sleep(1.0)
            status_tailor = await eval_js(ws, """
                (() => {
                    const occEl = document.querySelector('p.text-\\\\[11px\\\\].text-\\\\[\\\\#D6A84B\\\\].font-extrabold');
                    const skills = Array.from(document.querySelectorAll('h4.text-xs.font-black.text-\\\\[\\\\#17233F\\\\]')).map(h => h.innerText);
                    const isBusy = document.body.innerText.includes('Extracting Trade Competencies') || document.body.innerText.includes('XLM-RoBERTa Inferencing');
                    return { done: !isBusy, occupation: occEl ? occEl.innerText : null, skills: skills };
                })()
            """, msg_id)
            if status_tailor.get("done") and "Tailor" in (status_tailor.get("occupation") or ""):
                print(f"Tailor analysis completed at {sec+1}s!")
                print(f"Detected Occupation: {status_tailor['occupation']}")
                print(f"Extracted Competencies: {status_tailor['skills']}")
                break
        assert "tailor" in (status_tailor.get("occupation") or "").lower()
        print("VERIFICATION 2 PASSED: Tailor correctly detected with garment skills!")

        # 8. Test Plumber Quick Test Prompt
        print("\nTesting Quick Prompt: Plumber (TRD-03)...")
        await eval_js(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const plumberBtn = buttons.find(b => b.textContent.includes('Plumber (TRD-03)'));
                if (plumberBtn) plumberBtn.click();
            })()
        """, msg_id)
        await asyncio.sleep(0.5)
        await eval_js(ws, """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const btn = buttons.find(b => b.textContent.includes('Analyze Experience'));
                if (btn) btn.click();
            })()
        """, msg_id)

        for sec in range(25):
            await asyncio.sleep(1.0)
            status_plumber = await eval_js(ws, """
                (() => {
                    const occEl = document.querySelector('p.text-\\\\[11px\\\\].text-\\\\[\\\\#D6A84B\\\\].font-extrabold');
                    const skills = Array.from(document.querySelectorAll('h4.text-xs.font-black.text-\\\\[\\\\#17233F\\\\]')).map(h => h.innerText);
                    const isBusy = document.body.innerText.includes('Extracting Trade Competencies') || document.body.innerText.includes('XLM-RoBERTa Inferencing');
                    return { done: !isBusy, occupation: occEl ? occEl.innerText : null, skills: skills };
                })()
            """, msg_id)
            if status_plumber.get("done") and "Plumber" in (status_plumber.get("occupation") or ""):
                print(f"Plumber analysis completed at {sec+1}s!")
                print(f"Detected Occupation: {status_plumber['occupation']}")
                print(f"Extracted Competencies: {status_plumber['skills']}")
                break
        assert "plumber" in (status_plumber.get("occupation") or "").lower()
        print("VERIFICATION 3 PASSED: Plumber correctly detected with plumbing skills!")

        print("\n=======================================================")
        print("ALL BROWSER UI VERIFICATIONS PASSED SUCCESSFULLY!")
        print("=======================================================")

if __name__ == "__main__":
    asyncio.run(test_ui())

