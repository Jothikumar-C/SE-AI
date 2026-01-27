from playwright.sync_api import sync_playwright

def run_youtube_automation():
    with sync_playwright() as p:
        # Launch browser - headless=False is required to see the interaction
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 7. Open the website
        print("Opening YouTube...")
        page.goto("https://www.youtube.com/")

        # 8. Main Search Bar Selectors (Provided)
        search_bar_css = '#center > yt-searchbox > div.ytSearchboxComponentInputContainer > div > form > input'
        page.wait_for_selector(search_bar_css)

        # 9. Search for “Ilayaraja Songs”
        print("Searching...")
        page.fill(search_bar_css, "Ilayaraja Songs")
        page.press(search_bar_css, "Enter")

        # Wait for results and click the first video title/thumbnail
        # We need to click this to actually reach the page where #movie_player exists
        print("Selecting the first video from results...")
        first_video_result = "ytd-video-renderer #video-title"
        page.wait_for_selector(first_video_result)
        page.click(first_video_result)

        # 10. Video Player Selectors (Provided)
        video_player_css = '#movie_player > div.html5-video-container > video'

        # 11. Play the song
        print("Waiting for video player to load...")
        # We wait for 'attached' because YouTube layers can block 'visibility'
        page.wait_for_selector(video_player_css, state="attached")
        
        # Give the player a tiny moment to buffer/initialize
        page.wait_for_timeout(2000)

        # To ensure it plays, we use a Javascript injection which is the most 
        # reliable way to trigger play in automation.
        print("Triggering Play...")
        page.evaluate("document.querySelector('video').play()")
        
        # Double check with a click in case of browser 'interact-first' policies
        page.click(video_player_css, force=True)

        # 12. Close after 25 seconds
        print("Playback should be active. Enjoying for 25 seconds...")
        page.wait_for_timeout(25000)

        print("Automation complete. Closing.")
        browser.close()

if __name__ == "__main__":
    run_youtube_automation()