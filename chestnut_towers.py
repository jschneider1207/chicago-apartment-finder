from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import urllib.parse

URL = 'https://chestnuttowerchicago.securecafe.com/onlineleasing/chestnut-tower-apartments/floorplans.aspx'

def url():
  return URL

def get_availabilities():
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  return ApartmentAvailabilities.parse(soup)

class HtmlParsable(ABC):
  @classmethod
  @abstractmethod
  def parse(html):
    pass

class ApartmentAvailabilities(HtmlParsable):
  def __init__(self, categories):
    self.categories: list[ApartmentCategory] = categories

  @classmethod
  def parse(cls, html):
    floor_plan_list = html.find(id='floorplanlist')
    categories = []
    for category_html in floor_plan_list.find_all('div', class_='accordion-group'):
      categories.append(ApartmentCategory.parse(category_html))
    return ApartmentAvailabilities(categories)

class ApartmentCategory(HtmlParsable):
  def __init__(self, name, floor_plans):
    self.name: str = name
    self.num_bedrooms: int = int(name[0])
    self.floor_plans: list[FloorPlan] = floor_plans
  
  def __str__(self):
    floor_plans = [f'\t• '+str(f) for f in self.floor_plans]
    lines = [f'{self.name}:'] + floor_plans
    return '\n'.join(lines)
  
  @classmethod
  def parse(cls, html):
    name = ApartmentCategory.__parse_name(html)
    floor_plans = ApartmentCategory.__parse_floor_plans(html)
    return ApartmentCategory(name, floor_plans)
  
  @classmethod
  def __parse_name(cls, html): 
    return  html.find('a', class_='accordion-toggle').text.strip()
  
  @classmethod
  def __parse_floor_plans(cls, html): 
    floor_plans = []
    floor_plan_htmls = html.find(
      'table', class_='table'
    ).find(
      'tbody'
    ).find_all(
      'tr', scope='row'
    )
    for floor_plan_html in floor_plan_htmls:
      floor_plans.append(FloorPlan.parse(floor_plan_html))
    return floor_plans


class FloorPlan(HtmlParsable):
  def __init__(self, layout, floor_plan, bed_bath, sq_ft, rent, availability):
    self.layout: str = layout
    self.floor_plan: str = floor_plan
    self.bed_bath: str = bed_bath
    self.sq_ft: int = sq_ft
    self.rent: str = rent
    self.availability: int = availability
  
  def __str__(self):
    return f'{self.floor_plan} ({self.bed_bath}): {self.sq_ft} sq ft, {self.rent} rent, {self.availability} available'
  
  
  @classmethod
  def parse(cls, html):
    layout = FloorPlan.__parse_layout(html)
    floor_plan = FloorPlan.__parse_floor_plan(html)
    bed_bath = FloorPlan.__parse_bed_baths(html)
    sq_ft = FloorPlan.__parse_sq_ft(html)
    rent = FloorPlan.__parse_rent(html)
    availability = FloorPlan.__parse_availability(html)    
    return FloorPlan(layout, floor_plan, bed_bath, sq_ft, rent, availability)
  
  @classmethod
  def __parse_layout(cls, html):
    col = html.find('td', class_='floorplan-img')
    img = col.find('img')['data-src']
    pre, sep, post = img.rpartition('/')
    post = urllib.parse.quote(post)
    return pre + sep + post
  
  @classmethod
  def __parse_floor_plan(cls, html):
    col = html.find('td', attrs={"data-label": "Floor Plan"})
    return col.span.next_sibling
  
  @classmethod
  def __parse_bed_baths(cls, html):
    col = html.find('td', attrs={"data-label": "Beds"})
    return col.span.next_sibling.strip()
  
  @classmethod
  def __parse_sq_ft(cls, html):
    col = html.find('td', attrs={"data-label": "SQ. FT."})
    return int(col.contents[0].replace(',',''))
  
  @classmethod
  def __parse_rent(cls, html):
    col = html.find('td', attrs={"data-label": "Rent"})
    low = col.span.next_sibling
    high = low.next_sibling.next_sibling
    return low + high
  
  @classmethod
  def __parse_availability(cls, html):
    col = html.find('td', attrs={"data-label": "Availability"})
    span_children = col.span.contents
    return int(span_children[0]) if len(span_children) > 0 else 0
