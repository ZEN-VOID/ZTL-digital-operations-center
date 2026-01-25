"""
Debug styling issue on ZTL Web UI pages
Investigates why Tailwind v4 styles are not being applied
"""
from playwright.sync_api import sync_playwright
import json

def debug_styling():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Capture console logs
        console_logs = []
        page.on("console", lambda msg: console_logs.append({
            "type": msg.type,
            "text": msg.text
        }))

        # Capture network errors
        network_errors = []
        page.on("requestfailed", lambda request: network_errors.append({
            "url": request.url,
            "failure": request.failure
        }))

        results = {}

        # Test each page
        pages_to_test = [
            ("Home", "http://localhost:3000/home"),
            ("Chat", "http://localhost:3000/chat"),
            ("Resources", "http://localhost:3000/resources")
        ]

        for page_name, url in pages_to_test:
            print(f"\n{'='*60}")
            print(f"Testing {page_name} Page: {url}")
            print(f"{'='*60}")

            console_logs.clear()
            network_errors.clear()

            try:
                page.goto(url, wait_until='networkidle', timeout=10000)

                # 1. Check if globals.css is loaded
                stylesheets = page.evaluate("""() => {
                    return Array.from(document.styleSheets).map(sheet => {
                        try {
                            return {
                                href: sheet.href,
                                rulesCount: sheet.cssRules?.length || 0
                            };
                        } catch (e) {
                            return { href: sheet.href, error: e.message };
                        }
                    });
                }""")

                # 2. Check computed styles on body
                body_styles = page.evaluate("""() => {
                    const body = document.body;
                    const computed = window.getComputedStyle(body);
                    return {
                        backgroundColor: computed.backgroundColor,
                        color: computed.color,
                        fontFamily: computed.fontFamily
                    };
                }""")

                # 3. Check if Tailwind classes are working
                tailwind_test = page.evaluate("""() => {
                    const testDiv = document.createElement('div');
                    testDiv.className = 'bg-cyber-bg-primary text-neon-cyan';
                    document.body.appendChild(testDiv);
                    const computed = window.getComputedStyle(testDiv);
                    const result = {
                        backgroundColor: computed.backgroundColor,
                        color: computed.color
                    };
                    testDiv.remove();
                    return result;
                }""")

                # 4. Get all loaded CSS custom properties
                css_vars = page.evaluate("""() => {
                    const styles = window.getComputedStyle(document.documentElement);
                    const vars = {};
                    for (let i = 0; i < styles.length; i++) {
                        const prop = styles[i];
                        if (prop.startsWith('--')) {
                            vars[prop] = styles.getPropertyValue(prop).trim();
                        }
                    }
                    return vars;
                }""")

                # 5. Take screenshot
                screenshot_path = f"/tmp/{page_name.lower()}_page.png"
                page.screenshot(path=screenshot_path, full_page=True)

                results[page_name] = {
                    "url": url,
                    "stylesheets": stylesheets,
                    "body_styles": body_styles,
                    "tailwind_test": tailwind_test,
                    "css_vars_count": len(css_vars),
                    "css_vars_sample": dict(list(css_vars.items())[:10]),
                    "console_logs": console_logs.copy(),
                    "network_errors": network_errors.copy(),
                    "screenshot": screenshot_path
                }

                print(f"\n✅ Successfully loaded {page_name}")
                print(f"📄 Stylesheets loaded: {len(stylesheets)}")
                print(f"🎨 Body background: {body_styles['backgroundColor']}")
                print(f"🎨 Body color: {body_styles['color']}")
                print(f"🔧 CSS variables found: {len(css_vars)}")
                print(f"📸 Screenshot saved: {screenshot_path}")

                if console_logs:
                    print(f"\n⚠️  Console logs ({len(console_logs)}):")
                    for log in console_logs[:5]:
                        print(f"  [{log['type']}] {log['text']}")

                if network_errors:
                    print(f"\n❌ Network errors ({len(network_errors)}):")
                    for err in network_errors:
                        print(f"  {err['url']}: {err['failure']}")

            except Exception as e:
                results[page_name] = {
                    "url": url,
                    "error": str(e)
                }
                print(f"\n❌ Error loading {page_name}: {e}")

        browser.close()

        # Save detailed results
        with open('/tmp/styling_debug_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*60}")
        print("📊 Full results saved to: /tmp/styling_debug_results.json")
        print(f"{'='*60}")

        return results

if __name__ == "__main__":
    debug_styling()
