let timeout_ms = 15000;
let timeoutID;

window.addEventListener("load", setup);
document.addEventListener("DOMContentLoaded", () => {
    new_msg_btn = document.getElementById("new_msg_btn");
    new_msg_btn.addEventListener("click", new_message);
})

function setup() {
    poller();
    timeoutID = window.setTimeout(poller, timeout_ms);
}

function poller() {
	fetch("/messages/")
        .then((response)=> {
            return response.json();
        })
		.then(updateChat)
        .catch((err)=>{
            chat_window.value = "error retrieving messages from server";
            console.log(err);
        })
    
    timeoutID = window.setTimeout(poller, timeout_ms);
}

function new_message() {
    fetch("/new_message/", {
        method: "post",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `author=${sessionStorage.getItem('user')}&message=${document.getElementById('new_message').value}`
    })
    .then((response)=> {
        return response.json();
    })
    .then(updateChat)
    .then(()=>{
        document.getElementById("new_message").value = "";
    })
    .catch((err)=>{
        chat_window.value = "error retrieving messages from server";
        console.log(err);
    })
}

function updateChat(results) {
    let chat_window = document.getElementById('messages');
    let messages = "";
    for (let index in results) {
        current_set = results[index];
        author = current_set['author'];
        message = current_set['message'];
        messages += `${author}:\n${message}\n\n`;
    }
    chat_window.innerText = messages;
}