# images_360
* A image spider on https://image.so.com/

# spiders/images.py
* 1. In spiders/images.py: 
    In start_request function, u can change the given keyword options of 'ch' of data query dict. 
* 2. In pipeline.py: 
    The project offers 3 methods saving the item crawled by images.py in pipeline.py, which includes MongoDB, Mysql and local storage. 
* 3. In settings.py:
    Besides, if u wanna to store the pics locally, u can uncomment the ITEMPIPELINE SETTINGS "'images_360.pipelines.ImagePipeline': 299,'" in settings.py and remember choose the save path by retype the attribute "IMAGES_STORE" in settings.py either.


# spiders/search_images.py
* 1. acheieve a free search way of crawl the pics on this site
* 2. similar structure with images.py, but ConnectionError occurs more, proxies need to be added in this spider middleware.

# Run instruction
## if your KEYWORD in optional list: [beauty, wallpaper, design#/, funny, news, art, car, photography, food, home, pet]
    * -> choose the way u want to save them(settings.py -> ItemPipeline)
    * -> change the KEYWORD in settings.py
    * -> just run "scrapy crawl images" command in terminal
## otherwise
    *  -> same with given keywords at the fisrt 2 steps 
    * -> run "scray crawl search_images" command in terminal
