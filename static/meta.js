const connectButton = document.getElementById("connect-metamask");
connectButton.addEventListener("click", async () => {
    if (window.ethereum) {
        try {
            const accounts = await ethereum.request({method: "eth_requestAccounts"});
            const walletAddress = accounts[0];

            // Отправка адреса на backend
            await fetch("/connect-wallet", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({wallet_address: walletAddress}),
            });

            // Обновление страницы
            location.reload();
        } catch (err) {
            console.error("Ошибка подключения MetaMask:", err);
        }
    } else {
        alert("MetaMask не установлен!");
    }
});
