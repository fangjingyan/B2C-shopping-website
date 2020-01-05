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

## Modules

[website display](https://github.com/fangjingyan/B2C-shopping-website/blob/master/dailyfresh.md)

### User Module
* register
* login
* activate
* exit
* user profile 
* user orders
* address management

### Goods Module
* display goods by category in index
* display goods detail
* display goods list by default, price abd sales
* new goods recommend
* search goods by keywords

### Cart Module
* add goods to cart
* select all/ some goods in cart
* increase/decrease goods amount in cart 
* delete goods in cart
* compute price of goods in cart

### Order Module
* create orders
* pay orders
* comment goods in paid orders

## Database
### MySQL
<img width="979" alt="Screen Shot 2020-01-03 at 15 05 17" src="https://user-images.githubusercontent.com/43054004/71746425-ded98680-2e3a-11ea-80cb-e09620924fa6.png">

### Redis
* browsing history

type: list

each user has one record

history_user_id: [sku_id1,sku_id2, sku_id3]

* cart info

type: hash

each user has one record

cart_user_id: {'sku_id1': amount, 'sku_id2': amount, 'sku_id3': amount}

* session

## Project Deploy
<img width="548" alt="Screen Shot 2020-01-04 at 21 02 09" src="https://user-images.githubusercontent.com/43054004/71774029-7cb17c00-2f35-11ea-9b9f-a86fdac62d6c.png">

* cerely tasks:

1. send activation emails, and use Redis as broker

2. re-generate index.html when models are modified
