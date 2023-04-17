# # playwright codegen demo.playwright.dev/todomvc

# import pandas as pd

# csv = pd.read_csv("busan_Restaurant.csv")
# print(csv)
# name = csv['업소명'][0]
# print(name)

# for i in range(len(csv)):
#     name = csv['업소명'][i]
#     print(name)

# name = "대디돈스택"
# address = "부산 영도구 태종로 759 신흥하리상가 2층"

# # def scrapping(name, address):
    
    

# ##################################################
# # import re
# # from playwright.sync_api import Page, expect


# # def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):
# #     page.goto("https://playwright.dev/")

# #     # Expect a title "to contain" a substring.
# #     expect(page).to_have_title(re.compile("Playwright"))

# #     # create a locator
# #     get_started = page.get_by_role("link", name="Get started")

# #     # Expect an attribute "to be strictly equal" to the value.
# #     expect(get_started).to_have_attribute("href", "/docs/intro")

# #     # Click the get started link.
# #     get_started.click()

# #     # Expects the URL to contain intro.
# #     expect(page).to_have_url(re.compile(".*intro"))

# # if __name__ == '__main__':
# #     test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(Page)
    
# ##################################################


# # # # print("hello world")
# # # import re
# # # from playwright.sync_api import Page, expect


# # # def test_homepage_has_Playwright_in_title_and_get_started_link_linking_to_the_intro_page(page: Page):
# # #     page.goto("https://playwright.dev/")

# # #     # Expect a title "to contain" a substring.
# # #     expect(page).to_have_title(re.compile("Playwright"))

# # #     # create a locator
# # #     get_started = page.get_by_role("link", name="Get started")

# # #     # Expect an attribute "to be strictly equal" to the value.
# # #     expect(get_started).to_have_attribute("href", "/docs/intro")

# # #     # Click the get started link.
# # #     get_started.click()

# # #     # Expects the URL to contain intro.
# # #     expect(page).to_have_url(re.compile(".*intro"))

# # from playwright.sync_api import sync_playwright

# # with sync_playwright() as p:
# #     # Make sure to run headed.
# #     browser = p.chromium.launch(headless=False)

# #     # Setup context however you like.
# #     context = browser.new_context() # Pass any options
# #     context.route('**/*', lambda route: route.continue_())

# #     # Pause the page, and start recording manually.
# #     page = context.new_page()
# #     page.pause()