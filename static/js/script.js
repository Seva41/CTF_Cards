document.getElementById('encrypt-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('text').value;
    const key = document.getElementById('key').value;
    const mode = document.getElementById('mode').value;

    const response = await fetch('/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, key, mode })
    });
    const result = await response.json();
    alert("Texto cifrado: " + result.encrypted);
});

document.getElementById('decrypt-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const encrypted = document.getElementById('encrypted').value;
    const key = document.getElementById('key-decrypt').value;
    const mode = document.getElementById('mode-decrypt').value;

    const response = await fetch('/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encrypted, key, mode })
    });
    const result = await response.json();
    alert("Texto descifrado: " + result.decrypted);
});
