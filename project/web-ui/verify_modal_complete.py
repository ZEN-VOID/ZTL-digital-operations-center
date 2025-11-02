"""
Complete Modal Verification
Tests all aspects: opening, display, interaction, and navigation
"""
from playwright.sync_api import sync_playwright
import time

def verify_modal():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        console_logs = []
        page.on("console", lambda msg: console_logs.append({"type": msg.type, "text": msg.text}))

        print("=" * 70)
        print("COMPLETE AGENT DETAIL MODAL VERIFICATION")
        print("=" * 70)

        try:
            # Load page
            page.goto('http://localhost:3000/home', wait_until='networkidle', timeout=10000)
            print("\n[1/5] ✅ Home page loaded")

            # Find and click detail button
            detail_buttons = page.locator('button:has-text("详情")').all()
            print(f"[2/5] ✅ Found {len(detail_buttons)} '详情' buttons")

            # Click first button
            detail_buttons[0].click()
            time.sleep(0.5)

            # Verify modal opened
            modal = page.locator('[role="dialog"]')
            assert modal.is_visible(), "Modal did not open"
            print("[3/5] ✅ Modal opened successfully")

            # Verify modal content
            modal_text = modal.inner_text()

            checks = {
                "Agent Name": "F0-产品经理" in modal_text,
                "Group Badge": "开发组" in modal_text,
                "Description": "产品经理专家" in modal_text or "智能体简介" in modal_text,
                "Model Info": "模型" in modal_text and "sonnet" in modal_text,
                "Tools Section": "可用工具" in modal_text,
                "Start Chat Button": page.locator('[role="dialog"] button:has-text("开始对话")').is_visible(),
                "Close Button": page.locator('[role="dialog"] button:has-text("关闭")').is_visible()
            }

            print("\n[4/5] ✅ Modal Content Verification:")
            all_passed = True
            for check_name, result in checks.items():
                status = "✅" if result else "❌"
                print(f"      {status} {check_name}")
                if not result:
                    all_passed = False

            # Take screenshot
            screenshot_path = '/tmp/modal_complete_verification.png'
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n      📸 Screenshot: {screenshot_path}")

            # Test navigation
            start_chat_btn = page.locator('[role="dialog"] button:has-text("开始对话")')
            start_chat_btn.click()
            page.wait_for_url("**/chat?agent=*", timeout=5000)
            final_url = page.url

            if "/chat" in final_url and "agent=" in final_url:
                print(f"\n[5/5] ✅ Navigation successful")
                print(f"      📍 URL: {final_url}")
            else:
                print(f"\n[5/5] ❌ Navigation failed: {final_url}")
                all_passed = False

            # Check console errors
            errors = [log for log in console_logs if log['type'] == 'error']
            if errors:
                print(f"\n⚠️  Console Errors ({len(errors)}):")
                for err in errors[:3]:
                    print(f"   {err['text'][:100]}")
                all_passed = False
            else:
                print(f"\n✅ No console errors detected")

            # Summary
            print("\n" + "=" * 70)
            if all_passed:
                print("✅ ALL CHECKS PASSED - MODAL FULLY FUNCTIONAL")
            else:
                print("⚠️  SOME CHECKS FAILED - SEE DETAILS ABOVE")
            print("=" * 70)

            return {"status": "success" if all_passed else "partial", "checks": checks}

        except Exception as e:
            print(f"\n❌ Verification failed: {e}")
            page.screenshot(path='/tmp/modal_error.png')
            return {"status": "failed", "error": str(e)}
        finally:
            browser.close()

if __name__ == "__main__":
    verify_modal()
