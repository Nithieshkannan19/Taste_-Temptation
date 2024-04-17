from flask import Flask, render_template, request,url_for,session,redirect
import MySQLdb
import MySQLdb.cursors
from flask_mysqldb import MySQL
import json
import pymysql
from datetime import datetime


app = Flask(__name__,static_url_path='/static', static_folder='static')

db = MySQLdb.connect("localhost","root","Jeni@3604","restaurant" )
cur = db.cursor()

app.secret_key = 'Jeni@3604'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/back")
def back():
    return render_template("front.html")

@app.route('/order')
def order():
	return render_template('order.html')

@app.route('/gobookingTable')
def gobookingTable():
	return render_template('bookingTable.html')

@app.route("/bookingTable",methods = ['POST', 'GET'])
def bookingTable():
    msg = ''
    try:
        r_name = (request.form['R_NAME'])
        r_date = (request.form['R_DATE'])
        mob_num = (request.form['MOB_NUM'])

        # Check if r_date is today or a future date
        r_date_obj = datetime.strptime(r_date, '%Y-%m-%d')
        if r_date_obj < datetime.today():
            raise ValueError("Invalid date")

        sql = """INSERT INTO BOOKINGTABLE (R_NAME,R_DATE,MOB_NUM) VALUES(%s,%s,%s)"""
        val = (r_name,r_date,mob_num,)
        cur.execute(sql,val)
        db.commit()
        msg = "Successfully reserved.."
    except ValueError:
        msg = "Please enter a valid date."
    except:
        msg = "Sorry.."

    return render_template('bookingTable.html',msg=msg)


@app.route("/admin",methods = ['POST', 'GET'])
def admin():
    return render_template("admin.html")

@app.route("/adminLogin",methods=['POST','GET'])
def adminLogin():
    try:
        msg = ''
        name = request.form['username']
        pwd = request.form['password']
        if name == 'admin' and pwd == 'admin@123':
            return render_template("admin1.html",msg=msg)
        else:
            return render_template("admin.html",msg="Invalid")
    except:
        return render_template("front.html")

@app.route("/admin1#hallbooking")
def hallbooking():
    cur.execute('SELECT * FROM BOOKINGTABLE')
    data = cur.fetchall()
    return render_template('admin1.html', data=data)

@app.route('/addsales', methods=['POST'])
def add_sales():
    date = request.form['date']
    oid = request.form['order_id']
    amount = request.form['amount']
    status = request.form['status']
    cur.execute('INSERT INTO ADMIN_SALES (TODAY_DATE,ORDER_NUM,AMOUNT,S_STATUS) VALUES (%s, %s,%s,%s)', (date,oid,amount,status))
    db.commit()
    return redirect(url_for('sales'))
    
@app.route('/admin1#sales')
def sales():
    cur.execute('SELECT * FROM ADMIN_SALES')
    data = cur.fetchall()
    return render_template('admin1.html', data1=data)

@app.route('/placeorder', methods=['POST'])
def place_order():
    cur.execute("SELECT MAX(order_id) FROM ORDERNEW")
    result = cur.fetchone()
    if result[0]:
        order_id = result[0] + 1
    else:
        order_id = 1

    order_items = request.json['order_items']
    total_amount = request.json['total_amount']

    for item in order_items:
        item_name = item['item']
        qty = item['quantity']
        price = getPrice(item_name)
        amount = float(qty) * price
        sql = "INSERT INTO ORDERNEW (ITEM_NAME, QTY, PRICE, ORDER_ID) VALUES (%s, %s, %s, %s)"
        val = (item_name, qty, price, order_id)
        cur.execute(sql, val)
        db.commit()
    return "Ordered"

def getPrice(item):
    switcher = {
        "Chicken Lollipop": 12,
        "Butter Chicken": 16,
        "Paneer Tikka": 9,
        "Chicken Soup": 8,
        "Corn Soup": 6,
        "Tomato Soup": 5.50,
        "Kothu Parotta": 4.50, 
        "Chilli Parota": 4,
        "Bun Parotta": 1,
        "Scrambled Egg": 0.75,
        "Half Boil": 1.25,
        "Egg Gravy": 0.75,
        "Masal Dosa": 1.50,
        "Ghee Roast": 2.50,
        "Paneer Dosa": 3,
        "Mutton Biriyani": 9,
        "Chicken Biriyani": 8,
        "Hyderabad Biriyani": 8.50,
        "Veg Noodles": 5.25,
        "Spl Noodles": 6,
        "Paneer Noodles": 6.50,
        "Mojito": 2.25,
        "Oreo Shake": 3,
        "Caramel Shake": 2.75
    }
    return switcher.get(item, 0)

