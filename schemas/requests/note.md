# Form
Data from forms is normally encoded using the "media type" application/x-www-form-urlencoded.

But when the form includes files, it is encoded as multipart/form-data. You'll read about handling files in the next chapter.

khi không có file sẽ tự convert application/x-www-form-urlencoded. để dịch nên có thể dùng form-data gửi hoặc application/x-www-form-urlencoded

sẽ tạo filed tương ứng cho các prams  = Form() vì vậy không dùng schemas request được ví dụ định nghĩa def(form : ASchemas = Form()) => nhận prams form <dict>


# Body
    - là nhận dữ liệu dạng row data string
    - khi co File() thì cũng sẽ ở dạng multipart/form-data sẽ tạo ra filed tương ứng nên không thể dùng schemas request để định nghĩa/ read các filed gửi nên gán vào prams <dict>
    ví dụ khi không có file def(form : ASchemas = Form())  hoặc | def(form : ASchemas ) sẽ nhận prams ở dạng body row data gửi lên

## khi gửi file phải định nghĩa rõ các field 
   