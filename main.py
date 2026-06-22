#this file contains API logic for E-commerce Backend Systems
#these are used to create all the tables in the database
from database import Base,engine,SessionLocal
#import the session
from sqlalchemy.orm import Session
#import models for perfroming operations on models
import models
#importing required Fastapi stuff
from fastapi import FastAPI,Depends,HTTPException,Path
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
oauth2scheme=OAuth2PasswordBearer(tokenUrl='login')
#import the passlib for hashing the password and verifying them
from passlib.context import CryptContext
pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
#importing jose for security
from jose import JWTError,jwt
import os
from datetime import datetime,timedelta
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')
#for pydantic 
from pydantic import BaseModel
#creating an app for fastapi
app=FastAPI()
#create all tables
Base.metadata.create_all(engine)
#--create token---
def create_token(data:dict):
     to_encode=data.copy()
     expire=datetime.utcnow()+timedelta(minutes=30)
     to_encode.update({'exp':expire})
     return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
#---creating a function for token validation-----
def verify_token(token:str):
    try:
        return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401,detail='Invalid Token or Token Expired')
#----Pydantic for register for user-------
class UserRegistration(BaseModel):
    name:str
    email:str
    password:str
#-----pydantic for adding product-------
class addProduct(BaseModel):
    name:str
    description:str
    price:float
    stock_quantity:int
#-----Pydantic for Add to cart ------
class addCart(BaseModel):
    product_id:int
    quantity:int
def get_db():
    db=SessionLocal()#using database locally
    try:
        yield db #giving db to API
    finally:
        db.close()#closing db 
#--password hashing
def hashpassword(password):
     return pwd_context.hash(password)
#---verify password
def verifyPassword(password,hashpassword):
    return pwd_context.verify(password,hashpassword)
#welcome page
@app.get('/',tags=['Welcome'])
def home():
    return 'Welcome to E-Commerce Backend System'
#-------1.Register User--------------
@app.post('/register',tags=['Register'])
def register(add:UserRegistration,db:Session=Depends(get_db)):
        user=models.User(name=add.name,email=add.email,password=hashpassword(add.password))
        #let's add user to session
        db.add(user)
        #commiting to database
        db.commit()
        db.refresh(user)
        return{
             'message':'user created successfully',
             'user_id':user.id
        }
#------2.login User----------
@app.post('/login',tags=['Login User'])
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not verifyPassword(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user.name
    }
#to get current user
def get_current_user(token:str=Depends(oauth2scheme)):
    payload=verify_token(token)
    return int(payload.get('sub'))
#profile API
@app.get('/profile',tags=['Get Profile'])
def get_profile(user=Depends(get_current_user),db:Session=Depends(get_db)):
    userdetails=db.query(models.User).filter(models.User.id==user).first()
    if userdetails:
        return{
        'id':userdetails.id,
        'name':userdetails.name,
        'email':userdetails.email
                }
    raise HTTPException(status_code=404,detail='user not found')
#------3.Add Product ------------
@app.post('/product',tags=['Add Product'])
def add_product(add:addProduct,db:Session=Depends(get_db)):
    item=models.Item(name=add.name,description=add.description,price=add.price,stock_quantity=add.stock_quantity)
    #add to session
    db.add(item)
    #commit to database
    db.commit()
    return{
        'message':'Product Added Successfully',
        "product_id":item.id
    }
#------4.Get all Products-----------
@app.get('/Products',tags=['Get all Products'])
def getallProducts(db:Session=Depends(get_db)):
    items=db.query(models.Item).all()
    if not items:
        raise HTTPException(status_code=404,detail='Items not Found')
    return{
        'Products':items
    }
