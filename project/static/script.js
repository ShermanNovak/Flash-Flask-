document.addEventListener('DOMContentLoaded', function() {
    home_href();
    content();
    status();
    onlyone();
});

/* make deck_name in home page direct to viewer */
function home_href() {
    var deck_href = document.querySelectorAll('.deck_href');
    if (window.location.pathname=='/home') {
        for (var i = 0; i < deck_href.length; i++) {
            var deck_name = deck_href[i].innerHTML;
            var direct_to = "/view/" + deck_name + "/1";
            deck_href[i].setAttribute('href', direct_to);
        }
    }
};

/* make content of card appear once the show_content button is clicked */
function content() {
    var hidden_content = document.querySelector('#hidden_content');
    var hidden_label = document.querySelector('#hidden_label');
    var show_content = document.querySelector('#show_content');
    var status_form = document.querySelector('#status_form');
    if (hidden_content && hidden_label && show_content && status_form) {
        show_content.addEventListener('click', function() {
            hidden_label.removeAttribute('hidden');
            hidden_content.removeAttribute('hidden');
            status_form.removeAttribute('hidden');
        })
    }
};

/* display status color for each card in edit_deck*/
function status() {
    var status_color = document.querySelectorAll('.status_color');
    var dot = document.querySelectorAll('.dot');
    for (var i = 0; i < dot.length; i++) {
        if (status_color[i].innerHTML == "Green") {
            dot[i].style.backgroundColor = "green";
        }
        if (status_color[i].innerHTML == "Yellow") {
            dot[i].style.backgroundColor = "#fee12b";
        }
        if (status_color[i].innerHTML == "Red") {
            dot[i].style.backgroundColor = "#c81d25";
        }
    }
}

/* make sure only one checkbox can be checked at any one time */
function onlyone() {
    var checkboxes = document.querySelectorAll('.form-check-input');
    checkboxes.forEach((box) => {
        box.addEventListener('click', function () {
            for (var j = 0; j < checkboxes.length; j++) {
                checkboxes[j].checked = false;
            }
            box.checked = true;
        })
    })
}