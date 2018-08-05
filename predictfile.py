import os  #fileやディレクトリを扱うモジュール
from flask import Flask, request, redirect, url_for
# redirect : pageを移動　url_for : アドレスを指定してページ遷移
from werkzeug.utils import secure_filename
# secure_filename : ファイル名をサニタイズ


import keras, sys
import numpy as np
from PIL import Image
from keras.models import Sequential, load_model


classes = ["monkey", "boar", "crow"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads' # 慣習として、大文字で
ALLOWED_EXTENSIONS = set(['png','jpg','gif'])

app = Flask(__name__) # appをFlaskのインスタンスとして初期化する
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


def allowed_file(filename):
    #ふたつのロジックのandをとっている前者のandはfilename中に'.'がふくまれるかを判断している
    #後者のandの中では、filenameを右から一回.で区切って、["配列1","配列2"]のように、
    #要素2の配列を生成。その二番目の要素[1]がALLOWE_EXTENSIONSに含まれているかを判断
    #upload可能かを判定する。両方の条件を満たすなら1を返し、満たさないなら0を返す
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST']) #@appはFlask特有の記法
def upload_file():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file'] # requestのfilesの'file'名の項目からデータをとりだす
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename)) #ディレクトリ情報のついたファイルパスを返す
            # return redirect(url_for('uploaded_file', filename=filename)) # url_for()でアップロード後のページに転送
            
            # filepathを格納する変数
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)

            # load model
            model = load_model('./animal_cnn.h5')

            # input filepath as open argv
            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax() # return max arg of result array
            percentage = int(result[predicted]*100)

            return "Label: " + classes[predicted] + ", Possibility：" + str(percentage) + " %"


    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>ファイルをアップロードして判定しよう</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう！</h1>
    <form method=post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=upload>
    </form>
    </body>
    </html>
    '''
from flask import send_from_directory # ファイルを送り返す

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)





