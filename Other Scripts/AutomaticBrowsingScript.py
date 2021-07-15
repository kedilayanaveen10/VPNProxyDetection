""" 
    The program when run, detects the use of anonymizing services in a test dataset
    
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
