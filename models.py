#this file contains all the models that we use in the E-Commerce Backend System
from database import Base
#this is used to create columns in the table with integer,string,date,text,float as datatypes with foregin key constraint
from sqlalchemy import Column,Integer,String,Date,Text,ForeignKey,Float,DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

#----1.User Table-----
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)#this is id of the user and which is unique
    name=Column(String,nullable=False)#this is the name of the user which cannot be null
    email=Column(String,nullable=False,unique=True)#this is email of the user which cannot be null and it should be unique
    password=Column(String,nullable=False)#this is the password of the user which cannot be null
    cart = relationship("Cart", backref="user")
    orders = relationship("Order", backref="user")


#-----2.Product Table----------
class Item(Base):
    __tablename__='item'
    id=Column(Integer,primary_key=True)#this is id of the item and which is unique
    name=Column(String,nullable=False)#this is the name of the item which cannot be null
    description=Column(Text,nullable=True)#this is the additional  information of the product
    price=Column(Float,nullable=False)#this is the price of the product
    stock_quantity=Column(Integer,nullable=False)#this is about the stock of a product
    cart=relationship('Cart',back_populates='item')
    order_items = relationship("OrderItem", backref="item")


#---------3.cart table-----------------
class Cart(Base):
    __tablename__='cart'
    id=Column(Integer,primary_key=True)#this is the of the cart which is unique
    user_id=Column(Integer,ForeignKey('user.id'))#this is the id of the user which refers to id in user table
    product_id=Column(Integer,ForeignKey('item.id'))#this is the product id which refers to id in product table
    quantity=Column(Integer,nullable=False,default=1)#this is the quantity of the product that user want to order default value of a product is zero
    item=relationship('Item',back_populates='cart')


#------------4.Orders Table---------------
class Order(Base):
    __tablename__='order'
    id=Column(Integer,primary_key=True)#this is the order id which is unique
    user_id=Column(Integer,ForeignKey('user.id'))#this is the id of the user which refers to id in user table
    total_amount=Column(Float,nullable=False,default=0)#this is the total price of the order
    status=Column(String,nullable=False)#this is the status of the order 
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow)#this is the date of the order
    order_items = relationship("OrderItem", backref="order")


#-------5.Order Items Table-------------------
class OrderItem(Base):
    #Stores products inside an order
    __tablename__='order_item'
    id=Column(Integer,primary_key=True)#this is the orderItem id which is unique
    order_id=Column(Integer,ForeignKey('order.id'))#this is the id of the order which refers to id in order table
    product_id=Column(Integer,ForeignKey('item.id'))#this is the product id which refers to id in product table
    quantity=Column(Integer,nullable=False)#this is the quantity of the item 
    price_at_purchase=Column(Float,nullable=False)#this is the price  of the item