#------5.Get by Product ID--------
@app.get('/product/{id}',tags=['Get By Product ID'])
def get_by_id(id:int,db:Session=Depends(get_db)):
    item=db.query(models.Item).filter(models.Item.id==id).first()
    if not item:
        raise HTTPException(status_code=404,detail='Item Not Found')
    return{
        'id':item.id,
        'name':item.name,
        'description':item.description,
        'price':item.price,
        'stock_quantity':item.stock_quantity
    }
#-----------6.Add to Cart---------------
@app.post('/cart',tags=['Add To Cart'])
def add_cart(add:addCart,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    # check product exists
    product = db.query(models.Item).filter(models.Item.id == add.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # check already in cart
    existing = db.query(models.Cart).filter(
        models.Cart.user_id == current_user,
        models.Cart.product_id == add.product_id
    ).first()
    if existing:
        existing.quantity += add.quantity
    else:
        cart = models.Cart(
            user_id=current_user,
            product_id=add.product_id,
            quantity=add.quantity
        )
        db.add(cart)
    db.commit()
    return {"message": "Item added to cart"}

#---------7.View Cart---------------
@app.get('/cart',tags=['View cart'])
def viewCart(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    cart_item=db.query(models.Cart).filter(
        models.Cart.user_id == current_user
    ).all()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart is empty")
    total=sum(Citem.quantity*Citem.item.price for Citem in cart_item)
    
    return {
    "cart_items":
                [
                        {
                            "product_id": item.product_id,
                            "name": item.item.name,
                            "quantity": item.quantity,
                            "price": item.item.price
                        }
                        for item in cart_item
                ],
    "total": total
        }

#----------8.Remove from cart------------
@app.delete('/cart/remove/{id}',tags=['Remove from Cart'])
def remove_cart(id:int=Path(description='Enter Product ID to delete'),current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    product=db.query(models.Cart).filter(models.Cart.user_id == current_user,models.Cart.product_id==id).first()
    if not product:
        raise HTTPException(status_code=404,detail='Item Not Found in Cart')
    db.delete(product)
    db.commit()
    return{
        'message':'Item Removed from Cart'
    }
#-----------ORDER API's---------------------
#---------9.create order-----------
@app.post('/order/create',tags=['Create Order'])
def create_order(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    # get cart items
    cart_items = db.query(models.Cart).filter(
        models.Cart.user_id == current_user
    ).all()
    #if cart is empty
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")
    total_amount = 0
    try:
        # Step 1: validate stock & calculate total
        for item in cart_items:
            product = item.item

            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for {product.name}"
                )

            total_amount += item.quantity * product.price

        # Step 2: create order
        order = models.Order(
            user_id=current_user,
            total_amount=total_amount,
            status="Placed",
            created_at=datetime.utcnow()
        )
        db.add(order)
        db.flush()  

        # Step 3: create order items + reduce stock
        for item in cart_items:
            product = item.item

            # reduce stock
            product.stock_quantity -= item.quantity

            order_item = models.OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
            db.add(order_item)

        # Step 4: clear cart
        for item in cart_items:
            db.delete(item)

        db.commit()

        return {
            "message": "Order placed successfully",
            "order_id": order.id,
            "total_amount": total_amount
        }

    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Order failed")
#---------------10.View all orders of a user-------------------
@app.get('/orders/view',tags=['View All Orders'])
def View_all(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    orders=db.query(models.Order).filter(models.Order.user_id==current_user).all()
    if not orders:
        raise HTTPException(status_code=404,detail='Orders Not Found')
    return{
        'orders':orders
    }
#------------11.Order Details----------------------
@app.get('/order/details/{order_id}',tags=['Order Details'])
def order_details(order_id: int,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    orderDetails=db.query(models.Order).filter(models.Order.id == order_id,models.Order.user_id==current_user).first()
    if not orderDetails:
        raise HTTPException(status_code=404,detail='Order Not Found')
    items = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == orderDetails.id
    ).all()

    return {
        "order_id": orderDetails.id,
        "total_amount": orderDetails.total_amount,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price_at_purchase
            }
            for item in items
        ]
    }