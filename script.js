async function encryptText() {
    const text = document.getElementById("input-text").value;
    if (text) {
        const result = await window.pywebview.api.encrypt(text);
        document.getElementById("output-text").value = result;
    }
}

async function decryptText() {
    const text = document.getElementById("input-text").value;
    if (text) {
        const result = await window.pywebview.api.decrypt(text);
        document.getElementById("output-text").value = result;
    }
}

async function openFile() {
    const content = await window.pywebview.api.open_file();
    if (content) {
        document.getElementById("input-text").value = content;
    }
}

async function saveFile() {
    const result = document.getElementById("output-text").value;
    if (result) {
        const msg = await window.pywebview.api.save_file(result);
        alert(msg);
    }
}

function copyResult() {
    const result = document.getElementById("output-text").value;
    if (result) {
        navigator.clipboard.writeText(result);
        alert("Скопировано!");
    }
}
