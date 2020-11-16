from flask import Flask, request, render_template, Response,jsonify 
from flask import g, render_template, request, jsonify, make_response,session,redirect,url_for
from flask_cors import CORS
import requests
import face
from base64 import b64decode
import sqlite3 as sql

app = Flask(__name__)
CORS(app)
db = sql.connect("FaceId.db")
db.execute(
    "create table if not exists faceTable(email varchar(50), name varchar(50),image_file varchar(60))")
db.close()


@app.route('/')
def home():
    return render_template('test.html')

@app.route('/redirected')
def redirectMe():
    return render_template('redirected.html')

@app.route('/recogniser')
def recogniser():
    return render_template('recogniser.html')

@app.route('/testPostMethod', methods=["GET", "POST","OPTIONS"])
def testPostMethod():
    if request.method == 'POST':
        content = request.get_json()
        title = content['title']
        bar = content['bar']
        userId = content['userId']
        return jsonify({'title': title,'bar':bar,'userId':userId}) 
    return jsonify({'value':"failed"})        


@app.route('/store_image', methods=["GET", "POST"])
def process_image():
    print("method called")
    content = request.get_json()
    name=content['name']
    email=content['emailValue']
    image1=content['value1']
    image2=content['value2']
    image3=content['value3']
    image4=content['value4']
    image5=content['value5']
    image6=content['value6']
    image7=content['value7']
    image8=content['value8']
    image9=content['value9']
    image10=content['value10']
    # value = request.json.get()
    image_data1=base64_to_img(image1)
    image_data2=base64_to_img(image2)
    image_data3=base64_to_img(image3)
    image_data4=base64_to_img(image4)
    image_data5=base64_to_img(image5)
    image_data6=base64_to_img(image6)
    image_data7=base64_to_img(image7)
    image_data8=base64_to_img(image8)
    image_data9=base64_to_img(image9)
    image_data10=base64_to_img(image10)
    PATH="D:"
    img1=f"{PATH}\\temp_img1.jpg"
    img2=f"{PATH}\\temp_img2.jpg"
    img3=f"{PATH}\\temp_img3.jpg"
    img4=f"{PATH}\\temp_img4.jpg"
    img5=f"{PATH}\\temp_img5.jpg"
    img6=f"{PATH}\\temp_img6.jpg"
    img7=f"{PATH}\\temp_img7.jpg"
    img8=f"{PATH}\\temp_img8.jpg"
    img9=f"{PATH}\\temp_img9.jpg"
    img10=f"{PATH}\\temp_img10.jpg"
    try:
        with open(img1, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img1, "rb+") as f:
        f.write(image_data1)
    try:
        with open(img2, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img2, "rb+") as f:
        f.write(image_data2)
    try:
        with open(img3, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img3, "rb+") as f:
        f.write(image_data3)
    try:
        with open(img4, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img4, "rb+") as f:
        f.write(image_data4)
    try:
        with open(img5, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img5, "rb+") as f:
        f.write(image_data5)
    try:
        with open(img6, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img6, "rb+") as f:
        f.write(image_data6)
    try:
        with open(img7, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img7, "rb+") as f:
        f.write(image_data7)
    try:
        with open(img8, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img8, "rb+") as f:
        f.write(image_data8)
    try:
        with open(img9, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img9, "rb+") as f:
        f.write(image_data9)
    try:
        with open(img10, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img10, "rb+") as f:
        f.write(image_data10)
        

    if save_to_database(name, email, f"{PATH}\\temp_img1.jpg", f"{PATH}\\temp_img2.jpg", f"{PATH}\\temp_img3.jpg", f"{PATH}\\temp_img4.jpg", f"{PATH}\\temp_img5.jpg", f"{PATH}\\temp_img6.jpg", f"{PATH}\\temp_img7.jpg", f"{PATH}\\temp_img8.jpg", f"{PATH}\\temp_img9.jpg", f"{PATH}\\temp_img10.jpg"):
        print("Stored")
        # url="http:/b67d2a58.ngrok.io/user"
        # r=requests.post(
        #     url=url, json={'username': name, 'email': emailValues})
        # print(r.text)
        #return jsonify({'message':'Success'})
        # obj='{"message":"success"}'
        # return Response(obj, content_type="application/json")
        data = "success"
        return jsonify({'data': data}) 
    data = "failed"
    return jsonify({'data': data}) 
    #return Response("False", content_type="text/html")
    # if save_to_database(name, email, f"{PATH}\\temp_img.jpg"):
    #     print("Stored")
    #     url="http://localhost:4000/createUser"
    #     r=requests.post(url=url,data={'name':name,'emailValue':emailValues})
    #     print(r.text)
    #     return Response("True", content_type="application/json")
    # print("Not Stored")
    # return Response("False", content_type="application/json")

