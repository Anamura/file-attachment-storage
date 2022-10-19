## File Attachment Storage

Хранилище файлов с доступом по http

предоставляет REST API для загрузки (upload), скачивания (download) и удаления файлов.<br/>
тип авторизации пользователей: **Basic**.<br/><br/>


Файлы сохраняются на диск в следующую структуру каталогов:

       store/ab/abcdef12345...
где "abcdef12345..." - имя файла, совпадающее с его хэшем.<br/>
/ab/ - подкаталог, состоящий из первых двух символов хэша файла.
<br/><br/>

<img width="698" alt="swagger_docs" src="https://user-images.githubusercontent.com/5726929/196762845-23c52804-169f-4124-8f36-35620e9440d5.png">


### Usage

      $ curl -X POST "http://127.0.0.1:5000/api/files/upload" -H  "Authorization: Basic dGVzdDp0ZXN0"
                                                              -H "Content-Type: multipart/form-data"
                                                              -F "file=@dog_1;type="
      {
        "hash": "564298b1cf9539b57f32737d7673f5bb"
      }
    
      $ DELETE http://localhost:5000/api/files/delete/{hash} -H  "Authorization: Basic dGVzdDp0ZXN0"
      {
        OK
      }
    
      $ curl -X GET "http://127.0.0.1:5000/api/files/download/{hash}" -H  "accept: application/json"
      {
        content-disposition: attachment; filename= 
        content-length: 83871 
        content-type: file
        cache-control: public,max-age=43200
      }
