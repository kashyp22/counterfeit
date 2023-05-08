from flask import *
from DBConnection import Db


from web3 import Web3, HTTPProvider
blockchain_address = 'http://127.0.0.1:7545'
web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'C:\\Users\\kashy\\Contacts\\build\\contracts\\Crowdfunding.json'
deployed_contract_address = '0x6DfAd330F057c5235C003F374490376FB1F8384e'
deployed_contract_addressa = web3.eth.accounts[5]


# --------------------------admin
app = Flask(__name__)
app.secret_key="abc"

@app.route('/')
def login():
    return render_template('login_index.html')

@app.route('/login_post', methods=['POST'])
def login_post():
    username=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="SELECT * FROM `login`WHERE `user_name`='"+username+"' AND `password`='"+password+"' "
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['lid']
        if res['type']=='admin':
            return redirect('/admin_home')
        elif res['type']=='manufacture':
            return redirect('/man_home')

        else:
            return '''<script>alert("invalid");window.location='/'</script>'''
    return '''<script>alert("not found");window.location='/'</script>'''


@app.route('/admin_home')
def admin_home():
    return render_template('admin/admin index.html')


@app.route('/admin_view_manufacture')
def admin_view_manufacture():
    db = Db()
    qry ="SELECT * FROM `manufacture` WHERE `status` ='pending'"
    res = db.select(qry)
    return render_template('admin/approve manufacture.html',data=res)

@app.route('/admin_view_manufacture_search',methods=['post'])
def admin_view_manufacture_search():
    db = Db()
    name=request.form['textfield']
    qry ="SELECT * FROM `manufacture` WHERE `status` ='pending'AND name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template('admin/approve manufacture.html',data=res)

@app.route('/approve_manufacture/<id>')
def approve_manufacture(id):
    db = Db()
    qry ="UPDATE `manufacture` SET `status`='approved' WHERE `lid`='"+id+"'"
    res = db.update(qry)
    return redirect('/admin_view_manufacture')




@app.route('/reject_manufacture/<id>')
def reject_manufacture(id):
    db = Db()
    qry ="UPDATE `manufacture` SET `status`='rejected' WHERE `lid`='"+id+"'"
    res = db.update(qry)
    return redirect('/admin_view_manufacture')

@app.route('/admin_approved_manufacture')
def admin_approved_manufacture():
    db = Db()
    qry = "SELECT * FROM `manufacture` WHERE `status` ='approved'"
    res = db.select(qry)
    return render_template('admin/approved manufacture.html',data=res)

@app.route('/reject_approved_manufature/<id>')
def reject_approved_manufature(id):
    db = Db()
    qry = "UPDATE `manufacture` SET `status`='rejected' WHERE `lid`='"+str(id)+"'"
    res = db.update(qry)
    return '''<script>alert('Reject approved');window.location='/admin_approved_manufacture'</script>'''





@app.route('/admin_rejected_manufacture')
def admin_rejected_manufacture():
    db = Db()
    qry = "SELECT * FROM `manufacture` WHERE `status` ='rejected'"
    res = db.select(qry)
    return render_template('admin/rejected_manufacture.html',data=res)



@app.route('/view_users')
def view_users():
    db = Db()
    qry = "SELECT * FROM `user`"
    res = db.select(qry)
    return render_template('admin/view_users.html',data=res)

@app.route('/view_users_search_post',methods=['post'])
def view_users_search_post():
    db = Db()
    name=request.form['textfield']
    qry = "SELECT * FROM `user` WHERE name LIKE '%"+name+"%'"
    res = db.select(qry)
    return render_template('admin/view_users.html',data=res)




@app.route('/send_reply/<id>')
def send_reply(id):
    return render_template('admin/send reply.html',rid=id)

@app.route('/send_reply_post', methods=['POST'])
def send_reply_post():
    id=request.form['id']
    reply=request.form['textarea']
    qry="UPDATE complaint SET reply='"+reply+"',STATUS='replied' WHERE complaint_id='"+id+"'"
    db=Db()
    res=db.update(qry)

    return "k"

@app.route('/view_complaints')
def view_complaints ():
    db= Db()
    qry ="SELECT * FROM complaint JOIN USER ON user.lid=complaint.lid"
    res = db.select(qry)
    return render_template('admin/view complaints.html',data=res)
@app.route('/view_complaints_post',methods=['post'])
def view_complaints_search_post ():
    db= Db()
    ffrom = request.form['textfield']
    to = request.form['textfield2']
    qry ="SELECT * FROM complaint JOIN USER ON user.lid=complaint.lid WHERE date BETWEEN '"+ffrom+"'and'"+to+"'"
    res = db.select(qry)

    return render_template('admin/view complaints.html',data=res)


