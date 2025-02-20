export function docPrinter(imageUrl) {
    let win = window.open('', '_blank');
    win.document.write('<html><head><title>Print Image</title></head><body>');
    win.document.write('<img src="' + imageUrl + '" onload="window.print(); window.onafterprint = function() { window.close(); }" style="max-width:100%;"/>');
    win.document.write('</body></html>');
    win.document.close();
}