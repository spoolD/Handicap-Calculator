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

    const user = document.createElement('div');
    user.innerText = golfer.username;
    container.append(user);

    const handicap = document.createElement('div');
    handicap.innerText = golfer.handicap;
    container.append(handicap);

    document.querySelector('#results').append(container);
}

