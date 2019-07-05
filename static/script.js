var h1 = document.querySelector("h1");
// var color1 = document.querySelector(".color1");
var color = document.querySelector("#color");
var body = document.querySelector("body");
var reconnect = document.querySelector("#reconnect");
var p = document.querySelector("p");
var turnOff = document.querySelector("#turnOff");
var inputs = document.querySelectorAll("input");

// var socket = new WebSocket("ws:localhost:8080");
// var socket;

// connectSocket = () => {
//     socket = new WebSocket("ws:192.168.1.9:8080");
//     socket.onmessage = msg => {
//         var json = JSON.parse(msg.data);
//         switch (json.cod) {
//             case 200:
//                 h1.textContent = json.isOn ? "połączono" : "włącz przyciskiem";
//                 color.jscolor.fromString(json.currentColor.replace("#", ""));
//                 setColor(json.currentColor.replace("#", ""));
//                 break;
//             case 408:
//                 h1.textContent = "inne urządzenie jest już połączone";
//                 console.log("408")
//                 socket.close();
//                 break;
//             default:
//                 h1.textContent = "wystąpił błąd. spróbuj ponownie później.";
//                 console.log("error");
//                 socket.close();
//                 break;
//         }
//     }

//     socket.onclose = () => {
//         h1.textContent = "rozłączono. odśwież stronę.";
//     }
// }

// hexToRgb = hex => {
//     var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
//     return result ? {
//         r: parseInt(result[1], 16),
//         g: parseInt(result[2], 16),
//         b: parseInt(result[3], 16)
//     } : null;
// }

setColor = (jscolor) => {
    var newColor = `#${jscolor}`;
    console.log(newColor)
    body.style.background = newColor;
    var rgb = hexToRgb(newColor);
    req = open("GET", "/color", true);
    req.send();
    // if (socket !== null) {
    //     socket.send(JSON.stringify({
    //         color: newColor,
    //         changeOnce: true
    //     }));
    // }
    var luma = 0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b; // per ITU-R BT.709
    if (luma < 40) {
        h1.style.color = "#FFF";
        reconnect.style.borderColor = "#FFF";
        reconnect.style.color = "#FFF";
        turnOff.style.borderColor = "#FFF";
        turnOff.style.color = "#FFF";
        p.style.color = "#FFF";
    } else {
        h1.style.color = "#000";
        turnOff.style.borderColor = "#000";
        turnOff.style.color = "#000";
        reconnect.style.borderColor = "#000";
        reconnect.style.color = "#000";
        p.style.color="#000";
    }
}

disable = () => {
    console.log("turning off...");
    color.jscolor.fromString("000");
    setColor("000");
}

connectSocket();

// color1.addEventListener("input", setColor);
reconnect.addEventListener("click", connectSocket);
turnOff.addEventListener("click", disable);