#this scraper returns the ingredients and setps of all recipes under a certain category. it is not the final product.

import scrapy

class foodspider(scrapy.Spider):
    name = 'foodspider'
    
    start_urls = ["https://www.allrecipes.com/recipes/78/breakfast-and-brunch/?page=2"]
    #started from this page because it had a clear next button with new urls.
    #5000+ breakfast items is sufficient. 

    def parse(self, response):
        #recipez=response.css("div.component.card.card__category")
        recipez=response.css("div.tout__contentHeadline a")
        #oneRecipe=recipez.css("div.card__imageContainer a")
        #dishes=[]
        #for dish in [a.attrib["href"] for a in oneRecipe]:
        for dish in [a.attrib["href"] for a in recipez]:
            dish_url = response.urljoin(dish)
            yield scrapy.Request(dish_url, callback = self.parse_recipes)
        nextpage=response.css("div.category-page-list-related-nav-container a.category-page-list-related-nav-next-button").attrib["href"]
        if nextpage:
            url=nextpage
            yield scrapy.Request(url, callback = self.parse)


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
