// larger puzzles 18, smaller puzzles ?
fonstsize = 18;

window.jColors = ['red', 'mediumvioletred', '#DC143C', '#D2691E', 'gold', '#FFDEAD','#FF00FF' ,'seagreen', 'lime', '#DDA0DD', 'blue', 'dodgerblue', '#00FFFF', '#FF00FF', '#DCDCDC', '#0C0C0C'];
window.lColors = ['white', 'black', 'purple', 'darkgray', '#009'];
window.lWidths = [3, 8, 13];
window.jCols = parseInt(document.getElementById('info-creator').innerText.match(/(\d+)×/)[1]);
window.jC = 0;
CanvasRenderingContext2D.prototype.putImageData = function (imageData, dx, dy) {
    const col = window.jC % window.jCols;
    const row = Math.floor(window.jC / window.jCols);
    this.fillStyle = window.jColors[col % window.jColors.length];
    this.fillRect(-1000, -1000, 2000, 2000);
    if (0 == (row % 2)) { this.fillStyle = '#ffffff33'; this.fillRect(-1000, -1000, 2000, 2000); }
    this.fillStyle = window.lColors[row % window.lColors.length];
    // adjust position of vertical line - won't be aligned but still help differentiate columns with the same color
//    this.fillRect(-1000, 35, 2000, window.lWidths[row % window.lWidths.length]);
    this.fillStyle = window.lColors[col % window.lColors.length];
//    this.fillRect(35, -1000, window.lWidths[col % window.lWidths.length], 2000);
    // little smaller font so that the numbers are less likely to be cut of on the edge of the tile
    this.font = 'bold '+fonstsize+'px sans-serif';

    // print the col first since i sort the cols first by color and it makes it more readable
    // print it a few times since not sure where the center of the tile is
    // print it in black and white for better contrast with darker and lighter colors (and simplicity ;) )
    this.fillStyle = 'black';
    const s='·';
    const r=String.fromCharCode(0x41 + row);
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 25);
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 50);
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 75);

    this.fillStyle = 'white';
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 38);
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 63);
    this.fillText(`${col + 1},${r}${s}${col + 1},${r}${s}`.repeat(10), 0, 88);

    window.jC++;
}
if (document.getElementById("adcnt")) {
 document.getElementById("adcnt").style.display = "none";
}
if (document.getElementById("hide-panel") && (document.getElementById('sidepanel').clientHeight > 0)) {
  document.getElementById("hide-panel").dispatchEvent(new MouseEvent('click', { view: window }));
}
if (document.getElementById("restart")) {
  document.getElementById("restart").dispatchEvent(new MouseEvent('click', { view: window }));
}
