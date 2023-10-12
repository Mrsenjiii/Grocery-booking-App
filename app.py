import datetime  # for datetime
import os  # for file
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from User_model import *
from datetime import date, datetime
import json
import random
import csv
from graphs_utils import *

# from sqlalchemy import func
user_name = ' '

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# from user_function import *

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IIT_project.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.app_context().push()
db.init_app(app)
app.secret_key = 'your_secret_key_here'
# temp_name_pass = {}

product_sold = False


def authentication_login(username, password, user_list):
    for user in user_list:
        if username == user.user_name:  # username found
            if password == user.user_password:
                return True  # user found
            else:
                return None
    return False


def authentication_admin(admin_name, password, admin_list):
    for admin in admin_list:
        if admin.admin_username == admin_name and admin.admin_password == password:
            return True
    return False


def login_status():
    username = session.get('username')

    if username is not None:  # Check for presence of 'username'
        return True
    else:
        return False


def admin_login_status():
    admin_name = session.get('adminname')
    if admin_name:
        return True
    else:
        False


def Category_exists(cate):
    category = Category.query.filter_by(category_name=cate).all()
    if category == [] : 
        cat_to_add = Category(category_name=cate)
        db.session.add(cat_to_add)
        db.session.commit()
        return cat_to_add.category_id
    if category[0].category_name == cate : 
        return category[0].category_id


