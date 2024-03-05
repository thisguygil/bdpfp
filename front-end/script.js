function searchTweets() {
    const query = document.getElementById('searchQuery').value;
    fetch('http://localhost:8081/search', { // Uses port-forwarding to connect to the back-end
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data, query);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayResults(results, query) {
    let resultsMessage = document.getElementById('results-message');
    // If the message element doesn't exist, create it
    if (!resultsMessage) {
        resultsMessage = document.createElement('p');
        resultsMessage.id = 'results-message';
        document.body.insertBefore(resultsMessage, document.getElementById('results'));
    }

    // Update the message text based on the results
    if (results.length > 0) {
        resultsMessage.textContent = `Search results for: "${query}"`;
    } else {
        resultsMessage.textContent = "No search results found.";
    }

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    // Display tweets if there are any
    results.forEach(result => {
        const tweetDiv = document.createElement('div');
        tweetDiv.className = 'tweet';
        
        const tweetInfo = document.createElement('p');
        tweetInfo.innerHTML = `<span class="author">${result.author}</span> - <strong>${result.date_time}</strong><br>${result.content}<br><i>❤️${result.number_of_likes}, ↗️${result.number_of_shares}</i>`;

        tweetDiv.appendChild(tweetInfo);
        resultsDiv.appendChild(tweetDiv);
    });
}
