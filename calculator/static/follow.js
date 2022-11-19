//Script to follow or unfollow golfer


const  button = document.querySelector('button');
button.addEventListener('click', () => {
    const golferFollow = document.getElementById('golfer').textContent;
    
    // Send POST request to modify database
    fetch('/follow', { 
        method: 'POST',
        body: JSON.stringify({
            type: button.textContent,
            golfer: golferFollow
        })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
    
    // Update Button
    if (button.textContent === 'Follow'){
        button.textContent = 'Unfollow';
    }
    else {
        button.textContent = 'Follow';
    }
})
