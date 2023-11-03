document.addEventListener("DOMContentLoaded", function() {
    const getAllGamesButton = document.getElementById("getAllGamesButton");
    const gameTableBody = document.getElementById("gameTableBody");

    getAllGamesButton.addEventListener("click", function() {
        // Substitua 'SUA_CHAVE_API_AQUI' pela sua chave de API
        const apiKey = "X}u~Pree#wrNj3_0v;&('h+_!";
        const url = "/getAllGames";

        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${apiKey}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na solicitação da API');
            }
            return response.json();
        })
        .then(data => {
            // Limpa o corpo da tabela antes de inserir novos dados
            gameTableBody.innerHTML = '';

            // Itera sobre os dados e insere cada jogo na tabela
            data.forEach(game => {
                const row = gameTableBody.insertRow();
                row.insertCell().textContent = game.Name;
                row.insertCell().textContent = game.Platform;
                row.insertCell().textContent = game.Genre;
                row.insertCell().textContent = game.Publisher;
                row.insertCell().textContent = game.Year;
                row.insertCell().textContent = game.NA_Sales;
                row.insertCell().textContent = game.EU_Sales;
                row.insertCell().textContent = game.JP_Sales;
                row.insertCell().textContent = game.Global;
                row.insertCell().textContent = game.Critical_Score;
                row.insertCell().textContent = game.User_Score;
            });
        })
        .catch(error => {
            console.error(error);
            gameTableBody.innerHTML = '';
            // Você pode exibir uma mensagem de erro no corpo da tabela, se desejar.
        });
    });
});