@app.route('/test', methods = ["GET", "POST"]) 
def homes(): 
    print("method called")
    content = request.get_json()
    name=content['name']
    email=content['emailValue']
    image1=content['value1']
    image2=content['value2']
    image3=content['value3']
    image4=content['value4']
    image5=content['value5']
    image6=content['value6']
    image7=content['value7']
    image8=content['value8']
    image9=content['value9']
    image10=content['value10']
    image_data1=base64_to_img(image1)
    image_data2=base64_to_img(image2)
    image_data3=base64_to_img(image3)
    image_data4=base64_to_img(image4)
    image_data5=base64_to_img(image5)
    image_data6=base64_to_img(image6)
    image_data7=base64_to_img(image7)
    image_data8=base64_to_img(image8)
    image_data9=base64_to_img(image9)
    image_data10=base64_to_img(image10)
    PATH="D:"
    img1=f"{PATH}\\temp_img1.jpg"
    img2=f"{PATH}\\temp_img2.jpg"
    img3=f"{PATH}\\temp_img3.jpg"
    img4=f"{PATH}\\temp_img4.jpg"
    img5=f"{PATH}\\temp_img5.jpg"
    img6=f"{PATH}\\temp_img6.jpg"
    img7=f"{PATH}\\temp_img7.jpg"
    img8=f"{PATH}\\temp_img8.jpg"
    img9=f"{PATH}\\temp_img9.jpg"
    img10=f"{PATH}\\temp_img10.jpg"
    try:
        with open(img1, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img1, "rb+") as f:
        f.write(image_data1)
    try:
        with open(img2, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img2, "rb+") as f:
        f.write(image_data2)
    try:
        with open(img3, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img3, "rb+") as f:
        f.write(image_data3)
    try:
        with open(img4, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img4, "rb+") as f:
        f.write(image_data4)
    try:
        with open(img5, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img5, "rb+") as f:
        f.write(image_data5)
    try:
        with open(img6, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img6, "rb+") as f:
        f.write(image_data6)
    try:
        with open(img7, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img7, "rb+") as f:
        f.write(image_data7)
    try:
        with open(img8, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img8, "rb+") as f:
        f.write(image_data8)
    try:
        with open(img9, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img9, "rb+") as f:
        f.write(image_data9)
    try:
        with open(img10, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img10, "rb+") as f:
        f.write(image_data10)

    #checking
    res1=recognise_people(img1)
    res2=recognise_people(img2)
    res3=recognise_people(img3)
    res4=recognise_people(img4)
    res5=recognise_people(img5)
    res6=recognise_people(img6)
    res7=recognise_people(img7)
    res8=recognise_people(img8)
    res9=recognise_people(img9)
    res10=recognise_people(img10)
    if res1:
        name, email=res1
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data})         
    elif res2:
        name, email=res2
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data})
    elif res3:
        name, email=res3
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res4:
        name, email=res4
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res5:
        name, email=res5
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res6:
        name, email=res6
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res7:
        name, email=res7
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res8:
        name, email=res8
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res9:
        name, email=res9
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data}) 
    elif res10:
        name, email=res10
        print(name)
        print(name, email)
        data = "user Exits"
        return jsonify({'status':data})   
    
    if save_to_database(name, email, f"{PATH}\\temp_img1.jpg", f"{PATH}\\temp_img2.jpg", f"{PATH}\\temp_img3.jpg", f"{PATH}\\temp_img4.jpg", f"{PATH}\\temp_img5.jpg", f"{PATH}\\temp_img6.jpg", f"{PATH}\\temp_img7.jpg", f"{PATH}\\temp_img8.jpg", f"{PATH}\\temp_img9.jpg", f"{PATH}\\temp_img10.jpg"):        
        print("datas stored")
        data = "success"
        return jsonify({'data': data})
    data = "failed"
    return jsonify({'data': data})        













