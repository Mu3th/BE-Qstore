import psycopg2
from flask import Flask, Response, request, jsonify, send_file
from flask_cors import CORS, cross_origin
# from PIL import Image

app = Flask(__name__)
cors = CORS(app)

def connect():
    return psycopg2.connect(
                # host = "dpg-cj3trj5iuie55pnpabcg-a.oregon-postgres.render.com",
                host = "dpg-cj3trj5iuie55pnpabcg-a", 
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
        # print(result)
        for item in result:
            name = item[2].split('/')
            path = "https://qstore-sesb.onrender.com/image?name=" + name[-1]
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
        # Get the name parameter from the request
        name = request.form.get('name')
        price = request.form.get('price')
        offer_price = request.form.get('offer_price')
        quantity = request.form.get('quantity')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        if name and price and quantity and category_id and request.method == 'POST':
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
            # cur.execute("insert into categories ( name, image) values (%s, %s);", 
            #             (name,image_path,))
            cur.execute("""insert into products 
                        ( name, price, offer_price, quantity, category_id, description, image) 
                        values (%s, %s, %s, %s, %s, %s, %s);""", 
                        (name, price, offer_price, quantity, category_id, description, image_path,))
            response = jsonify('Product added successfully')
            response.status_code = 201
            return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/product/update/<int:id>", methods = ['PUT'])
def updateProduct(id):
    try:
        # Get the name parameter from the request
        name = request.form.get('name')
        price = request.form.get('price')
        offer_price = request.form.get('offer_price')
        quantity = request.form.get('quantity')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        if name and price and quantity and category_id and request.method == 'PUT':
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
            cur.execute("update products set name = %s, price = %s, offer_price = %s, quantity = %s, category_id = %s, description = %s, image = %s where id = %s;", (name, price, offer_price, quantity, category_id, description, image_path, id,))
            response = jsonify('Product updated successfully')
            response.status_code = 200
            return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/products/delete/<int:id>", methods = ['DELETE'])
def delProduct(id):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("delete from products where id = %s", (id,))
        response = jsonify("Product deleted successfully")
        response.status_code = 200
        return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/products/<int:id>", methods = ['GET'])
def getProducts(id):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("select * from products where category_id = %s", (id,))
        result = cur.fetchall()
        products = []
        # print(result)
        for item in result:
            name = item[7].split('/')
            path = "https://qstore-sesb.onrender.com/image?name=" + name[-1]
            product = {
                "id": item[0],
                "name": item[1],
                "price": item[2],
                "offer_price": item[3],
                "quantity": item[4],
                "category_id": item[5],
                "description": item[6],
                "image": path,
            }
            # print(category)
            products.append(product)
        # print(categories)
        response = jsonify({"products": products})
        response.status_code = 200
        return response
    except Exception as e :
        print(e)
    finally:
        conn.commit()
        cur.close()
        conn.close()

@app.route("/image", methods=["GET"])
def getImage():
    """GET in server"""
    # return jsonify(message="POST request returned")
    name = request.args.get('name', 'Anonymous')
    image_path = f'./uploads/{name}'
    image =  send_file(image_path, mimetype='image/jpeg')
    return image

@app.route("/fuck", methods=["GET"])
def post_example():
    """GET in server"""
    # return jsonify(message="POST request returned")
    image_path = "./uploads/123.jpg"
    image =  send_file(image_path, mimetype='image/jpeg')
    return image

if __name__ == '__main__':
    app.run(host = "192.168.1.107", port=8000)