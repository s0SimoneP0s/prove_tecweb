var winningIndices = [
	new Set([0, 1, 2]),
	new Set([3, 4, 5]),
	new Set([6, 7, 8]),
	new Set([0, 3, 6]),
	new Set([1, 4, 7]),
	new Set([2, 5, 8]),
	new Set([0, 4, 8]),
	new Set([2, 4, 6])
  ];
  
  var curPlayer = 0;
  var playerColor = ["Tomato", "DeepSkyBlue"]
  
  var moves = [new Set(), new Set()];
  
  const title = "Tris: tocca a te player ";
  var header = document.getElementById("header");
  var clicked = 0;
  header.innerHTML = title + (curPlayer + 1);
  
  function onClick(e) {
  
	console.log("clicked " + e.id);
	var row = parseInt(e.id.charAt(1));
	var col = parseInt(e.id.charAt(2));
	e.style.backgroundColor = playerColor[curPlayer]
	e.onclick = nope;
	moves[curPlayer].add(col + row * 3);
	checkWin();
  }
  
  function checkWin() {
  
	if (moves[curPlayer].size >= 3) {
	  for (let i = 0; i < winningIndices.length; i++) {
		var wmov = winningIndices[i];
		var intersect = new Set();
		for (let x of wmov)
		  if (moves[curPlayer].has(x)) intersect.add(x);
		if (intersect.size == 3) {
		  alert("Player " + (curPlayer + 1) + " you Win!");
		  return;
		}
	  }
	}
  
	curPlayer = curPlayer == 0 ? 1 : 0;
	header.innerHTML = title + (curPlayer + 1);
	clicked++;
	if (clicked == 9) {
	  alert("Parità!");
	}
  
  }
  
  function nope() {
	alert("Già Cliccato!");
  }
  
  