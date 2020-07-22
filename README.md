# images_360
A image spider on https://image.so.com/

# spiders/images.py
1. In spiders/images.py: 
    class ImageSpider's function start_request, u can change the given keyword options of 'ch' of data query dict. 
2. In pipeline.py: 
    The project offers 3 methods saving the item crawled by images.py in pipeline.py, which includes MongoDB, Mysql and local storage. 
2. In settings.py:
    Besides, if u wanna to store the pics locally, u can uncomment the ITEMPIPELINE SETTINGS "'images_360.pipelines.ImagePipeline': 299,'" in settings.py and remember choose the save path by retype the attribute "IMAGES_STORE" in settings.py either.


all_site crawler need to be done, so there is nothing to add more.
add later...
