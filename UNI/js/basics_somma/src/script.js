//costante
const message = "Titolo";

//ottenimento di un elemento HTML tramite id
document.querySelector("#header").innerHTML = message;

//variabile e scrittura alternativa per l'ottenimento di elementi dal documento.
var header = document.getElementById("header");

//manipolazione dei valori (concatenazione di stringhe)
header.innerHTML += " della Pagina";

/*
print su console, visibile dalla visuale dello sviluppatore 
del browser.
*/
console.log(message);
miaFunzione(message); //chiamata a funzione.

e = document.getElementById("campo1_id");
nascondiElemento(/*e*/);

//funzione
function miaFunzione(str) {
  console.log("La stringa in ingresso ha " + str.length + " caratteri");
}

function nascondiElemento(elemento=null){
		if (elemento == null)
    	return;
    elemento.type = "hidden";
}

//gestione degli eventi:
var b = document.getElementById("button_id");
b.onclick = onClick;
b.value = "Mostra Alert"

function onClick(){
	window.alert("Data: " + Date())
}

// complica

var subBtn = document.getElementById("sub_id");
subBtn.onclick = function (id) { operazione(subBtn.id); }

	function operazione(id){
		const a = parseInt(document.getElementById("campo1_id").value);
		const b = parseInt(document.getElementById("campo2_id").value);
		switch(id){
			case "sum_id":
				header.innerHTML = a+b;
			break;
			default:
				header.innerHTML = a-b;
		}
	}






	