from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def testCanStartAListAndRetrieveItLater(self):
        # Edith has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

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

        # Whe she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputBox.send_keys(Keys.ENTER)

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find.elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # The page updates again, and now shows both items on her list
        self.fail('Finish the test !')

        # Edith wonders whether the site will remember her list.
        # Then she sees that the site has generated a unique url for her
        # -- there is some explanatory text to that effect

        # She visits that url - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == "__main__":
    unittest.main(warnings='ignore')
