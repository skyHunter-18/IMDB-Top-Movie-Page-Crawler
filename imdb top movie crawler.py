from os import write
import requests
from bs4 import BeautifulSoup
import time
import csv

res = requests.get('https://www.imdb.com/chart/top/')
soup = BeautifulSoup(res.text, 'html.parser')
count = 1
csv_data = [['Count', 'Name', 'Year', 'Rating',
             'Runtime', 'Description']]
link_set = soup.select('.titleColumn > a')
for links in link_set:
    rest = requests.get(f'https://www.imdb.com/{links.attrs["href"]}')
    soupy = BeautifulSoup(rest.text, 'html.parser')
    tags = []
    for i in (soupy.select('.TitleHeader__TitleText-sc-1wu6n3d-0')):
        movie_name = i.text
    for i in soupy.select(
            '.TitleBlockMetaData__StyledTextLink-sc-12ein40-1')[:-1]:
        year = i.text
    for r in soupy.select('.AggregateRatingButton__RatingScore-sc-1ll29m0-1'):
        rating = r.text
    for d in soupy.select('.GenresAndPlot__TextContainerBreakpointXL-cum89p-2'):
        desc = d.text
    for t in soupy.select('.GenresAndPlot__GenreChip-cum89p-3 > span'):
        tags.append(t.text)
    for run in soupy.select('.TitleBlockMetaData__MetaDataList-sc-12ein40-0 > li')[-1:]:
        runtime = run.text
    csv_data.append([count, movie_name, year, rating, runtime, desc])
    with open('Top 250 Movies List.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)
    print(f'Scrapped {count}')
    count += 1
    time.sleep(0.3)
file.close()
