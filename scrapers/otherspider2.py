import scrapy

class foodspider(scrapy.Spider):
    name = 'foodspidery'
    #attach all the links to different cuisines here?

    start_urls = [
    "https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/?page=2",
    "https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/?page=2",
    "https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/?page=2",
    "https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/?page=2",
    "https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/?page=2",
    "https://www.allrecipes.com/recipes/235/world-cuisine/middle-eastern/?page=2",
    "https://www.allrecipes.com/recipes/17582/world-cuisine/african/north-african/?page=2",
    "https://www.allrecipes.com/recipes/17845/world-cuisine/african/east-african/?page=2",
    "https://www.allrecipes.com/recipes/15035/world-cuisine/african/south-african/?page=2",
    "https://www.allrecipes.com/recipes/731/world-cuisine/european/greek/?page=2",
    "https://www.allrecipes.com/recipes/721/world-cuisine/european/french/?page=2",
    "https://www.allrecipes.com/recipes/726/world-cuisine/european/spanish/?page=2",
    "https://www.allrecipes.com/recipes/722/world-cuisine/european/german/?page=2",
    "https://www.allrecipes.com/recipes/733/world-cuisine/canadian/?page=2",
    "https://www.allrecipes.com/recipes/721/world-cuisine/european/french/?page=2",
    "https://www.allrecipes.com/recipes/699/world-cuisine/asian/japanese/?page=2",
    "https://www.allrecipes.com/recipes/700/world-cuisine/asian/korean/?page=2",
    "https://www.allrecipes.com/recipes/16704/healthy-recipes/mediterranean-diet/?page=2"
    #purposely not including us recipes because there is too much    
    ]
    #started from this page because it had a clear next button with new urls.
    #5000+ breakfast items is sufficient. 

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_data, dont_filter=True)
    def parse_data(self, response):
        #recipez=response.css("div.component.card.card__category")
        recipez=response.css("div.tout__contentHeadline a")
        #oneRecipe=recipez.css("div.card__imageContainer a")
        #dishes=[]
        #for dish in [a.attrib["href"] for a in oneRecipe]:

        #categorytitle = response.css("h1.categoryPage__heading.elementFont__headline:text").get()
        #category = categorytitle.split()[1]

        for dish in [a.attrib["href"] for a in recipez]:
            dish_url = response.urljoin(dish)
            yield scrapy.Request(dish_url, callback = self.parse_recipes)
        nextpage=response.css("div.category-page-list-related-nav-container a.category-page-list-related-nav-next-button").attrib["href"]
        if nextpage:
            url=nextpage
            yield scrapy.Request(url, callback = self.parse_data)


    def parse_recipes(self, response):
        title = response.css("h1.headline.heading-content.elementFont__display::text").get()
        ingredients= response.css("span.ingredients-item-name.elementFont__body::text").getall()
        steps=response.css("div.section-body.elementFont__body--paragraphWithin.elementFont__body--linkWithin")
        recipe = "\n".join(steps.css("p::text").getall())

        categorytitle=response.css("li.breadcrumbs__item.breadcrumbs__item--last")
        category = categorytitle.css("span.breadcrumbs__title::text").get()

        yield{
            "title": title,
            "ingredients": ingredients,
            "recipe": recipe,
            "category": category
        }


        #getting the cuisine's category
        #returns "Mexican" etc