def externalStoreMethod(name,email,image1,image2,image3,image4,image5): 
    print("method called")
    
    image_data1=base64_to_img(image1)
    image_data2=base64_to_img(image2)
    image_data3=base64_to_img(image3)
    image_data4=base64_to_img(image4)
    image_data5=base64_to_img(image5)
    image_data6=base64_to_img(image1)
    image_data7=base64_to_img(image2)
    image_data8=base64_to_img(image3)
    image_data9=base64_to_img(image4)
    image_data10=base64_to_img(image5)
    PATH="D:"
    img1=f"{PATH}\\temp_img1.jpg"
    img2=f"{PATH}\\temp_img2.jpg"
    img3=f"{PATH}\\temp_img3.jpg"
    img4=f"{PATH}\\temp_img4.jpg"
    img5=f"{PATH}\\temp_img5.jpg"
    img6=f"{PATH}\\temp_img6.jpg"
    img7=f"{PATH}\\temp_img7.jpg"
    img8=f"{PATH}\\temp_img8.jpg"
    img9=f"{PATH}\\temp_img9.jpg"
    img10=f"{PATH}\\temp_img10.jpg"
    try:
        with open(img1, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img1, "rb+") as f:
        f.write(image_data1)
    try:
        with open(img2, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img2, "rb+") as f:
        f.write(image_data2)
    try:
        with open(img3, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img3, "rb+") as f:
        f.write(image_data3)
    try:
        with open(img4, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img4, "rb+") as f:
        f.write(image_data4)
    try:
        with open(img5, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img5, "rb+") as f:
        f.write(image_data5)
    try:
        with open(img6, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img6, "rb+") as f:
        f.write(image_data6)
    try:
        with open(img7, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img7, "rb+") as f:
        f.write(image_data7)
    try:
        with open(img8, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img8, "rb+") as f:
        f.write(image_data8)
    try:
        with open(img9, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img9, "rb+") as f:
        f.write(image_data9)
    try:
        with open(img10, "x") as f:
            f.close()
    except FileExistsError:
        pass
    with open(img10, "rb+") as f:
        f.write(image_data10)

    #checking
    res1=recognise_people(img1)
    res2=recognise_people(img2)
    res3=recognise_people(img3)
    res4=recognise_people(img4)
    res5=recognise_people(img5)
    res6=recognise_people(img6)
    res7=recognise_people(img7)
    res8=recognise_people(img8)
    res9=recognise_people(img9)
    res10=recognise_people(img10)
    if res1:
        name, email=res1
        print(name)
        print(name, email)
        data = "user Exits"
        return False       
    elif res2:
        name, email=res2
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res3:
        name, email=res3
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res4:
        name, email=res4
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res5:
        name, email=res5
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res6:
        name, email=res6
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res7:
        name, email=res7
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res8:
        name, email=res8
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res9:
        name, email=res9
        print(name)
        print(name, email)
        data = "user Exits"
        return False
    elif res10:
        name, email=res10
        print(name)
        print(name, email)
        data = "user Exits"
        return False   
    
    if save_to_database(name, email, f"{PATH}\\temp_img1.jpg", f"{PATH}\\temp_img2.jpg", f"{PATH}\\temp_img3.jpg", f"{PATH}\\temp_img4.jpg", f"{PATH}\\temp_img5.jpg", f"{PATH}\\temp_img6.jpg", f"{PATH}\\temp_img7.jpg", f"{PATH}\\temp_img8.jpg", f"{PATH}\\temp_img9.jpg", f"{PATH}\\temp_img10.jpg"):        
        print("datas stored")
        data = "success"
        return True
    data = "failed"
    return False        









































