import time
from splinter import Browser

#Create Browser object
b = Browser()

'''
#List of glype proxy sites to be visited
url = [
		"http://samstevenm.net/prox/",
		"http://www.docoja.com/blue/index.php"]

'''
#List of non-proxy websites
url = [
		"https://www.bbc.co.uk/",
		"https://whatismyipaddress.com/",
		"https://www.google.com/",
		"https://www.youtube.com/",
		"https://www.facebook.com/",
		"https://www.wikipedia.org/",
		"https://www.yahoo.com/",
		"https://www.reddit.com/",
		"https://www.amazon.com/",
		"https://www.instagram.com/",
		"https://www.linkedin.com/",
		"https://www.netflix.com/"
		]
		
for site in url:
	#Visit site using Browser object
	print('Visiting {0}'.format(site))
	b.visit(site)
	#time.sleep(2)

	'''
	#Find all textboxes and fill it
	b.find_by_id('input').fill('www.whatismyipaddress.com')
	time.sleep(1)
	
	#Find submit button and click it
	if b.is_element_present_by_css('input.button'):
		goButton = b.find_by_css('input.button')
		goButton.click()
	elif b.is_element_present_by_css('input.submitbutton'):
		goButton = b.find_by_css('input.submitbutton')
		goButton.click()
	time.sleep(2)

	#Deal with SSL warning page if it appears
	sslWarningPage = b.find_by_text('Warning!')
	if sslWarningPage is not None:
		print('Dealing with warnings...')
		continueButton = b.find_by_css('input')[1]
		continueButton.click()'''
	print('Done visiting {0}'.format(site))
		
b.quit
