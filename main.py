import requests
from bs4 import BeautifulSoup
import pandas as pd 

def get_html_code(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_code = response.text
            return html_code
        else:
            print(f'{response.status_code} Error')

    except Exception as e:
        print(e)
        return
    
if __name__ == "__main__":
    html_codes = get_html_code('https://github.com/topics')
    
    soup = BeautifulSoup(html_codes, 'lxml')

    topic_names = soup.find_all(
        'p', class_ = 'f3 lh-condensed mb-0 mt-1 Link--primary')
    topic_names = [topic.text.strip() for topic in topic_names]
    
    topic_des = soup.find_all('p', class_ = 'f5 color-fg-muted mb-0 mt-1')
    topic_des = [topic.text.strip() for topic in topic_des]
    
    base_link = 'https://github.com'
    topic_link_tags = soup.find_all(
        'div', class_ = 'py-4 border-bottom d-flex flex-justify-between')
    topic_links = [
        base_link + tags.find('a')['href'] for tags in topic_link_tags]

    topic_dict = {
        'topic name': topic_names,
        'topic descriptions': topic_des,
        'topic link': topic_links
    }

    df = pd.DataFrame(topic_dict)
    df.to_csv('github_topics.csv', index=False)

    
    for link in topic_links:
        topic_html = get_html_code(link)

        topic_soup = BeautifulSoup(topic_html, 'lxml')

        repo_dict = {
            'username': [],
            'user link': [],
            'repo name': [],
            'repo link': [],
            'star': []
            }

        repo_tags = topic_soup.find_all(
            'div',
            class_ = 'd-flex flex-justify-between flex-items-start flex-wrap gap-2 my-3')
        for repo in repo_tags:
            usr_name = repo.div.h3.find('a', class_ = 'Link').text.strip()
            repo_dict['username'].append(usr_name)

            usr_link = repo.div.h3.find('a', class_ = 'Link')['href']
            usr_link = base_link + usr_link
            repo_dict['user link'].append(usr_link)

            repo_name = repo.div.h3.find(
                'a', class_ = 'Link text-bold wb-break-word').text.strip()
            repo_dict['repo name'].append(repo_name)

            repo_link = repo.div.h3.find(
                'a', class_ = 'Link text-bold wb-break-word')['href']
            repo_link = base_link + repo_link
            repo_dict['repo link'].append(repo_link)

            repo_star = repo.find('span', id = 'repo-stars-counter-star').text.strip()
            repo_dict['star'].append(repo_star)


        topic_df = pd.DataFrame(repo_dict)
        filename = link.rsplit('/', 1)[-1]
        topic_df.to_csv(f'topic/{filename}.csv', index=False)



            


