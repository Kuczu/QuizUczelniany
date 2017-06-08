function nextQuestion() {
	"use strict";
	var i, active, next,
		container = document.getElementById("here-questions");
	
	for (i = 1; i < container.children.length; i += 1) {
		if (container.children[i].style.display !== "none") {
			active = container.children[i];
			if (i !== container.children.length - 1) {
				next = container.children[i + 1];
			}
			break;
		}
	}
	active.style.display = "none";
	next.style.display = "block";
}
function removeElems() {
	"use strict";
	document.getElementById("realQestions").innerHTML = "";
	document.getElementById("real-form").innerHTML = "";
}

function drawElems(json) {
	"use strict";
	var i, j, card, title, titleText, supporting, hr, grid, label, input, ansText, action, actionLink, csrf,
		container = document.getElementById("here-questions"),
		orgForm = document.getElementById("real-form").children[0];
	
	csrf = document.getElementById("csrf").outerHTML;
	container.innerHTML += csrf;
	
	container.method = orgForm.method;
	container.action = orgForm.action;
	
	for (i = 0; i < json.questions.length; i += 1) {
		console.log(json.questions[i]);

		card = document.createElement("div");
		title = document.createElement("div");
		titleText = document.createElement("h2");
		supporting = document.createElement("div");
		hr = document.createElement("hr");
		grid = document.createElement("div");
		action = document.createElement("div");
		
		card.id = "question-" + i;
		card.className = "mdl-card mdl-shadow--8dp group-card question-card";
		title.className = "mdl-card__title";
		titleText.className = "mdl-card__title-text";
		supporting.className = "mdl-card__supporting-text";
		grid.className = "mdl-grid mdl-grid--no-spacing";
		action.className = "mdl-card__actions mdl-card--border";
		
		titleText.innerHTML = "Pytanie #" + (i + 1);
		supporting.innerHTML = json.questions[i].text;
		
		if (i < json.questions.length - 1) {
			actionLink = document.createElement("a");
			actionLink.className = "mdl-button";
			actionLink.innerHTML = "Dalej";
			actionLink.href = "#";
			actionLink.onclick = function () {
				nextQuestion();
			};
		} else {
			actionLink = document.createElement("button");
			actionLink.className = "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect";
			actionLink.innerHTML = "Sprawdź wyniki";
			actionLink.type = "submit";
		}
		
		for (j = 0; j < json.questions[i].answers.length; j += 1) {
			label = document.createElement("label");
			input = document.createElement("input");
			ansText = document.createElement("span");
			
			label.classList = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect";
			input.classList = "mdl-checkbox__input";
			ansText.classList = "mdl-checkbox__label";
			
			label.htmlFor = json.questions[i].ansIds[j];
			input.type = "checkbox";
			input.id = json.questions[i].ansIds[j];
			input.name = json.questions[i].ansNames[j];
			
			ansText.innerHTML = json.questions[i].answers[j];
			
			label.appendChild(input);
			label.appendChild(ansText);
			grid.appendChild(label);
		}
		title.appendChild(titleText);
		action.appendChild(actionLink);
		card.appendChild(title);
		card.appendChild(supporting);
		card.appendChild(hr);
		card.appendChild(grid);
		card.appendChild(action);
		container.appendChild(card);
	}
	removeElems();
}

function parseQuestions() {
	"use strict";
	var i, j, questions, cont, questionText, questionId, questionName, answersTexts, answersIds, answersNames,
		container = document.getElementById("realQestions");
	
	console.log(container);
	cont = new Array(container.children.length);
	
	questions = "{\"questions\":[";
	
	for (i = 0; i < container.children.length; i += 1) {
		//console.log(container.children[i]);
		if (container.children[i].tagName === "TEXTAREA") {
			questionText = container.children[i - 1].innerText;
			questionId = container.children[i].id;
			questionName = container.children[i].name;
			
			j = 0;
			answersIds = "";
			answersNames = "";
			answersTexts = "";
			while (true) {
				j += 1;
				if (container.children[i + j] === undefined || container.children[i + j].tagName === "TEXTAREA") {
					break;
				}
				if (container.children[i + j].className === "text-is-here" && container.children[i + j + 1].tagName !== "TEXTAREA") {
					if (answersIds.length > 0) {
						answersTexts += ",";
						answersIds += ",";
						answersNames += ",";
					}
					answersTexts += "\"" + container.children[i + j].innerText + "\"";
					answersIds += "\"" + container.children[i + j + 1].id + "\"";
					answersNames += "\"" + container.children[i + j + 1].name + "\"";
				}
			}
			if (questions[questions.length - 1] !== "[") {
				questions += ",";
			}
			questions += "{\"text\": \"" + questionText + "\",\"id\": \"" + questionId + "\",\"name\":\"" + questionName + "\",\"answers\":[" + answersTexts + "], \"ansIds\":[" + answersIds + "],\"ansNames\":[" + answersNames + "]}";
		}
	}
	questions += "]}";
	
	questions = JSON.parse(questions);
	drawElems(questions);
}