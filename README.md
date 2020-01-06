# B2C-shopping-website
B2C means Business to Customer, which is one of the E-commerce business model.

This is a online shopping mall website, users could buy fruits, meat, seafood, eggs, produce and grocery here.

Here are the [screen shots](https://github.com/fangjingyan/B2C-shopping-website/blob/master/dailyfresh.md) of the website.

## Technology Stack
* Front-end: jQuery, HTML, CSS
* Back-end: Django
* Database: MySQL, Redis
* Task Queue (Asynchronous Processing): Celery
* Distributed File Storage System: FastDFS
* Search Framework and Engine: Haystack, Whoosh
* Web Server Configure: Nginx, uwsgi
* Develop Env: Pycharm, Linux

<img width="548" alt="Screen Shot 2020-01-04 at 21 02 09" src="https://user-images.githubusercontent.com/43054004/71774029-7cb17c00-2f35-11ea-9b9f-a86fdac62d6c.png">

* Tasks of Celery:

1. send activation emails, and use Redis as broker

2. re-generate homepage when models are modified

## Modules

### User Module
* register
* login
* activate
* exit
* user profile 
* user orders
* address management

### Goods Module
* display goods by category in homepage
* display goods detail
* display goods sorted by creation time, price and popularity
* new goods recommendations
* search goods by keywords

### Cart Module
* add goods to cart
* select all/some goods in cart
* change the number of goods in cart 
* delete goods in cart
* compute price of goods in cart

### Order Module

* create orders
* pay orders
* create comments for goods in completed orders

## Database

### MySQL

<img width="979" alt="Screen Shot 2020-01-03 at 15 05 17" src="https://user-images.githubusercontent.com/43054004/71746425-ded98680-2e3a-11ea-80cb-e09620924fa6.png">

* SKU

SKU is short for stock keeping unit. For example, Apple Iphone X black, 256G is a SKU. And each color corresponds to a different SKU code. This makes it easy for sellers to manage their products and send the right products to customers.

* SPU

SPU is short for standard product unit. For example, Apple Iphone X is a SPU.

* Description of tables

User table records users basic information and their permissions.

Address table records each user's mailing address, one user could have one or more mailing addresses.

GoodsSKU table records each SKU good basic information

GoodsSPU table records each SPU good detail, one SPU good could have one or more SKU goods.

GoodsImage table records each SKU good's images, one SKU good could have one or more images.

GoodsType table records goods categories, one category could have one or more SKU goods.

IndexGoodsBanner table records carousel goods displayed on the homepage.

IndexPromotions table records promotions displayed on the homepage. 

IndexTypeGoods table records SKU goods displayed on the homepage by category.

OrderInfo table records each user's order information, one user could place one or more orders.

OrderGoods table records each SKU good's information and comment of one order, one order could contain one or more SKU goods.



### Redis

* Browsing history 

Browsing history is the latest five sku_id of goods that are recently viewed by a user.

Each user's browsing history is stored as one list.

key: history_\[user_id\], e.g. `history_7`

value: `[sku_id1, sku_id2, sku_id3]`, the order is from the latest to the oldest

* Shopping cart

Shopping cart is the goods that are added to the cart by a user and represented by their sku_id and numbers

Each user's shopping cart is stored as one hash.

key: cart_\[user_id\], e.g. `cart_7`

value: `{'sku_id1': num, 'sku_id2': num, 'sku_id3': num}`, in the hash, sku_id is the key, and its corresponding number is the value

* Session

Session is recorded by Django, the configuration is in setting.py
