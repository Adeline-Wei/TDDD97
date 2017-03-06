import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class WebProgrammingLab4(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Firefox()
		cls.driver.implicitly_wait(2)
		cls.driver.get('http://127.0.0.1:5004/')
		cls.verificationErrors = []		


	def test_01_log_in(self):
		driver = self.driver
		self.assertIn('TDDD97', driver.title)
		driver.find_element(By.NAME, 'emailsignin').send_keys('111@gmail.com')
		driver.find_element(By.NAME, 'pwsignin').send_keys('111111')
		driver.find_element(By.NAME, 'login').click()
		time.sleep(0.5)
		self.assertTrue(driver.find_element(By.CLASS_NAME, 'tab'))
		

	def test_02_post_a_message(self):
		driver = self.driver
		driver.find_element(By.ID, 'userTextareaHome').send_keys('post from selenium')
		driver.find_element(By.NAME, 'postText').click()
		time.sleep(0.5)
		parent_elem = driver.find_element(By.ID, 'userMessagesHome')
		child_elems = parent_elem.find_elements(By.TAG_NAME, 'div')
		message = child_elems[len(child_elems)-1].get_attribute('innerHTML')
		index = message.index(':')
		self.assertEqual(message[index+2:], 'post from selenium')


	def test_03_find_a_user(self):
		driver = self.driver
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'browse')))
		driver.find_element(By.NAME, 'browse').click()
		driver.find_element(By.ID, 'userEmail').send_keys('222@gmail.com')
		driver.find_element(By.NAME, 'searchThisUser').click()
		time.sleep(0.5)
		style = driver.find_element(By.ID, 'ifUserFounded').get_attribute("style")
		self.assertEqual(style, 'display: block;')


	def test_04_change_password(self):
		driver = self.driver
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'account')))
		driver.find_element(By.NAME, 'account').click()
		driver.find_element(By.NAME, 'oldpw').send_keys('111111')
		driver.find_element(By.NAME, 'newpw').send_keys('111111')
		driver.find_element(By.NAME, 'changepw').click()
		elem = driver.find_element(By.ID, 'accountAlert')
		time.sleep(0.5)
		self.assertEqual(elem.get_attribute('innerHTML'), 'Password changed!')


	def test_05_sign_out(self):
		driver = self.driver
		WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'account')))
		driver.find_element(By.NAME, 'account').click()
		driver.find_element(By.NAME, 'signout').click()
		time.sleep(0.5)
		self.assertTrue(driver.find_element(By.CLASS_NAME, 'slogan'))


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(WebProgrammingLab4)
	unittest.TextTestRunner(verbosity=2).run(suite)

