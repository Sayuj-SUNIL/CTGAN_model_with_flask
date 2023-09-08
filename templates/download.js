document.getElementById('downloadButton').addEventListener('click', function () {
    // Specify the filename you want to download
    // Create a link element
    var link = document.createElement('a');
    link.href = 'http://127.0.0.1:5000/download';
    link.download = filename;
    
    // Simulate a click on the link to trigger the download
    link.click();
});