@app.route('/addMenu', methods=['POST'])
def addMenu():
    print("add menu")
    itemname = request.form['itemName']
    itemamt = request.form['item_amt']
    cur.execute('INSERT INTO MENU (ITEM_NAME,AMOUNT) VALUES(%s,%s)',(itemname,itemamt))
    db.commit()
    return redirect(url_for('items'))

@app.route('/delMenu', methods=['POST'])
def delMenu():
    itemname = request.form['del_itemName']
    sql = "DELETE FROM MENU WHERE ITEM_NAME = %s"
    val = (itemname,)
    cur.execute(sql,val)
    db.commit()
    return redirect(url_for('items'))

@app.route('/chef')
def chef():
    cur.execute("SELECT ORDER_ID,ITEM_NAME,QTY FROM ORDERNEW ORDER BY ORDER_ID")
    orders = cur.fetchall()
    return render_template('chef.html', orders=orders)

@app.route("/admin1#items")
def items():
    cur.execute('SELECT * FROM MENU')
    data = cur.fetchall()
    return render_template('admin1.html', data2=data)

@app.route('/netsales', methods=['POST'])
def netsales():
    msg = ''
    date = request.form.get('date')
    cur.execute('SELECT SUM(AMOUNT) FROM ADMIN_SALES WHERE TODAY_DATE = %s', (date,))
    total_sales = cur.fetchone()[0]
    return render_template('admin1.html',msg="Total sales : $" + str(total_sales))

@app.route('/get_last_order_id')
def get_last_order_id():
  cur.execute('SELECT MAX(ORDER_ID) FROM ORDERNEW')
  last_order_id = cur.fetchone()[0]
  if last_order_id is None:
    last_order_id = 0
  return str(last_order_id)






'''
@app.route('/delete_item/<string:item>', methods=['DELETE'])
def delete_item(item):
    print("Delete")
    sql = "DELETE FROM ORDERNEW WHERE ITEM_NAME = %s"
    val = (item,)
    cur.execute(sql, val)
    db.commit()
    return "success"
'''

'''
# Route for adding items to the order table
@app.route('/additem', methods=['POST'])
def add_item():
    if request.method == 'POST':
        # Get the values from the form
        itemname = request.form['items']
        print(itemname)
        qty = request.form['qty']
        print(qty)
        price = get_price(itemname) # A function to get the price of the item from the database
        print(price)
        orderid = get_next_orderid() # A function to get the next order ID from the database
        print(orderid)
        cur.execute('INSERT INTO ORDER1 (ORDER_ID) VALUES(%s)',(orderid))
        db.commit()
        # Store the values in the database
        sql = "INSERT INTO ORDERNEW (ITEM_NAME,QTY,PRICE,ORDER_ID) VALUES (%s, %s, %s, %s)"
        val = (itemname,qty,price,orderid)
        cur.execute(sql, val)
        print("additem database")
        db.commit()

        # Return a success message
        return {"status": "success"}
'''
'''
# Route for placing the order
@app.route('/placeorder', methods=['POST'])
def placeorder():
    # get the order details from the form data
    orderid = request.form['orderid']
    items = request.form.getlist('item')
    qtys = request.form.getlist('qty')
    prices = request.form.getlist('price')
    totalamount = request.form['totalamount']
    
    # create a new order object
    order = Order(orderid=orderid, items=items, qtys=qtys, prices=prices, totalamount=totalamount)
    
    # save the order to the database
    db.session.add(order)
    db.session.commit()
    
    # return a success message
    return 'Order placed successfully!'
'''
'''
@app.route('/additem', methods=['POST'])
def add_item():
    oid = 101
    cur.execute('INSERT INTO ORDER1 (ORDER_ID) VALUES (%s)',(oid))
    print(oid)
    db.commit()
    item = request.form['item']
    qty = request.form['qty']
    price5 = request.form['price5']
    print(item)
    print(qty)
    print(price5)
    cur.execute('INSERT INTO  ORDERNEW(ITEM_NAME,QTY,PRICE,ORDER_ID) VALUES (%s, %s, %s, %s)', (item, qty, price5,oid))
    db.commit()
    oid = oid + 1
    return 'Success!'
'''

'''
@app.route('/waiter')
def waiter():
	return render_template('waiter.html')

@app.route("/waiterLogin",methods=['POST','GET'])
def waiterLogin():
    msg = ''
    name = request.form['username']
    pwd = request.form['password']
    if name == 'def' and pwd == '456':
        return render_template("order1.html",msg=msg)
    else:
        return render_template("waiter.html",msg="Invalid")
'''


if __name__ == '__main__':
   app.run(debug=True)