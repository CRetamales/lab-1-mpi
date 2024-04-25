document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.text())
    .then(data => alert(data))
    .catch(error => alert('Error al subir el archivo: ' + error));
});

function fetchResults() {
    fetch('/results')
    .then(response => response.json())
    .then(data => {
        const resultsElement = document.getElementById('results');
        resultsElement.innerHTML = '<h2>Resultados:</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
    })
    .catch(error => alert('Error al obtener resultados: ' + error));
}

/*
Function to download the results in csv format
*/
function downloadResults() {
    fetch('/save')
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('content-disposition').split('filename=')[1];
        a.click();
    })
    .catch(error => alert('Error al descargar resultados: ' + error));
}