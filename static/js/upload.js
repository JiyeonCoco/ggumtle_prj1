


$(function() {

    // Select File 버튼 클릭 시
    $('#select_file').on('change', function(event) {

        var file_form = /(.*?)\.(zip|tar|wget|7z)$/;
        
        var file_name = $('#select_file').val();
        real_filename = file_name.split('\\').reverse()[0];

        // 파일 확장자 확인 후 노출
        if(file_name.match(file_form)) {
            var fileInput = document.getElementById('select_file');
            var file = fileInput.files[0];
            console.log('file=', file)
            
            var formData = new FormData();
            formData.append('file', file);
            formData.append('filename', real_filename);

            $.ajax({
                url: '/upload',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                    alert(`"${real_filename}" 파일 업로드 완료`);
                },
                error: function(xhr, status, error) {
                    alert('파일 업로드 실패');
                }
            });
        }

        else {
            alert("압축 파일(zip, 7z, tar, wget 형식의 파일)만 올려주세요");
            $('#select_file').focus();
            return; 
        }
    });
});
