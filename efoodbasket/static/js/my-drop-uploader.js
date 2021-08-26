window.addEventListener("load", function () {
  let dropArea = document.getElementById("drop-area");
  var fileInpt = document.getElementById("fileElem");

  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, highlight, false);
  });
  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, unhighlight, false);
  });

  dropArea.addEventListener("drop", handleDrop, false);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight(e) {
    dropArea.classList.add("highlight");
  }

  function unhighlight(e) {
    dropArea.classList.remove("highlight");
  }

  function handleDrop(e) {
    var dt = e.dataTransfer;
    var files = dt.files;

    handleFiles(files, true);
  }

  function handleFiles(files, isDropped) {
    document.getElementById("gallery").innerHTML = "";
    if (isDropped) {
      fileInpt.files = files;
    }
    files = [...files];
    files.forEach(previewFile);
  }

  function previewFile(file) {
    let reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = function () {
      let img = document.createElement("img");
      img.className = "upload-preview-img";
      img.src = reader.result;
      document.getElementById("gallery").appendChild(img);
    };
  }

  fileInpt.onchange = function () {
    var files = this.files;
    handleFiles(files);
  };
});