@app.route('/recognise_image', methods=["POST", "GET","OPTIONS"])
def recognise_from_images():
    if  request.method == 'POST':
        print("in recognize method")
        content = request.get_json()
        image=content['encValue']
        data=base64_to_img(image)
        PATH="D:"
        img=f"{PATH}\\temp_img.jpg"
        try:
            with open(img, "x") as f:
                f.close()
        except FileExistsError:
            pass

        with open(img, "rb+") as f:
            f.write(data)

        res=recognise_people(img)
        user = []
        if res:
            
            name, email=res
            print(name)
            print(name, email)
            # url="http://c4c8bd9d.ngrok.io/userLogin"
            # r=requests.post(url=url, json={'name': name, 'emailValue': email})
            # print(r.text)
            data = "success"
            user = {
                    "name":name
                } 
            return redirect('/redirected')
            return jsonify({'status':data,'name': name,'email':email}) 
            #return Response(f"name:{name}, email:{email}", content_type="text/html")
        #return Response("False", content_type="text/html")
        data = "failed"
        
        return jsonify({'status': data}) 
       
    return render_template('redirected.html',user=user)




def externalRecogniseMethod(image):
        
        data=base64_to_img(image)
        PATH="D:"
        img=f"{PATH}\\temp_img.jpg"
        try:
            with open(img, "x") as f:
                f.close()
        except FileExistsError:
            pass

        with open(img, "rb+") as f:
            f.write(data)

        res=recognise_people(img)
        user = []
        if res:
            
            name, email=res
            print(name)
            print(name, email)
            # url="http://c4c8bd9d.ngrok.io/userLogin"
            # r=requests.post(url=url, json={'name': name, 'emailValue': email})
            # print(r.text)
            data = "success"
            user = {
                    "name":name, "email":email
                } 
            return user
            #return jsonify({'status':data,'name': name,'email':email}) 
            #return Response(f"name:{name}, email:{email}", content_type="text/html")
        #return Response("False", content_type="text/html")
        user = {
                    "name":"fail", "email":"fail"
                } 
        
        return user 
       
    

































def base64_to_img(bs4):
    i=bs4.index(",")
    bs4=bs4[i+1:]
    return b64decode(bs4)


def save_to_database(name, email, file1, file2, file3, file4, file5, file6, file7, file8, file9, file10):
    db=sql.connect("FaceId.db")
    i=0
    file1=face.detect_faces(file1)
    file2=face.detect_faces(file2)
    file3=face.detect_faces(file3)
    file4=face.detect_faces(file4)
    file5=face.detect_faces(file5)
    file6=face.detect_faces(file6)
    file7=face.detect_faces(file7)
    file8=face.detect_faces(file8)
    file9=face.detect_faces(file9)
    file10=face.detect_faces(file10)
    if file1:
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file1))
        db.commit()
        db.close()
        print("File 1 saved")
        i+=1
        
    if file2:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file2))
        db.commit()
        db.close()
        print("File 2 saved")
        i+=1
    if file3:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file3))
        db.commit()
        db.close()
        print("File 3 saved")
        i+=1
    if file4:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file4))
        db.commit()
        db.close()
        print("File 4 saved")
        i+=1
    if file5:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file5))
        db.commit()
        db.close()
        print("File 5 saved")
        i+=1
    if file6:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file6))
        db.commit()
        db.close()
        print("File 6 saved")
        i+=1
    if file7:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file7))
        db.commit()
        db.close()
        print("File 7 saved")
        i+=1
    if file8:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file8))
        db.commit()
        db.close()
        print("File 8 saved")
        i+=1
    if file9:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file9))
        db.commit()
        db.close()
        print("File 9 saved")
        i+=1
    if file10:
        db=sql.connect("FaceId.db")
        db.execute("insert into faceTable values(?, ?, ?)", (email, name, file10))
        db.commit()
        db.close()
        print("File 10 saved")
        i+=1
    if i>5:
        return True
    else:
        return False


def recognise_people(img):
    db=sql.connect("FaceId.db")
    file=face.recognise_face(img)
    if file:
        cur=db.cursor()
        cur.execute(
            "select name, email from faceTable where image_file = ?", (file, ))
        name, email=cur.fetchone()
        cur.close()
        return name, email
    return False


if __name__ == '__main__':
    app.run(debug=True)
    # base64_to_img(None)
