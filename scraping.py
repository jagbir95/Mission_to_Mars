# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path={'executable_path':ChromeDriverManager().install()}
    browser=Browser('chrome',**executable_path,headless=False)
    news_title,news_p=mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":hemisphere_data(browser)
    
    }
    #stop webdrivre and return data
    browser.quit()
    return data
def mars_news(browser):
    # visit the mars nasa news site
    url='https://redplanetscience.com'
    browser.visit(url)
    #optional delay for loading the page
    browser.is_element_present_by_css('div.list_text',wait_time=1)

    html=browser.html
    new_soup=soup(html,'html.parser')
    try:
        slide_elem=new_soup.select_one('div.list_text')

        slide_elem.find('div',class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        news_p=slide_elem.find('div',class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title,news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # find and click the full image button
    full_image_elem=browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    


    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

def hemisphere_data(browser):
    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    try:
        for i in range(0,4):
            hemisphere={}
            image=browser.find_by_tag('h3')[i]
            image.click()
            html=browser.html
            hemi_soup=soup(html,"html.parser")
            
            #find image jpg url
            img_link=hemi_soup.find('div',class_='downloads')
            link=img_link.find('a').get('href')
            img_url=f'https://marshemispheres.com/{link}'
            
            #insert image url to dictionary
            hemisphere['img_url']=img_url
            #find the title of the image
            title=hemi_soup.find('h2',class_='title').text
            #insert title into dictionary
            hemisphere['title']=title
            #append to list
            hemisphere_image_urls.append(hemisphere)
            
            browser.back()
        
    except AttributeError:
        return None, None
    return hemisphere_image_urls
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