@app.route('/view_feedback')
def view_feedback ():
    db=Db()
    qry="SELECT * FROM feedback JOIN USER ON user.lid=feedback.lid"
    res = db.select(qry)
    return render_template('admin/view feedback.html',data=res)
@app.route('/view_feedback_search_post',methods=['post'])
def view_feedback_search_post():
    db = Db()
    ffrom=request.form['textfield']
    to=request.form['textfield2']
    qry = "SELECT * FROM feedback JOIN USER ON user.lid=feedback.lid WHERE date BETWEEN '"+ffrom+"'and'"+to+"'"
    res = db.select(qry)
    return render_template('admin/view feedback.html', data=res)






@app.route('/view_product')
def view_product():
    db=Db()
    ls = []
    try:

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        print(blocknumber)
        lq = []


        for i in range(blocknumber ,12 , -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            try:
                decoded_input = contract.decode_function_input(a['input'])
                decoded_input=decoded_input[1]
                print(decoded_input)
                print(decoded_input['pida'])
                print(decoded_input['typeofproduct'])
                print(decoded_input['description'])
                print(decoded_input['photo'])
                print(decoded_input['date'])
                print(decoded_input['price'])

                try:
                    s={'pida':str(decoded_input['pida']),'type of product':decoded_input['typeofproduct'],'description':decoded_input['description'],'photo':decoded_input['photo'],'date':decoded_input['date'],'price':decoded_input['price']}
                    ls.append(s)
                except:
                    print("heyyy")

            except Exception as b:
                print("errror",b)
                pass
                return jsonify (status='no')
    except Exception as b:
        print("errror", b)
        pass

    return render_template('admin/view product.html',data=ls)


@app.route('/view_product_search_post',methods=['post'])
def view_product_search_post():
    db=Db()
    product_name=request.form['textfield']
    qry="SELECT * FROM `product`WHERE product_name LIKE '%"+product_name+"%'"
    res=db.select(qry)
    return render_template('admin/view product.html',data=res)

# -----------------------------------------------------------------------------------------------------------------------manufacture

@app.route('/man_home')
def man_home():
    return render_template("manufacturer/manufacture_index.html")

@app.route('/registration')
def registration():
    return render_template("register_index.html")

@app.route('/register_post', methods=['post'])
def register_post():
    name=request.form['textfield']
    place = request.form['textfield2']
    pin =request.form['textfield4']
    post=request.form['textfield3']
    district=request.form['textfield5']
    phone=request.form['textfield9']
    email=request.form['textfield8']
    state=request.form['textfield6']
    logo=request.files['fileField']
    licence=request.form['textfield7']
    password=request.form['textfield10']
    confirm_password=request.form['textfield11']
    from datetime import datetime
    date=datetime.now().strftime('%Y%m%d-%H%M%S')
    logo.save("C:\\Users\\kashy\\PycharmProjects\\counterfiet\\static\\logo\\"+date+".jpg")
    path="/static/logo/"+date+".jpg"
    db=Db()
    qry1="INSERT INTO `login`(`user_name`,`password`,`type`)VALUE('"+email+"','"+confirm_password+"','manufacture')"
    res=db.insert(qry1)
    qry="INSERT INTO `manufacture`(lid,`name`,`place`,`post`,`pin`,`district`,`state`,`licence`,`email`,`phone`,`logo`,status) VALUE('"+str(res)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+district+"','"+state+"','"+licence+"','"+email+"','"+phone+"','"+path+"','pending')"
    res=db.insert(qry)
    return '''<script>alert("success");window.location='/registration'</script>'''


@app.route('/add_product')
def add_product():

    return render_template("manufacturer/add product.html")


@app.route('/add_productpost',methods=['post'])
def add_productpost():
    product=request.form['textfield']
    # type=request.form['textfield1']
    description=request.form['textfield2']
    photo=request.files['fileField']

    from datetime import  datetime

    filename= datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"

    path="C:\\Users\\kashy\\PycharmProjects\\counterfiet\\static\\photo\\"

    photo.save(path+ filename)


    p="/static/photo/"+ filename
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        print(contract_abi)
    contract = web3.eth.contract(address=deployed_contract_addressa, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    print(blocknumber)

    from datetime import  datetime
    import qrcode_p
    qrcode_p.gen_qrcode(product,str(blocknumber+1))
    pida=blocknumber+1
    typeofproduct=product
    description=description
    photo=p
    date= datetime.now().strftime("%Y-%m-%d")
    price="10"

    message2 = contract.functions.addTransaction( pida,typeofproduct , description,  photo ,  date, price).transact()
    # bob=deployed_contract_address
    # tx_hash = contract.functions.transfer(bob, 100).transact({'from':deployed_contract_addressa })
    # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)



    return render_template("manufacturer/add product.html")

@app.route('/change_password')
def change_password():
    return render_template("manufacturer/change password.html")
@app.route('/change_password_post',methods=['post'])
def change_password_post():
    current_password=request.form['textfield']
    new_password=request.form['textfield2']
    confirm_password=request.form['textfield3']
    db=Db()
    qry="SELECT * FROM `login` WHERE `lid`='"+str(session['lid'])+"' and password='"+current_password+"'"
    print(qry)
    res=db.selectOne(qry)
    print(res)
    if res is not None:
        if new_password == confirm_password:
            qry1="UPDATE `login` SET `password`='"+confirm_password+"' WHERE `lid`='"+str(session['lid'])+"'"
            res1=db.update(qry1)
            return '''<script>alert('Changed');window.location="/"</script>'''
        else:
            return '''<script>alert('confirm password does not match');window.location="/change_password"</script>'''
    else:
        return '''<script>alert('current password does not match');window.location="/change_password"</script>'''


@app.route('/edit_profile')
def edit_profile():
    db = Db()
    qry = "SELECT * FROM manufacture WHERE lid ='" + str(session['lid']) + "'"
    res = db.selectOne(qry)
    return render_template("manufacturer/edit profile.html",data=res)

@app.route('/edit_profile_post', methods=['POST'])
def edit_profile_post():
    name = request.form['textfield']
    place = request.form['textfield2']
    pin = request.form['textfield4']
    post = request.form['textfield3']
    district = request.form['textfield5']
    phone = request.form['textfield9']
    email = request.form['textfield8']
    state = request.form['textfield6']
    licence = request.form['textfield7']
    db=Db()
    if 'fileField' in request.files:
        logo = request.files['fileField']
        if logo.filename!='':
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S')
            logo.save("C:\\Users\\kashy\\PycharmProjects\\counterfiet\\static\\logo\\" + date + ".jpg")
            path = "/static/logo/" + date + ".jpg"
            qry="UPDATE `manufacture` SET `name`='"+name+"',`place`='"+place+"',`post`='"+post+"',`pin`='"+pin+"',`district`='"+district+"',`state`='"+state+"',`licence`='"+licence+"',`email`='"+email+"',`phone`='"+phone+"',`logo`='"+path+"' WHERE `lid`='"+str(session['lid'])+"'"
            res=db.update(qry)
            return redirect('/view_profile')
        else:
            qry = "UPDATE `manufacture` SET `name`='" + name + "',`place`='" + place + "',`post`='" + post + "',`pin`='" + pin + "',`district`='" + district + "',`state`='" + state + "',`licence`='" + licence + "',`email`='" + email + "',`phone`='" + phone + "' WHERE `lid`='" + str(
                session['lid']) + "'"
            res = db.update(qry)
            return redirect('/view_profile')
    else:
        qry = "UPDATE `manufacture` SET `name`='" + name + "',`place`='" + place + "',`post`='" + post + "',`pin`='" + pin + "',`district`='" + district + "',`state`='" + state + "',`licence`='" + licence + "',`email`='" + email + "',`phone`='" + phone + "' WHERE `lid`='" + str(
            session['lid']) + "'"
        res = db.update(qry)
        return redirect('/view_profile')




@app.route('/view_profile')
def view_profile():
    db=Db()
    qry="SELECT * FROM manufacture WHERE lid ='"+str(session['lid'])+"'"
    res=db.selectOne(qry)

    return render_template("manufacturer/view profile.html",data=res)

@app.route('/man_view_product')

def man_view_product():
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

    blocknumber = web3.eth.get_block_number()
    print(blocknumber)
    lq = []


    ls=[]
    for i in range(blocknumber , 12, -1):
        a = web3.eth.get_transaction_by_block(i, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            decoded_input=decoded_input[1]
            print(decoded_input)
            print(decoded_input['pida'])
            print(decoded_input['typeofproduct'])
            print(decoded_input['description'])
            print(decoded_input['photo'])
            print(decoded_input['date'])
            print(decoded_input['price'])

            try:
                s={'pida':str(decoded_input['pida']),'type of product':decoded_input['typeofproduct'],'description':decoded_input['description'],'photo':decoded_input['photo'],'date':decoded_input['date'],'price':decoded_input['price']}
                ls.append(s)
            except:
                print("heyyy")

        except Exception as a:
            print("errror",a)
            pass

    return render_template("manufacturer/view product.html",ls=ls)


# ============================================================================================================================customer

@app.route('/and_user_signup_post', methods=['POST'])
def and_user_signup_post():
    name=request.form['name']
    place=request.form['place']
    pin=request.form['pin']
    post=request.form['post']
    district=request.form['district']

    state=request.form['state']
    email=request.form['email']
    phone=request.form['phone']
    photo=request.form['photo']
    password=request.form['password']

    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    import base64
    with open("C:\\Users\\kashy\\PycharmProjects\\counterfiet\\static\\photo\\" + date + ".jpg","wb") as hj:
        hj.write(base64.b64decode(photo))
    path = "/static/photo/" + date + ".jpg"



    db=Db()
    qry="INSERT INTO `login`(`user_name`,`password`,`type`)VALUES('"+email+"','"+password+"','user')"
    res=db.insert(qry)
    qry1="INSERT INTO `user`(`lid`,`name`,`place`,`post`,`pin`,`district`,`state`,`email`,`phone`,`photo`)VALUES('"+str(res)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+district+"','"+state+"','"+email+"','"+phone+"','"+path+"')"
    res1=db.insert(qry1)
    return jsonify(status="ok")

@app.route('/and_login_post', methods=['POST'])
def and_login_post():
    username=request.form['username']
    password=request.form['password']
    db=Db()
    qry="SELECT * FROM `login` WHERE `user_name`='"+username+"' AND`password`='"+password+"' AND type='user'"
    res=db.selectOne(qry)
    if res is not None:
        db = Db()
        qryp = "SELECT * FROM `user` WHERE `lid`='"+str(res['lid'])+"'"
        resp = db.selectOne(qryp)
        return jsonify(status='ok', lid = res['lid'], type = res['type'], name = resp['name'], email = resp['email'], photo = resp['photo'])
    else:
        return jsonify(status='no')

@app.route('/and_change_password_post',methods=['post'])
def and_change_password_post():
    cp = request.form['current_pswrd']
    newp = request.form['new_pswrd']

    id=request.form['lid']
    db=Db()
    qry="SELECT * FROM`login` WHERE `lid`='"+id+"' AND `password`='"+cp+"'"
    print(qry)
    res=db.selectOne(qry)
    if res is not None:

        qry1 = "UPDATE `login` SET `password`='" + newp + "' WHERE `lid`='" + id + "'"
        print(qry1)
        res1 = db.update(qry1)
        return jsonify(status='ok')
    else:
        return jsonify(status='no')

@app.route('/and_send_complaint_post', methods=['POST'])
def and_send_complaint_post():
    db= Db()
    complaint= request.form['complaint']
    lid= request.form['lid']
    qry ="INSERT INTO `complaint`(`lid`,`date`,`complaint`,`status`)VALUES('"+lid+"',curdate(),'"+complaint+"','pending')"
    db=Db()
    res = db.insert(qry)
    return jsonify(status='ok')

@app.route('/and_view_reply_post',methods=['POST'])
def and_view_reply_post():
    db=Db()
    lid=request.form['lid']
    qry="SELECT * FROM `complaint` WHERE `lid`='"+lid+"' "
    res=db.select(qry)
    return jsonify(status='ok',data=res)



@app.route('/and_view_profile_post',methods=['post'])
def and_view_profile_post():
     db=Db()
     lid = request.form['lid']
     qry="SELECT * FROM `user` WHERE `lid`='"+lid+"'"
     res=db.selectOne(qry)
     return jsonify(status='ok', data=res)

@app.route('/and_user_edit_post', methods=['POST'])
def and_user_edit_post():
    name=request.form['name']
    place=request.form['place']
    pin=request.form['pin']
    post=request.form['post']
    district=request.form['district']

    state=request.form['state']
    email=request.form['email']
    phone=request.form['phone']
    photo=request.form['photo']
    lid=request.form['lid']
    db = Db()
    if len(photo)>1:

        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S')
        import base64
        with open("C:\\Users\\kashy\\PycharmProjects\\counterfiet\\static\\photo\\" + date + ".jpg","wb") as hj:
            hj.write(base64.b64decode(photo))
        path = "/static/photo/" + date + ".jpg"


        qry1="update `user` set `name` = '"+name+"',`place` = '"+place+"',`post` = '"+post+"',`pin` = '"+pin+"',`district` = '"+district+"',`state` = '"+state+"',`email` = '"+email+"',`phone` = '"+phone+"',`photo` = '"+path+"' where lid = '"+lid+"'"
        res1=db.insert(qry1)
        return jsonify(status="ok")
    else:
        qry1="update `user` set `name` = '"+name+"',`place` = '"+place+"',`post` = '"+post+"',`pin` = '"+pin+"',`district` = '"+district+"',`state` = '"+state+"',`email` = '"+email+"',`phone` = '"+phone+"' where lid = '"+lid+"'"
        res1=db.insert(qry1)
        return jsonify(status="ok")

    
#@app.route('/and_view_product_post', methods=['POST'])
#def and_view_product_post():
 #     db=Db()
  #    qry=""
   #  return jsonify(status='ok')

@app.route('/and_send_feedback_post',methods=['post'])
def and_send_feedback_post():
    db=Db()
    feedback=request.form['feedback']
    lid=request.form['lid']
    qry="INSERT INTO `feedback`(`lid`,`feedback`,`date`)VALUES('','',curdate())"
    res=db.insert(qry)
    return jsonify(status='ok')


@app.route('/and_view_feedback_post',methods=['post'])
def and_view_feedback_post():
    db=Db()
    lid=request.form['']
    qry="SELECT * FROM `feedback` WHERE `lid`=''"
    res=db.select(qry)
    return jsonify(status='ok')

@app.route('/and_view_manufacture_post',methods=['post'])
def and_view_manufacture_post():
    db=Db()
    qry="SELECT *FROM`manufacture`"
    res=db.select(qry)
    return jsonify(status='ok',data=res)

@app.route('/and_search_manufacture_post',methods=['post'])
def and_search_manufacture_post():
    db=Db()
    search = request.form['search']
    qry="SELECT *FROM`manufacture` where name like '%"+search+"%'"
    res=db.select(qry)
    return jsonify(status='ok',data=res)


@app.route('/verify',methods=['post'])
def verify():
    db=Db()
    try:
        content=int(request.form['content'])
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        print(blocknumber)
        lq = []


        ls=[]
        # for i in range(blocknumber , 3, -1):
        a = web3.eth.get_transaction_by_block(content, 0)
        try:
            decoded_input = contract.decode_function_input(a['input'])
            decoded_input=decoded_input[1]
            print(decoded_input)
            print(decoded_input['pida'])
            print(decoded_input['typeofproduct'])
            print(decoded_input['description'])
            print(decoded_input['photo'])
            print(decoded_input['date'])
            print(decoded_input['price'])

            try:
                s={'pida':str(decoded_input['pida']),'type of product':decoded_input['typeofproduct'],'description':decoded_input['description'],'photo':decoded_input['photo'],'date':decoded_input['date'],'price':decoded_input['price']}
                ls.append(s)
                return jsonify(status="ok",type=decoded_input['typeofproduct'],description=decoded_input['description'],photo=decoded_input['photo'],date=decoded_input['date'],price=decoded_input['price'])
            except:
                print("heyyy")
                return jsonify(status='no')

        except Exception as a:
            print("errror",a)
            pass
            return jsonify (status='no')
    except Exception as a:
        print("errror", a)
        pass
        return jsonify(status='no')


@app.route('/viewproduct',methods=['post'])
def viewproduct():
    db=Db()
    ls = []
    try:

        with open(compiled_contract_path) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

        blocknumber = web3.eth.get_block_number()
        print(blocknumber)
        lq = []


        for i in range(blocknumber ,12 , -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            try:
                decoded_input = contract.decode_function_input(a['input'])
                decoded_input=decoded_input[1]
                print(decoded_input)
                print(decoded_input['pida'])
                print(decoded_input['typeofproduct'])
                print(decoded_input['description'])
                print(decoded_input['photo'])
                print(decoded_input['date'])
                print(decoded_input['price'])

                try:
                    s={'pida':str(decoded_input['pida']),'type of product':decoded_input['typeofproduct'],'description':decoded_input['description'],'photo':decoded_input['photo'],'date':decoded_input['date'],'price':decoded_input['price']}
                    ls.append(s)
                except:
                    print("heyyy")

            except Exception as b:
                print("errror",b)
                pass
                return jsonify (status='no')
    except Exception as b:
        print("errror", b)
        pass

    return jsonify(status='ok',data=ls)



if __name__ == '__main__':
    app.run(debug = True,port=4000,host='0.0.0.0')
