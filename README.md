# B2C-shopping-website
B2C means Business to Customer, which is one of the E-commerce business model.

## Technology Stack
* Front-end: jQuery, HTML, CSS
* Back-end: Django
* Database: MySQL, Redis
* Task Queue (Asynchronous Processing): Celery
* Distributed File Storage System: FastDFS
* Search Framework and Engine: Haystack, Whoosh
* Web Server Configure: Nginx, uwsgi
* Develop Env: Pycharm, Linux

## Project Module
### User Module
* register
* login
* activate
* exit
* user profile 
* user orders
* address management

### Goods Module
* index
* goods detail
* goods list
* goods search

### Cart Module
* add goods to cart
* select all/ some goods in cart
* increase/decrease goods amount in cart 
* delete goods in cart

### Order Module
* order creation
* order payment
* order comment

## Database
### MySQL
<img width="979" alt="Screen Shot 2020-01-03 at 15 05 17" src="https://user-images.githubusercontent.com/43054004/71746425-ded98680-2e3a-11ea-80cb-e09620924fa6.png">

### Redis
* [list]user history views: history_user_id: [sku_id1,sku_id2, sku_id3]
* [hash]goods info in cart: cart_user_id: {'sku_id1': num, 'sku_id2': num, 'sku_id2': num,}
* session
* cache

## Project Deploy
<img width="539" alt="Screen Shot 2020-01-03 at 15 24 02" src="https://user-images.githubusercontent.com/43054004/71747223-177a5f80-2e3d-11ea-9d9e-7fd07234db27.png">
