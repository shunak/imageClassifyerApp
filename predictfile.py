import os  #fileやディレクトリを扱うモジュール
from flask import Flask, request, redirect, url_for
# redirect : pageを移動　url_for : アドレスを指定してページ遷移
from werkzeug.utils import secure_filename
# secure_filename : ファイル名をサニタイズ

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
            

