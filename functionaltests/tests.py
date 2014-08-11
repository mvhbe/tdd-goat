from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def checkForRowInListTable(self, rowText):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(rowText, [row.text for row in rows])

    def testCanStartAListAndRetrieveItLater(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        headerText = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', headerText)

        # She's invited to enter a to-do item straight away
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputBox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box
        # (Edith's hobby is tying fly-fishing lures)
        inputBox.send_keys('Buy peacock feathers')

        # Whe she hits enter, she is taken to a new URL
        # and now the pages lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputBox.send_keys(Keys.ENTER)
        edithListUrl = self.browser.current_url
        self.assertRegex(edithListUrl, '/lists/.+')
        self.checkForRowInListTable('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('Use peacock feathers to make a fly')
        inputBox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.checkForRowInListTable('1: Buy peacock feathers')
        self.checkForRowInListTable('2: Use peacock feathers to make a fly')

        # now a new user, Francis, comes along to the site

        ## we use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There's no sing of Edith's list
        self.browser.get(self.live_server_url)
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', pageText)
        self.assertNotIn('make a fly', pageText)

        # Francis starts a new list by entering a new item.
        # He is less interesting than Edith ...
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys("Buy milk")
        inputBox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francisListUrl = self.brower.current_url
        self.assertRegex(francisListUrl, '/lists/.+')
        self.assertNotEqual(francisListUrl, edithListUrl)

        # Again there's no trace of Edith's list
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', pageText)
        self.assertIn('Buy milk', pageText)

        # Satisfied, the both go back to sleep

