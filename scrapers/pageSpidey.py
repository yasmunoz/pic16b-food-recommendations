import scrapy


class foodspider(scrapy.Spider):
    name = "foodspider" 
    start_urls = ["https://www.allrecipes.com/recipe/220520/classic-hash-browns/"]  # our URL to work with

    def parse(self, response):
        title = response.css("h1.headline.heading-content.elementFont__display::text").get()
        ingredients= response.css("span.ingredients-item-name.elementFont__body::text").get()
        steps=response.css("div.section-body.elementFont__body--paragraphWithin.elementFont__body--linkWithin")
        recipe = "\n".join(steps.css("p::text").getall())

        yield { 
            "title": title,
            "ingredients": ingredients,
            "recipe": recipe,
        }
