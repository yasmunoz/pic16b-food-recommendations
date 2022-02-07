#this scraper returns ingredients and recipes under a certain category. it is not the final product.

import scrapy

class foodspider(scrapy.Spider):
    name = 'foodspider'
    
    start_urls = ['https://www.allrecipes.com/recipes/78/breakfast-and-brunch/']
    #def parse_breakfast(self, response):
        #cast_url = response.urljoin("78/breakfast-and-brunch")
        #yield scrapy.Request(cast_url, callback = self.parse_bdishes)

    def parse(self, response):
        recipez=response.css("div.component.card.card__category")
        oneRecipe=recipez.css("div.card__imageContainer a")
        #dishes=[]
        for dish in [a.attrib["href"] for a in oneRecipe]:
            dish_url = response.urljoin(dish)
            yield scrapy.Request(dish_url, callback = self.parse_recipes)

    def parse_recipes(self, response):
        title = response.css("h1.headline.heading-content.elementFont__display::text").get()
        ingredients= response.css("span.ingredients-item-name.elementFont__body::text").getall()
        steps=response.css("div.section-body.elementFont__body--paragraphWithin.elementFont__body--linkWithin")
        recipe = "\n".join(steps.css("p::text").getall())
        yield{
            "title": title,
            "ingredients": ingredients,
            "recipe": recipe
        }
