from flask import Flask
from rag.qa import create_qa_chain
from rag import store
from routes.upload import upload_bp
from routes.ask import ask_bp


app = Flask(__name__)

try:
    store.qa_chain = create_qa_chain()
    print("QA chain created successfully.")
except Exception as e:
    print("QA chain error:", e)


app.register_blueprint(upload_bp)
app.register_blueprint(ask_bp)

@app.route("/")
def home():
    return {    "message": "RAG Knowledge Assistant is running." }



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)



'''
from flask import Flask
from rag.qa import create_qa_chain
from routes.upload import upload_bp
from routes.ask import create_ask_route


app = Flask(__name__)



try:
    qa_chain = create_qa_chain()
    print("QA chain created successfully.")

except Exception as e:
    print("QA chain error:", e)
    qa_chain = None
vector_store = None



app.register_blueprint(upload_bp)
ask_bp = create_ask_route(vector_store,qa_chain)

app.register_blueprint(ask_bp)



@app.route("/")
def home():

    return {"message": "RAG Knowledge Assistant is running."}



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

    '''


'''
import os
from flask import Flask
from flask_cors import CORS
from rag.qa import create_qa_chain
from rag.vector_store import load_vector_store
from routes.upload import upload_bp
from routes.ask import ask_bp



app = Flask(__name__)
CORS(app)



UPLOAD_FOLDER = "uploads"
VECTORSTORE_FOLDER = "vectorstore"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["VECTORSTORE_FOLDER"] = VECTORSTORE_FOLDER
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
os.makedirs(VECTORSTORE_FOLDER,exist_ok=True)



qa_chain = create_qa_chain()
app.config["QA_CHAIN"] = qa_chain
vector_store = None
faiss_index = os.path.join(VECTORSTORE_FOLDER, "index.faiss")

if os.path.exists(faiss_index):
    try:
        vector_store = load_vector_store( VECTORSTORE_FOLDER)
        print("FAISS vector store loaded.")
    except Exception as e:
        print("Could not load FAISS:",e)


app.config["VECTOR_STORE"] = vector_store
app.register_blueprint(upload_bp)
app.register_blueprint(ask_bp)



@app.route("/health",methods=["GET"])

def health():
    return {"status": "ok"}



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

    '''

