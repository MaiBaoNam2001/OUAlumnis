from bs4 import BeautifulSoup


def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('img')
    image_urls = []

    for image_tag in image_tags:
        image_url = image_tag.get('src')
        if image_url:
            image_urls.append(image_url)

    return image_urls
