import * as FilePond from "filepond";
import FilePondPluginFileValidateSize from "filepond-plugin-file-validate-size";
import FilePondPluginFileValidateType from "filepond-plugin-file-validate-type";
import "filepond/dist/filepond.min.css";

const $ = require("jquery");

document.addEventListener("DOMContentLoaded", function () {
	var files = [];
	FilePond.registerPlugin(FilePondPluginFileValidateSize);
	FilePond.registerPlugin(FilePondPluginFileValidateType);
	FilePond.setOptions({
		allowMultiple: true,
		maxFiles: 20,
		maxFileSize: "3MB",
	});
	const inputElement = document.querySelector('input[type="file"]');
	const pond = FilePond.create(inputElement, {
		acceptedFileTypes: ["image/png", "image/jpeg"],
		onaddfile: (err, fileItem) => {
			if (!err) {
				files.push(fileItem.file);
			}
			console.log(files);
		},
		onremovefile: (err, fileItem) => {
			const index = files.indexOf(fileItem.file);
			if (index > -1) {
				files.splice(index, 1);
			}
			console.log(files);
		},
	});

	var formData = new FormData();
	$(document).on("click", "#saveBtn", function (e) {
		if (
			$("#id_tahapan").val() === "" ||
			$("#id_bentuk").val() === "" ||
			$("#id_tujuan").val() === "" ||
			$("#id_sasaran").val() === "" ||
			$("#id_waktu").val() === "" ||
			$("#id_tempat").val() === "" ||
			$("#id_uraian").val() === ""
		) {
			alert("Please fill in all required fields");
			return; // Prevent form submission
		}

		formData.append("length", files.length);
		formData.append("tahapan", $("#id_tahapan").val());
		formData.append("bentuk", $("#id_bentuk").val());
		formData.append("tujuan", $("#id_tujuan").val());
		formData.append("sasaran", $("#id_sasaran").val());
		formData.append("waktu", $("#id_waktu").val());
		formData.append("tempat", $("#id_tempat").val());
		formData.append("uraian", $("#id_uraian").val());
		for (var i = 0; i < files.length; i++) {
			formData.append("images" + i, files[i]);
		}
		formData.append("csrfmiddlewaretoken", "{{ csrf_token }}");

		$.ajax({
			type: "POST",
			url: '{% url "ptps:LhpAddView" %}',
			data: formData,
			cache: false,
			processData: false,
			contentType: false,
			enctype: "multipart/form-data",
			success: function () {
				alert("LHP Anda Sudah dibuat!");
			},
			error: function (xhr, errmsg, err) {
				console.log(xhr.status + ":" + xhr.responseText);
			},
		});
	});
});
