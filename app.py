import psycopg2
from flask import Flask, Response, request, jsonify, send_file
from flask_cors import CORS, cross_origin
# from PIL import Image

app = Flask(__name__)
cors = CORS(app)

def connect():
    return psycopg2.connect(
                host = "dpg-cj3trj5iuie55pnpabcg-a.oregon-postgres.render.com",
                #host = "dpg-cj3trj5iuie55pnpabcg-a", 
                dbname = "qstore_7it7", 
                user = "qstore", 
                password = "QJDhQO5iVryRiBbkRV57O9Uf11uTAGue", 
                port = 5432)

##Categories
@app.route("/categories/add", methods = ['POST'])
def addCategory():
    try:
        # Get the name parameter from the request
        name = request.form.get('name')
        if name and request.method == 'POST':
            conn = connect()
            cur = conn.cursor()   
            # Check if an image file was uploaded
            if 'image' not in request.files:
                return 'No image file provided', 400
            image_file = request.files['image']
            # Check if the file has a filename
            if image_file.filename == '':
                return 'Empty filename', 400
            # Save the image to a desired location
            image_path = f'uploads/{image_file.filename}'
            image_file.save(image_path)    
            cur.execute("insert into categories ( name, image) values (%s, %s);", (name,image_path,))
            response = jsonify('Category added successfully')
            response.status_code = 201
            return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/categories/delete/<int:id>", methods = ['DELETE'])
def delCategory(id):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("delete from categories where id = %s", (id,))
        response = jsonify("Category deleted successfully")
        response.status_code = 200
        return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/categories/update/<int:id>", methods = ['PUT'])
def updateCategory(id):
    try:
        name = request.form.get('name')
        if name and request.method == 'PUT':
            conn = connect()
            cur = conn.cursor()   
            # Check if an image file was uploaded
            if 'image' not in request.files:
                return 'No image file provided', 400
            image_file = request.files['image']
            # Check if the file has a filename
            if image_file.filename == '':
                return 'Empty filename', 400
            # Save the image to a desired location
            image_path = f'uploads/{image_file.filename}'
            image_file.save(image_path)  
            cur.execute("update categories set name = %s, image = %s where id = %s;", (name,image_path, id,))
            response = jsonify("Category updated successfully")
            response.status_code = 200
            return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/categories", methods = ['GET'])
def getCategories():
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("select * from categories")
        result = cur.fetchall()
        categories = []
        #print(categories)
        for item in result:
            path = "./" + item[2]
            category = {
                "id": item[0],
                "name": item[1],
                "image": path,
            }
            # print(category)
            categories.append(category)
        # print(categories)
        response = jsonify({"categories": categories})
        response.status_code = 200
        return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

##Products 
@app.route("/product/add", methods = ['POST'])
def addProduct():
    try:
        _json = request.json
        name = _json['name']
        price = _json['price']
        offer_price = _json['offer_price']
        description = _json['description']
        category_id = _json['category_id']
        amount = _json['amount']
        #image = _json['image']
        if name and price and category_id and amount and request.method == 'POST':
            conn = connect
            cur = conn.cursor()
            #write code here
            cur.execute("""insert into products 
                        ( name, price, offer_price, description, category_id, amount) 
                        values (%s, %s, %s, %s, %s, %s);""", 
                        (name, price, offer_price, description, category_id, amount,))
            response = jsonify('Product added successfully')
            response.status_code = 201
            return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/fuck", methods=["GET"])
def post_example():
    """GET in server"""
    return jsonify(message="POST request returned")

if __name__ == '__main__':
    app.run(host = "192.168.1.69", port=8000)