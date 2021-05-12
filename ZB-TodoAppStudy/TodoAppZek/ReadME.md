 1. python kurun 
https://www.python.org/downloads/   

 2.MongoDB kurun
 https://www.mongodb.com/download-center#community 

Proje ortamına Flask, bson & pymongo u install edin
>pip install Flask

>pip install bson

>pip install pymongo

Mongodb örneğini çalıştırmadan önce, bir veri klasörü oluşturup  komut isteminde aşağıdaki komutu çalıştırın.

"C:\Program Files\MongoDB\Server\4.0\bin\mongod.exe" --dbpath="C:\mongo-data"

Burada C: \ mongo-data klasörü mongodb dosyalarını kaydetmek için kullanılır.
mongo db localhost 27017 portundan haberleşir

python app.py i run edin

http://127.0.0.1:5000/ adresinde uygulamayı görüntüleyebilirsiniz.

Postman üzerinde;

>   http://127.0.0.1:5000/getTodos adresine GET isteğinde bulunup todoları görebilirsiniz
>   http://127.0.0.1:5000/addTodo adresine POST isteğinde bulunup Json formatında verdiğiniz todoyu ekleyebilirsiniz {"Title":"newtodo","desc":"todo desc"}
>   http://127.0.0.1:5000/updateTodo/güncellemek istediğiniz Todo id sini buraya girip  PUT isteğinde bulunup tuduyu güncelleyebilirsiniz.  {"Title":"newtodo","desc":"todo desc"}
>   http://127.0.0.1:5000/deleteTodo adresine DELETE isteğinde bulunup json formatında verdiğiniz id e göre todoyu silebilirsiniz. {"_id":"609ad36099273de69e742a12"} gibi
"
