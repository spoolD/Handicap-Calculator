const golferSearch = document.getElementById('golfer-search')

golferSearch.addEventListener('input', (event) => {
    //Clear current output
    results = document.querySelector('#results');
    results.innerText = '';

    // query database based on current value
    fetch('/search/+' + golferSearch.value)
    .then(response => response.json())
    .then(golfers => {
        console.log(golfers)
        if (Object.entries(golfers).length > 0){
            Object.values(golfers).forEach(golfer => {
                add_golfer(golfer);
            })
        }
        else {
            results.innerText = 'No Golfers Found'
        }
    });

})

function add_golfer(golfer){
    const container = document.createElement('div');

    const user_container = document.createElement('div');
    const user = document.createElement('a')
    user.textContent = golfer.username + ' (' + golfer.handicap + ')';
    user.href = 'find/' + golfer.username
    user_container.append(user)
    container.append(user_container);

    document.querySelector('#results').append(container);
}

