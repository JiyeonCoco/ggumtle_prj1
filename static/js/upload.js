


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
                    console.log('response=', response);
                    alert(`"${real_filename}" 파일 업로드 완료`);

                    var html = "<table border='1'>";
                    html += "<tr><th>Input</th><th>Xmin</th><th>Ymin</th><th>Xmax</th><th>Ymax</th><th>Confidence</th><th>Name</th></tr>";
                    $.each(response, function(index, row) {
                        html += "<tr>";
                        html += "<td>" + row['input'] + "</td>";
                        html += "<td>" + row['xmin'] + "</td>";
                        html += "<td>" + row['ymin'] + "</td>";
                        html += "<td>" + row['xmax'] + "</td>";
                        html += "<td>" + row['ymax'] + "</td>";
                        html += "<td>" + row['confidence'] + "</td>";
                        html += "<td>" + row['name'] + "</td>";
                        html += "</tr>";
                    });
                    html += "</table>";

                    // var data = JSON.parse(response);
                    // console.log('data=', data);

                    // var html = "<table border='1'>";
                    // html += "<tr><th>Input</th><th>Xmin</th><th>Ymin</th><th>Xmax</th><th>Ymax</th><th>Confidence</th><th>Name</th></tr>";
                    // data.forEach(function(item) {
                    //     html += "<tr><td>" + item.input + "</td><td>" + item.xmin + "</td><td>" + item.ymin + "</td><td>" + item.xmax + "</td><td>" + item.ymax + "</td><td>" + item.confidence + "</td><td>" + item.name + "</td></tr>";
                    // });
                    // html += "</table>";
                    // $("#return_div").html(html);
                    $('#result-container').html(html);
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
