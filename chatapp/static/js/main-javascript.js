window.addEventListener('load', setup);

let timeoutID;
let timeout = 5000;

function setup(){
    console.log("setup function");
    addbutton = document.getElementById("send");
    addbutton.addEventListener("click", addnewmessage);
    timeoutID = window.setTimeout(poller, timeout);
}

function addnewmessage(){
    author = document.getElementById("username").value;
    message = document.getElementById("sendmessage").value;
    console.log(author)
    console.log(message)
    fetch("/new_message", { 
        method: "post", 
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }, 
        body: `username=${author}&message=${message}` 
    }).then(()=>{
        document.getElementById("sendmessage").value = "";
        showmessage();
    })
    .catch(error => console.error("Fetch Error =\n", error)
    ); 
}

function showmessage(){
    fetch("/messages/") 
    .then((response) => { 
        return response.json(); 
    }) 
    .then((results) => {
        let chat_window = document.getElementById("chat_window"); 
        let messages = ""; 
        for (let index in results) { 
            current_set = results[index]; 
            author = current_set.username; 
            message = current_set.message; 
            messages += `${author}:\n${message}\n\n`; 
        } 
        
        chat_window.value = messages;
        timeoutID = window.setTimeout(poller, timeout);
    }) 
    .catch(() => { 
        chat_window.value = "error retrieving messages from server"; 
    }); 
}

function poller() {
	console.log("Polling for new items");
	fetch("/messages")
		.then((response) => {
			return response.json();
		})
		.then(showmessage)
		.catch(() => {
			console.log("Error fetching items!");
		});
}
