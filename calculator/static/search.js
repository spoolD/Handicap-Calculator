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

    const button = document.createElement('button');
    // make fetch request to database for golfers being followed

    // if followed make button say 'unfollow'

    // else make button say 'follow'

    // add follow/unfollow logic to both from follow.js

    document.querySelector('#results').append(container);
}

