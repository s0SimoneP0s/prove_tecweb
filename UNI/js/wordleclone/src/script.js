var fiveLwords = [
	"which",
	"there",
	"their",
	"about",
	"would",
	"these",
	"other",
	"words",
	"could",
	"write",
	"first",
	"water",
	"after",
	"where",
	"right",
	"think",
	"three",
	"years",
	"place"
  ];
  
  for (let i = 0; i < fiveLwords.length; i++)
	fiveLwords[i] = fiveLwords[i].toUpperCase();
  

  
  //costruzione pagina
  const ENG_ALPHA = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
  var table = document.getElementById("tableA_id");
  var gameTable = document.getElementById("tableGame_id");
  var tr = null;
  
  for (let i = 0; i < 25; i++) {
  
	if (i % 5 == 0) {
	  tr = document.createElement("tr");
	  tr.id = "tr" + i + "_id";
	  gameTable.appendChild(tr);
	}
  
	let node = document.createElement("td");
	node.id = i + "_id";
	node.style.backgroundColor = "MidnightBlue";
	node.innerHTML = " ";
	tr.appendChild(node);
  }
  
  tr = null;
  for (let i = 0; i < ENG_ALPHA.length; i++) {
  
	if (i % 10 == 0) {
	  tr = document.createElement("tr");
	  tr.id = "trA" + i + "_id";
	  table.appendChild(tr);
	}
  
	let node = document.createElement("td");
	node.id = ENG_ALPHA[i] + "_id";
	node.style.backgroundColor = "LightSeaGreen";
	node.onclick = function() { onClick(this); };
	node.innerHTML = ENG_ALPHA[i];
	tr.appendChild(node);
  
  }
  
  //logica di gioco
  
  const randomWord = fiveLwords[Math.floor(Math.random() * (fiveLwords.length - 1))];
  var dictWord = {};
  
  for (let i = 0; i < randomWord.length; i++) {
	if (!(randomWord[i] in dictWord))
	  dictWord[randomWord[i]] = [i];
	else
	  dictWord[randomWord[i]].push(i);
  }
  
  var curCursore = 0;
  var guessStr = "";
  var hasToGuess = false;
  
  console.log(randomWord);
  console.log(dictWord);
  
  function onClick(e) {
  
	if (hasToGuess)
	  return;
  
	var car = e.innerHTML;
	var w = document.getElementById(curCursore + "_id");
	w.innerHTML = car;
	guessStr += car;
	curCursore++;
	if (curCursore % 5 == 0)
	  hasToGuess = true;
  }
  
  
  function guess() {
  
	console.log(curCursore);
  
	if (!hasToGuess)
	  return;
  
	for (let i = 0; i < guessStr.length; i++) {
  
	  let index = curCursore - 5 + i;
  
	  if (!(guessStr[i] in dictWord)) {
		document.getElementById(guessStr[i] + "_id").style.backgroundColor = "LightSlateGrey";
		document.getElementById(index + "_id").style.backgroundColor = "LightSlateGrey";
	  } else {
  
		let l = dictWord[guessStr[i]];
  
		for (let p = 0; p < l.length; p++) {
  
		  if (i == l[p]) {
			document.getElementById(index + "_id").style.backgroundColor = "LightGreen";
			continue;
		  } else
			document.getElementById(index + "_id").style.backgroundColor = "LemonChiffon";
		}
	  }
  
	}
  
	if (guessStr == randomWord)
	  alert("You Win!")
	else {
	  guessStr = "";
	  if (curCursore == 25)
		alert("You Lost!");
	  else
		hasToGuess = false;
	}
  
  
  }
  