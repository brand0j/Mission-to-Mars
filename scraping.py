

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt 



def scrape_all():

	# Set up Splinter
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=True)

	news_title, news_paragraph = mars_news(browser)


	data = {
		"news_title": news_title,
		"news_paragraph": news_paragraph,
		"featured_image": featured_image(browser),
		"facts": mars_facts(),
		"last_modified": dt.datetime.now(),
		"hemispheres": mars_hemispheres()
	}

	browser.quit()
	return data



def mars_news(browser):


	# Visit the mars nasa news site
	url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
	browser.visit(url)

	# Optional delay for loading the page
	browser.is_element_present_by_css('div.list_text', wait_time=1)


	# Convert the browser html to a soup object and then quit the browser
	html = browser.html
	news_soup = BeautifulSoup(html, 'html.parser')

	try:

		slide_elem = news_soup.select_one('div.list_text')
		slide_elem.find('div', class_='content_title')

		# Use the parent element to find the first `a` tag and save it as `news_title`
		news_title = slide_elem.find('div', class_='content_title').get_text()
		# Use the parent elemend to find the paragraph text
		news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

	except:
		return None, None

	
	return news_title , news_p




def featured_image(browser):

	# ## JPL Space IMages Featured Image
	url = 'https://spaceimages-mars.com'
	browser.visit(url)

	# Find and click the full image button
	full_image_elem = browser.find_by_tag('button')[1]
	full_image_elem.click()

	# Parse the resulting html with soup
	html = browser.html
	img_soup = BeautifulSoup(html, 'html.parser')


	try:
		# find the relative image url
		img_url_rel = img_soup.find('img', class_='thumbimg').get('src')

	except AttributeError:
		return None

	# Use the base url to create an absolute url
	img_url = f'https://spaceimages-mars.com/{img_url_rel}'

	return img_url





def mars_facts():
	
	try:
		# Mars Facts
		df = pd.read_html('https://galaxyfacts-mars.com')[0]
	
	except BaseException:
		return None


	df.columns=['Description', 'Mars', 'Earth']
	df.set_index('Description', inplace=True)

	return df.to_html()

def mars_hemispheres():

	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=False)
	url = 'https://marshemispheres.com/'
	browser.visit(url)

	hemisphere_image_urls = []
	j=4
	for i in range(4):
		hemispheres = {}
		# Set up beautiful soup
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')

		# Get the titles
		title = soup.find_all('h3')[i]
		browser.find_by_tag('a')[j].click()
		
		# Reset beautiful soup to the browser after .click()
		html = browser.html
		soup = BeautifulSoup(html, 'html.parser')
		
		# Store the image_url as img_url
		img_url = soup.find_all('img', class_='wide-image')[0]['src']
		
		# Add title and image_url
		hemispheres['title'] = title.get_text()
		hemispheres['img_url'] = f'{url}{img_url}'
		hemisphere_image_urls.append(hemispheres)
		j+=2
		# Go back in the browser
		browser.back()
	
	browser.quit()
	return hemisphere_image_urls
	

if __name__ == "__main__":
	print(scrape_all())