@app.route('/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user_login.html')
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        pass_word = request.form.get('user_password')
        amount = 1000

        if authentication_login(user_name, pass_word, Users.query.all()):
            
            session['username'] = user_name
            session['sold'] = False # this is for checking recent update in the sold_table
            username = session['username']
            return redirect(url_for('user'))
        return render_template('user_login_forgot_password.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('Admin_login.html')
    if request.method == 'POST':
        admin_name = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')

        if authentication_admin(admin_name, admin_password, Admin.query.all()):
            session['adminname'] = admin_name
            return redirect(url_for('admin_home_page'))

        return render_template('adminforgot.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('user_signup.html')
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('user_password')
        confirm_password = request.form.get('confirmed_user_password')
        # filetxt = open('data.txt', 'w')
        # filetxt.write(f"{name}")
        # filetxt.write(f"{password}")
        user = Users(user_name=name, user_password=password, user_wallet=1000)
        db.session.add(user)
        db.session.commit()
        return redirect('/')


# @app.route('/example<u_name>')
# def example(u_name):
#     return render_template('navbar.html')


# @app.route('/huu')
# def huu():
#     return redirect(url_for('example', u_name='rohit'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    if not login_status():
        return redirect(url_for('user_login'))

    username = session['username']
    # checking if the user is loged in
    if request.method == 'GET':
        all_category = Category.query.all()
        filter_categories = Category.query.all()

        product_list = Product.query.all()
        return render_template('new_user_rough.html', product_list=product_list,
                               categories_list=filter_categories,  user_name=username,
                               all_categories=all_category)

    if request.method == 'POST':
        # we have 4 post request.
        form_type = request.form.get('form_type')
        if form_type == 'search':
            item = request.form.get('search_string')
            # no search string given
            if item == '':
                return redirect(url_for('user'))

            # if search string given
            # filtering product app will match with apple

            product_list = Product.query.filter(func.lower(
                Product.product_name).ilike(f"{item}%")).all()

            all_category = Category.query.all()

            category_list = []
            all_category = Category.query.all()

            c_id = []
            for x in product_list:
                c_id.append(x.product_category_id)

            c_id = set(c_id)
            # return f"{c_id}"
            for x in c_id:
                category_list.append(Category.query.get(x))

            return render_template('new_user_rough.html', product_list=product_list, user_name=username,
                                   categories_list=category_list,  all_categories=all_category)

        elif form_type == 'filter_by_price':
            price = request.form.get('product_price')
            if not price:

                return redirect(url_for('user'))
            all_category = Category.query.all()
            product_list = Product.query.filter(
                Product.product_price <= price
            ).all()

            category_list = []

            c_id = []
            for x in product_list:
                c_id.append(x.product_category_id)

            c_id = set(c_id)
            for x in c_id:
                category_list.append(Category.query.get(x))

            return render_template('new_user_rough.html', product_list=product_list, user_name=username,
                                   categories_list=category_list,
                                   all_categories=all_category)

        elif form_type == 'filter_by_category':
            category = request.form.get('category')
           
            if category != 'All Category':
                category_list = Category.query.filter(
                    Category.category_name == category).all()
                product_list = Product.query.filter(                                 
                Product.product_category_id == category_list[0].category_id
                ).all()
            else : 
                
                category_list = Category.query.all()
                product_list = Product.query.all()
            all_category = Category.query.all()
            return render_template('new_user_rough.html', product_list=product_list, user_name=username,
                                   categories_list=category_list,
                                   all_categories=all_category)

        elif form_type == 'filter_by_date':
            start = request.form.get('product-mfg')
            end = request.form.get('product-exp')
            # return 'filter by date'
            all_category = Category.query.all()

            if start and end:
                start_date = datetime.strptime(start, '%Y-%m-%d')
                end_date = datetime.strptime(end, '%Y-%m-%d')

                # return f"{start_date} , {end_date}"
                product_list = Product.query.filter(
                    Product.product_mfg >= start_date,
                    Product.product_mfg <= end_date,
                ).all()
            elif start and not end:
                start_date = datetime.strptime(start, '%Y-%m-%d')

                # return f"{start_date} , {end_date}"
                product_list = Product.query.filter(

                    Product.product_mfg >= start_date,
                ).all()
            elif not start and end:
                end_date = datetime.strptime(end, '%Y-%m-%d')

                product_list = Product.query.filter(

                    Product.product_mfg <= end_date
                ).all()

            category_list = []

            c_id = []
            for x in product_list:
                c_id.append(x.product_category_id)

            c_id = set(c_id)
            for x in c_id:
                category_list.append(Category.query.get(x))

            return render_template('new_user_rough.html', product_list=product_list, user_name=username,
                                   categories_list=category_list,
                                   all_categories=all_category)


@app.route('/user/user_cart', methods=['GET', 'POST'])
def user_cart():

    """ In the post request we are adding product to the cart table we are checking if the same entry 
        already exists then we need to append other wise we will add a new entry to the cart table 
        if the same product with the same user id exist no need to create another entry.
    """

    if not login_status():
        return redirect(url_for('user_login'))

    username = session['username']
    if request.method == 'POST':
        # user_name = request.form.get('user_name')
        user_id = Users.query.filter_by(user_name=username).first().user_id
        product_id = request.form.get('product_id')
        # category_id = request.form.get('category_id')
        items = request.form.get('data_quantity')

        if int(items) < 1:  # checking if the no of item greater then 0
            return redirect(url_for('user'))
        results = db.session.query(Cart).filter(
            and_(Cart.product_id == product_id, Cart.cart_user_id == user_id)).first()

        # return f"done {results}"
        if results != None:  # checking if entry exists
            new_value = int(results.no_of_items) + int(items)  # appendin now
            results.no_of_items = new_value
            db.session.commit()
        else:
            cart = Cart(cart_user_id=user_id, product_id=product_id,
                        no_of_items=items)
            db.session.add(cart)
            db.session.commit()
        return redirect(url_for('user'))

    carts = Cart.query.all()
    # products=Product.query.all()

    user_id = Users.query.filter_by(user_name=username).first().user_id
    cart_product = {}
    for cart in carts : 
        if cart.cart_user_id == user_id:  # user_id is 1 here will change
            p_name = Product.query.filter_by(
                product_id=cart.product_id).first().product_name
            p_price = Product.query.filter_by(
                product_id=cart.product_id).first().product_price
            p_details = Product.query.filter_by(
                product_id=cart.product_id).first().product_pack_details
            p_category_id = Product.query.filter_by(
                product_id=cart.product_id).first().product_category_id
            p_stock = Product.query.filter_by(
                product_id=cart.product_id).first().product_stock
            qty = cart.no_of_items
        #    format product_name:[total price , quantity , details , cart id , product price , category_id , cart_product_id]
            cart_product[p_name] = [
                int(p_price)*int(qty), qty, p_details, cart.cart_id, p_price, p_category_id, p_stock, cart.product_id]

    return render_template('user_cart.html', user_name=username, user_cart=cart_product)
    # return f"{cart_product.keys()}"


# user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if not login_status():
        return redirect(url_for('user_login'))

    session.pop('username')
    return redirect(url_for('user_login'))


@app.route('/logout_admin', methods=['GET', 'POST'])
def logout_admin():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    session.pop('adminname')
    return redirect(url_for('admin_login'))


@app.route('/remove_buy', methods=['GET', 'POST'])
def remove_buy():
    if not login_status():
        return redirect(url_for('user_login'))
    
    if request.method == "POST":
        cart_id = request.form.get('cart_id')
        user_name = request.form.get('user_name')

        decision = request.form.get('decision')
        cart = Cart.query.filter_by(cart_id=cart_id).first()
        if decision == 'remove':
            db.session.delete(cart)
            #  here i am deleting the a cart item

        else:  # here i am buying item also delte from here and append to sold we
            # also decremting the stock after buying

            product_price = request.form.get('product_price')
            product_name = request.form.get('product_name')
            product_qty = request.form.get('product_quantity')
            category_id = request.form.get('category_id')
            product_id = request.form.get('product_id')

            product_to_edit = Product.query.get(
                product_id)  # product to make change
           

            stock = int(product_to_edit.product_stock)
  
            if int(product_qty) <= int(stock):
                 
                # return "we can buy"
                new_stock = int(stock) - int(product_qty)
                product_to_edit.product_stock = new_stock

                category_name = Category.query.get(category_id).category_name

                today_date = date.today()
                cart_ = cart.no_of_items

                solditem = Sold_Product(product_name=product_name, sold_date=today_date,
                                        product_price=product_price, product_category=category_name, sold_items=product_qty)
                db.session.add(solditem)
                db.session.commit()
                db.session.delete(cart)  # deleting cart here also
                session['sold'] = True

              # we just made some change in the Sold_product table.
                # return f"price {price}  name : {name}  qty : {qty} category_id  {category_id} date {today_date}"
                # return f"{cart_id}  , {decision} no of items {cart.no_of_items} after decrement {updated_items}"
            else:
                if stock > 0 : 
                    return f"<h1>You can only buy {stock} no of items </h1>"
                else :
                    return f" <h1>Currently Not available </h1>"
        db.session.commit()

        return redirect(url_for('user_cart'))


@app.route('/incri_decri', methods=['GET', 'POST'])
def incre():
    if not login_status():
        return redirect(url_for('user_login'))
    if request.method == "POST":
        cart_id = request.form.get('cart_id')
        decision = request.form.get('decision')
        user_name = request.form.get('user_name')
        # return f"{user_name}"
        cart = Cart.query.filter_by(cart_id=cart_id).first()
        if decision == 'incri':
            updated_items = int(cart.no_of_items) + 1
            cart.no_of_items = updated_items
            # return f"{cart_id}  , {decision} no of items {cart.no_of_items} after increment {updated_items}"

        else:
            if cart.no_of_items != '1':
                updated_items = int(cart.no_of_items) - 1
                cart.no_of_items = updated_items
            # return f"{cart_id}  , {decision} no of items {cart.no_of_items} after decrement {updated_items}"
        db.session.commit()
        return redirect(url_for('user_cart'))


@app.route('/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == 'GET':
     
        admin_all_catogory = Category.query.all()
    
        return render_template('Adminhomepage.html', categories_list=admin_all_catogory)
        # return 'admin home page' + admin_name

    if request.method == 'POST':
        cate_name = request.form.get('search_string')
        results = Category.query.filter(func.lower(
            Category.category_name).like(f"{cate_name}%")).all()
        # product_list = [x.product_name for x in results]
        return render_template('Adminhomepage.html',
                               #    admin_name=admin_name,
                               categories_list=results)


@app.route('/admin_home_page/add_product', methods=['GET', 'POST'])
def add_product():
    if not admin_login_status():
        return redirect(url_for('admin_login'))

    if request.method == "POST":
        product_name = request.form.get('product-name')
        product_desc = request.form.get('product-description')
        product_price = request.form.get('product-price')
        category_name = request.form.get('category-name')
        product_detail = request.form.get('product-detail')
        product_stock = request.form.get('product-stock')
        mfg_date = request.form.get('product-mfg')

        exp_date = request.form.get('product-exp')

        # if categoy exist give id if not create and give id

        if not (product_name and product_desc and product_price and category_name and product_detail and product_stock and mfg_date and exp_date):
            return redirect(url_for('add_product', error="occured"))

        mfg_date = datetime.strptime(mfg_date, '%Y-%m-%d').date()
        exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
        foreign_key_to_cateogry = Category_exists(category_name)

        if 'img' in request.files:
            # return 'image uploaded' + f"{a}"
            file = request.files['img']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_to_write = open('test.txt', 'w')
            file_to_write.write(filename)
            product_temp = Product(product_name=product_name, product_desc=product_desc, product_price=product_price,
                                   product_pack_details=product_detail, product_stock=product_stock,
                                   product_category_id=foreign_key_to_cateogry, product_mfg=mfg_date, product_exp=exp_date, img_file=filename)
            db.session.add(product_temp)
            db.session.commit()
            # return 'image  found'
        else:
            file = request.files['img']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_to_write = open('test.txt', 'w')
            file_to_write.write(filename)
            product_temp = Product(product_name=product_name, product_desc=product_desc, product_price=product_price,
                                   product_pack_details=product_detail, product_stock=product_stock, product_exp=exp_date,
                                   product_mfg=mfg_date, product_category_id=foreign_key_to_cateogry)
            
            db.session.add(product_temp)
            db.session.commit()

            return 'image not found'
        return redirect(url_for('admin_product_list', error="not-occured"))


    # return 'post working fine '
    # return (product_name, product_detail, product_desc, product_price, product_desc, product_stock, mfg_date, exp_date)
    all_category = Category.query.all()
    param = request.args.get('error')
    if param:
        # return f"some thing has occured{param}"
        return render_template('add_product.html', all_category=all_category, error=param)

    return render_template('add_product.html', all_category=all_category)


@app.route('/admin_home_page/admin_product_list', methods=['GET', 'POST'])
def admin_product_list():
    if not admin_login_status():
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        item = request.form.get('search_string')
        product_list = Product.query.filter(func.lower(
            Product.product_name).like(f"{item}%")).all()

        return render_template('admin_product_list.html', product_list=product_list)
    product_list = Product.query.all()
    return render_template('admin_product_list.html', product_list=product_list)


@app.route('/admin_home_page/add_category', methods=['GET', 'POST'])
def add_category():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == 'GET':
        param = request.args.get('error')
        if param:
            return render_template('Add_category.html', error=param)
        return render_template('Add_category.html')
    if request.method == 'POST':
        cate = request.form.get("category")
        if not cate:
            return redirect(url_for('add_category', error='occured'))
        # file.save('static/' + file.filename)
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_to_write = open('image.txt', 'w')
            file_to_write.write(filename)
            cat_eg = Category(category_name=cate, img_file=filename)
            db.session.add(cat_eg)
            db.session.commit()
        else:
            cat_eg = Category(category_name=cate)
            db.session.add(cat_eg)
            db.session.commit()

        return redirect(url_for('admin_home_page'))


@app.route('/admin_home_page/edit_category', methods=['GET', 'POST'])
def edit_category():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == 'GET':
        return render_template('edit_categories.html')
    if request.method == 'POST':
        cate_name = request.form.get("category")
        cate_id = request.form.get("category_id")
        cate_to_change = Category.query.get(cate_id)
        file = request.files['img']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_to_write = open('image.txt', 'w')
            file_to_write.write(filename)
            cate_to_change.category_name = cate_name
            cate_to_change.img_file = filename
            db.session.commit()
        else:
            # return 'in the else'

            cate_to_change.category_name = cate_name
            db.session.commit()
    # Handle the case when 'img' key is not present

        return redirect(url_for('admin_home_page'))


@app.route('/remove_category', methods=['GET', 'POST'])
def remove_category():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == "POST":
        category_id = request.form.get('category_id')  # geting the category_id
        # return f"{category_id}"
        products = Product.query.filter_by(
            product_category_id=category_id).all()  # product belongs to the cateogory to be deleted
        category = Category.query.get(
            category_id)   # cateogry to be deleted

        for x in products:
            db.session.delete(x)
        db.session.delete(category)
        db.session.commit()

    return redirect(url_for('admin_home_page'))


@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    """
        we are deleting carts in which our deleting product is there .

    """
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == "POST":
        product_id = request.form.get('product_id')  # geting the product_id

        product = Product.query.get(
            product_id)   # product to be deleted
        Cart_to_delete = Cart.query.filter(
            Cart.product_id == product_id).all()  # carts to delte
        for cart in Cart_to_delete:
            db.session.delete(cart)

        db.session.delete(product)
        db.session.commit()

        return redirect(url_for('admin_product_list'))


@app.route('/admin_home_page/admin_product_list/edit_product', methods=['GET', 'POST'])
def edit_product():
    if not admin_login_status():
        return redirect(url_for('admin_login'))
    if request.method == 'GET':
        p_id = request.args.get('product_id')
        # return f": {p_id}"
        return render_template('edit_product.html', product_id=p_id)
    if request.method == "POST":
        product_id = request.form.get('product_id')

        product_to_edit = Product.query.get(product_id)
        name = product_to_edit.product_name

        product_name = request.form.get('product-name')
        product_desc = request.form.get('product-description')
        product_price = request.form.get('product-price')
        category_name = request.form.get('category-name')
        product_detail = request.form.get('product-detail')
        product_stock = request.form.get('product-stock')
        mfg_date = request.form.get('product-mfg')

        exp_date = request.form.get('product-exp')

        # if categoy exist give id if not create and give id

        if product_name != '':
            product_to_edit.product_name = product_name
            db.session.commit()

        if product_desc != '':
            product_to_edit.product_desc = product_desc
            db.session.commit()

        if product_price != '':
            product_to_edit.product_price = product_price
            db.session.commit()

        if product_detail != '':
            product_to_edit.product_detail = product_detail
            db.session.commit()

        if product_stock != '':
            product_to_edit.product_stock = product_stock
            db.session.commit()

        if mfg_date != '':
            mfg_date = datetime.strptime(mfg_date, '%Y-%m-%d').date()
            product_to_edit.mfg_date = mfg_date
            db.session.commit()

        if exp_date != '':
            exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
            product_to_edit.exp_date = exp_date
            db.session.commit()

        # foreign_key_to_cateogry = Category_exists(category_name)
        file = request.files['img']
        if file:
            # return 'image uploaded' + f"{a}"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            product_to_edit.img_file = filename
            db.session.commit()
            # return 'image  found'
        return redirect(url_for('admin_product_list'))



@app.route('/admin_home_page/admin_product_list/analytics', methods=['GET', 'POST'])
def analytics():

    if not admin_login_status(): # checking for loging.
        return redirect(url_for('admin_login'))

    
    sold_table = Sold_Product.query.all()
    category_name = list({
        x.product_category for x in Sold_Product.query.all()})
    
    # if not session['sold'] : 
    #     return render_template('Analytics.html', category_name=category_name)


    a = set_frame(sold_table)
    runner()
    session['sold'] = False  # making false so that we don't have to load images again.
  
    return render_template('Analytics.html', category_name=category_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)