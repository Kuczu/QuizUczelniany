function drawResults(json) {
	/*
	var json = '{"results": [{"text": "Pytanie 1?","answers": [{"text": "odpowiedź 1","checked": true,"correct": false}, {"text": "odpowiedź 2","checked": false,"correct": true}]}, {"text": "Pytanie 2?","answers": [{"text": "Odpowiedź 2.1","checked": true,"correct": false}, {"text": "Odpowiedź 2.2","checked": false,"correct": true}]}]}';*/
	json = JSON.parse(json);
	console.log(json);
	
	var section, card, supporting, h4, questionText, ul, li, primary, icon, answer, points, secondary, label, checkbox, qResults, curr, cYour, cAvail,
		cTYour = 0,
		cTAvail = 0,
		container = document.getElementById("results-here");
	
	for(i = 0; i < json.results.length; i += 1) {
		cYour = 0;
		cAvail = 0;
		section = document.createElement("section");
		card = document.createElement("div");
		supporting = document.createElement("div");
		h4 = document.createElement("h4");
		questionText = document.createElement("span");
		ul = document.createElement("ul");
		qResults = document.createElement("div");
		
		section.classList = "section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp";
		card.classList = "mdl-card mdl-cell mdl-cell--12-col";
		supporting.classList = "mdl-card__supporting-text mdl-grid mdl-grid--no-spacing";
		h4.classList = "mdl-cell mdl-cell--12-col";
		questionText.classList = "question-text";
		ul.classList = "mdl-list question-answers-results";
		qResults.classList = "question-total-result";
		
		h4.innerHTML = "Pytanie #" + (i + 1);
		questionText.innerHTML = json.results[i].text;
		
		for(j = 0; j < json.results[i].answers.length; j += 1) {
			curr = json.results[i].answers[j];

			li = document.createElement("li");
			primary = document.createElement("span");
			icon = document.createElement("i");
			answer = document.createElement("span");
			points = document.createElement("span");
			secondary = document.createElement("span");
			label = document.createElement("label");
			checkbox = document.createElement("input");
			
			li.classList = "mdl-list__item mdl-list__item--two-line";
			primary.classList = "mdl-list__item-primary-content";
			icon.classList = "material-icons mdl-list__item-avatar";
			answer.classList = "answer-text";
			points.classList = "mdl-list__item-sub-title";
			secondary.classList = "mdl-list__item-secondary-content";
			label.classList = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect";
			checkbox.classList = "mdl-checkbox__input";
			
			if (curr.correct === true) {
				icon.innerHTML = "done";
				cAvail += 1;
			} else {
				icon.innerHTML = "close";
			}
			answer.innerHTML = curr.text;
			if (curr.correct && curr.checked) {
				points.innerHTML = "+1 punkt";
				cYour += 1;
				checkbox.checked = true;
			} else if (!curr.correct && curr.checked) {
				points.innerHTML = "-1 punkt";
				cYour -= 1;
				checkbox.checked = true;
			} else if (curr.correct && !curr.checked) {
				points.innerHTML = "0 punktów";
				
			} else if (!curr.correct && !curr.checked){
				points.innerHTML = "0 punktów";
			}

			checkbox.type = "checkbox";
			checkbox.disabled = true;
			
			label.htmlFor = "question-" + i + "-answer-" + j;
			checkbox.id = "question-" + i + "-answer-" + j;
			
			primary.appendChild(icon);
			primary.appendChild(answer);
			primary.appendChild(points);
			label.appendChild(checkbox);
			secondary.appendChild(label);
			li.appendChild(primary);
			li.appendChild(secondary);
			ul.appendChild(li);
		}
		qResults.innerHTML = "Za to pytanie zdobyłeś " + cYour + " na " + cAvail + "punktów";
		cTAvail += cAvail;
		cTYour += cYour;
		
		supporting.appendChild(h4);
		supporting.appendChild(questionText);
		supporting.appendChild(ul);
		supporting.appendChild(qResults);
		card.appendChild(supporting);
		section.appendChild(card);
		container.appendChild(section);
	}
	document.getElementById("total-points-yours").innerHTML = " " + cTYour + " ";
	document.getElementById("total-points").innerHTML = " " + cTAvail + " ";
}

function parseResults () {
	"use strict";
	var i, json, ansCount, curr,
		container = document.getElementById("original-form");
	/*
	{
	"results": [{
		"text": "Pytanie 1?",
		"answers": [{
			"text": "odpowiedź 1",
			"checked": true,
			"correct": false
		}, {
			"text": "odpowiedź 2",
			"checked": false,
			"correct": true
		}]
	}, {
		"text": "Pytanie 2?",
		"answers": [{
			"text": "Odpowiedź 2.1",
			"checked": true,
			"correct": false
		}, {
			"text": "Odpowiedź 2.2",
			"checked": false,
			"correct": true
		}]
	}]
}
	*/
	json = '{"results":[{"text": "' + container.children[1].innerText + '","answers":[';
	
	ansCount = 0;
	for (i = 4; i < container.children.length; i += 3) {
		curr = container.children[i];
		if (i === container.children.length - 1) {
			break;
		}
		if (ansCount === 5) { //5 answers more
			ansCount = 0;
		
			json = json.slice(0, -1);
			json += ']},{"text":"' + container.children[i].innerText + '","answers":[';
			
			continue;
		}
		ansCount += 1;
		json += '{"text":"' + container.children[i].innerText + '","checked":' + container.children[i + 1].children[0].checked + ',"correct":' + (container.children[i + 2].innerText.length > 0) + '},';
	}
	json = json.slice(0, -1);
	json += ']}]}';
	
	//console.log(json);
	drawResults(json);
}