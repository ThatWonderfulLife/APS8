document.getElementById('getAllGames').addEventListener('click', function() {
    fetch('http://177.74.186.5:5001/getAllGames', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer X}u~Pree#wrNj3_0v;&(\'h+_!'
        }
    })
    .then(response => response.json())
    .then(data => document.getElementById('data').textContent = JSON.stringify(data))
    .catch(error => console.error('Error:', error));
});

// Você pode adicionar mais funções de evento aqui para lidar com outras rotas, como /getGameID/<id>, /getAllGamesByConsole/<console>, etc.
// Por exemplo:
/*
document.getElementById('getGameID').addEventListener('click', function() {
    var id = document.getElementById('gameID').value;
    fetch(`http://localhost:5001/getGameID/${id}`, {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer X}u~Pree#wrNj3_0v;&(\'h+_!'
        }
    })
    .then(response => response.json())
    .then(data => document.getElementById('data').textContent = JSON.stringify(data))
    .catch(error => console.error('Error:', error));
});
*/
