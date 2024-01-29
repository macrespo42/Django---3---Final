const roomName = JSON.parse(document.getElementById("room-name").textContent);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

chatSocket.onmessage((e) => {
  const data = JSON.parse(e.data);
  document.querySelector("#chat-log").value += `${data}\n`;
});

chatSocket.onclose(() => {
  console.error("Chat closes unexpectedly");
});

const messageInput = document.querySelector("#chat-message-input");

messageInput.focus();
messageInput.onkeyup() = (e) => {
  if (e.key === "Enter") {
    document.querySelector("#chat-message-submit").click();
  }
}

document.querySelector("#chat-message-submit").onclick = () => {
  const message = messageInput.value;
  chatSocket.send(JSON.stringify({
    'message': message,
  }));
  messageInput.value = ""
}
