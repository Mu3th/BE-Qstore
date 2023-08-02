import psycopg2
from flask import Flask, Response, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

def connect():
    return psycopg2.connect(
                #host = "dpg-cj3trj5iuie55pnpabcg-a.oregon-postgres.render.com",
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
        categories = cur.fetchall()
        response = jsonify(categories)
        response.status_code = 200
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
    app.run(host = "192.168.1.113", port=8000)