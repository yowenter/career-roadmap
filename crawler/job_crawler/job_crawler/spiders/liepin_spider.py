# -*- coding: utf-8 -*-

import scrapy
import re
from bs4 import BeautifulSoup as Soup
from job_crawler.items import JobItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'

    custom_settings = {
        'base_url': "https://www.liepin.com/sh/zhaopin/",
        'keywords': [
            'Python',
            '后端工程师'
        ]
    }

    def start_requests(self):
        start_urls = [
            "{}?key={}".format(self.custom_settings['base_url'], k) for k in self.custom_settings['keywords']
            ]
        for url in start_urls:
            yield scrapy.Request(url, callback=lambda r: self.pagination_jobs(r, max_page=1))

    def pagination_jobs(self, response, max_page=None):
        soup = Soup(response.body)
        # for debug
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        job_list = soup.find('div', attrs={'class': 'search-result-box'}).ul.find_all('li')

        for job in job_list[:1]:
            job_detail_url = re.search('href="([^ ]+)"', str(job)).groups()[0]
            yield scrapy.Request(job_detail_url, callback=self.parse_job_detail)

        if max_page is None:
            pager_box = soup.find('div', attrs={'class': 'pager-box'})
            last_page = pager_box.find_all('a')[-2]
            last_page_href = last_page.attrs['href']
            last_page_num = re.search('\d+', last_page_href).group()
            max_page = int(last_page_num)

        if re.search('curPage=(\d+)', response.url):
            cur_page = int(re.search('curPage=(\d+)', response.url).groups()[0])
        else:
            cur_page = 1

        if cur_page < max_page:
            next_page_url = re.sub('curPage=\d+', '', response.url)
            if next_page_url.endswith('&'):
                next_page_url = next_page_url[:-1]

            yield scrapy.Request(next_page_url, callback=lambda r: self.pagination_jobs(r, max_page=max_page))

    def parse_job_detail(self, response):
        soup = Soup(response.body)

        from scrapy.shell import inspect_response
        inspect_response(response, self)

        require_degree, work_experience, required_skills, required_age = [r.text for r in
                                                                          soup.find('div', attrs={
                                                                              'class': 'job-qualifications'}).find_all(
                                                                              'span')]
        basic_info = soup.find('p', attrs={'class': 'basic-infor'}).text.strip().split(' ')

        position = basic_info[0]
        pub_date = basic_info[-1]

        yield JobItem(
            title=soup.find('div', attrs={'class': 'title-info'}).h1.text.strip(),
            salary=soup.find('p', attrs={'class': 'job-item-title'}).text.split('\n')[0],

            require_degree=require_degree,
            work_experience=work_experience,
            required_skills=required_skills,
            required_age=required_age,

            tags=','.join([r.text for r in soup.find_all('span', attrs={'class': 'tag'})]),

            job_description=soup.find('div', attrs={'class': 'content content-word'}).text,

            company_name=soup.find('div', attrs={'class': 'title-info'}).h3.text.strip(),
            company_description=soup.find('div', attrs={'class': 'job-item main-message noborder'}).text,

            position=position,
            pub_date=pub_date
        )
