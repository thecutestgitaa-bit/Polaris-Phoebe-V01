// ===============================
// POLARIS PHOEBE SCRIPT
// ===============================


// ELEMENT
const loginPage = document.getElementById("loginPage");
const chatPage = document.getElementById("chatPage");

const namaInput = document.getElementById("nama");
const tokenInput = document.getElementById("token");

const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");

const usernameDisplay = document.getElementById("username");

const chatBox = document.getElementById("chatBox");

const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");


// DATA USER
let user = "";
let token = "";


// ===============================
// LOGIN
// ===============================

loginBtn.addEventListener("click",()=>{

    user = namaInput.value.trim();
    token = tokenInput.value.trim();

    console.log("USER:",user);
    console.log("TOKEN:",token);

    if(user === "" || token === ""){
        alert("Nama dan token harus diisi!");
        return;
    }


    localStorage.setItem(
        "phoebe_user",
        user
    );


    localStorage.setItem(
        "phoebe_token",
        token
    );


    masukChat();

}); // <-- LOGIN DITUTUP DI SINI



// ===============================
// REGISTER
// ===============================

registerBtn.addEventListener(
"click",
async()=>{


    let nama =
    namaInput.value.trim();


    if(nama===""){

        alert("Isi nama dulu!");

        return;

    }


    let response =
    await fetch(
        "http://localhost:5000/register",
        {

        method:"POST",

        headers:{
            "Content-Type":
            "application/json"
        },


        body:JSON.stringify({
            nama:nama
        })

    });


    let data =
    await response.json();


    alert(
        "Akun dibuat!\nToken kamu: "
        + data.token
    );


    tokenInput.value =
    data.token;


});



// ===============================
// AUTO LOGIN
// ===============================

window.onload = ()=>{

    let savedUser =
    localStorage.getItem("phoebe_user");

    let savedToken =
    localStorage.getItem("phoebe_token");

    alert(
        "USER: "+ savedUser +
        "\nTOKEN: "+ savedToken
    )

    if(savedUser && savedToken){

        user = savedUser;
        token = savedToken;

        masukChat();

    }

};



// ===============================
// PINDAH KE CHAT
// ===============================

function masukChat(){

    loginPage.classList.add("hidden");

    chatPage.classList.remove("hidden");


    usernameDisplay.innerText =
    user;


    addMessage(
        "Phoebe",
        `Halo ${user}, aku sudah online ✦`
    );

}



// ===============================
// KIRIM PESAN
// ===============================


sendBtn.addEventListener("click", kirimPesan);


messageInput.addEventListener(
"keydown",
(e)=>{

    if(e.key==="Enter"){

        kirimPesan();

    }

});



async function kirimPesan(){

    let text =
    messageInput.value.trim();


    if(text==="") return;


    addMessage(
        user,
        text
    );


    messageInput.value="";



try {

    let response = await fetch(
        "http://127.0.0.1:5000/chat",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                user:user,

                token:token,

                message:text

            })
        }
    );


    let data = await response.json();


    addMessage(
        "Phoebe",
        data.reply
    );


}
catch(error){

    addMessage(
        "Phoebe",
        "Maaf, aku belum bisa terhubung..."
    );

    console.error(error);

}



    /*
    NANTI GANTI INI:

    fetch("http://localhost:5000/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            user:user,
            token:token,
            message:text
        })
    })

    */

}



// ===============================
// CHAT BUBBLE
// ===============================


function addMessage(sender,text){


    let bubble =
    document.createElement("div");


    bubble.className="message";


    bubble.innerHTML = `

        <b>${sender}</b>

        <p>${text}</p>

    `;


    chatBox.appendChild(bubble);


    chatBox.scrollTop =
    chatBox.scrollHeight;

}