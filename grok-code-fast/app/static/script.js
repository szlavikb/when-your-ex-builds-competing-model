document.addEventListener('DOMContentLoaded', function() {
    const newsContainer = document.getElementById('newsContainer');
    const driversContainer = document.getElementById('driversContainer');
    const constructorsContainer = document.getElementById('constructorsContainer');
    const refreshNewsBtn = document.getElementById('refreshNewsBtn');
    const refreshDriversBtn = document.getElementById('refreshDriversBtn');
    const refreshConstructorsBtn = document.getElementById('refreshConstructorsBtn');

    // Function to fetch and display news
    function loadNews() {
        // Show loading spinner
        newsContainer.innerHTML = `
            <div class="col-12 loading">
                <div class="spinner"></div>
                <p class="mt-3">Loading F1 news...</p>
            </div>
        `;

        fetch('/api/news')
            .then(response => response.json())
            .then(data => {
                displayNews(data);
            })
            .catch(error => {
                console.error('Error fetching news:', error);
                newsContainer.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle"></i> Failed to load news. Please try again later.
                        </div>
                    </div>
                `;
            });
    }

    // Function to display news items
    function displayNews(newsItems) {
        if (newsItems.length === 0) {
            newsContainer.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info" role="alert">
                        <i class="fas fa-info-circle"></i> No news available at the moment.
                    </div>
                </div>
            `;
            return;
        }

        newsContainer.innerHTML = newsItems.map((item, index) => `
            <div class="col-md-6 col-lg-4 mb-4 fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="card h-100">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">
                            <i class="fas fa-newspaper"></i> ${item.title}
                        </h5>
                        <p class="card-text flex-grow-1">${item.summary}</p>
                        <div class="mt-auto">
                            <small class="text-muted">
                                <i class="fas fa-calendar"></i> ${new Date(item.published).toLocaleDateString()}
                                ${item.source ? ` • <i class="fas fa-globe"></i> ${item.source}` : ''}
                            </small>
                            <br>
                            <a href="${item.link}" target="_blank" class="btn btn-sm btn-outline-primary mt-2">
                                <i class="fas fa-external-link-alt"></i> Read More
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Function to fetch and display driver standings
    function loadDriverStandings() {
        driversContainer.innerHTML = `
            <div class="col-12 loading">
                <div class="spinner"></div>
                <p class="mt-3">Loading driver standings...</p>
            </div>
        `;

        fetch('/api/driver-standings')
            .then(response => response.json())
            .then(data => {
                displayDriverStandings(data);
            })
            .catch(error => {
                console.error('Error fetching driver standings:', error);
                driversContainer.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle"></i> Failed to load driver standings. Please try again later.
                        </div>
                    </div>
                `;
            });
    }

    // Function to display driver standings
    function displayDriverStandings(standings) {
        if (standings.length === 0) {
            driversContainer.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info" role="alert">
                        <i class="fas fa-info-circle"></i> No standings available at the moment.
                    </div>
                </div>
            `;
            return;
        }

        driversContainer.innerHTML = standings.map((driver, index) => `
            <div class="col-md-6 col-lg-4 mb-4 fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="card h-100">
                    <div class="card-body d-flex flex-column text-center">
                        <div class="position-absolute top-0 start-0 bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; font-weight: bold;">
                            ${driver.position}
                        </div>
                        <h5 class="card-title mt-3">${driver.name}</h5>
                        <p class="card-text">
                            <strong>Team:</strong> ${driver.constructor}<br>
                            <strong>Nationality:</strong> ${driver.nationality}<br>
                            <strong>Points:</strong> ${driver.points}<br>
                            <strong>Wins:</strong> ${driver.wins}
                        </p>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Function to fetch and display constructor standings
    function loadConstructorStandings() {
        constructorsContainer.innerHTML = `
            <div class="col-12 loading">
                <div class="spinner"></div>
                <p class="mt-3">Loading constructor standings...</p>
            </div>
        `;

        fetch('/api/constructor-standings')
            .then(response => response.json())
            .then(data => {
                displayConstructorStandings(data);
            })
            .catch(error => {
                console.error('Error fetching constructor standings:', error);
                constructorsContainer.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            <i class="fas fa-exclamation-triangle"></i> Failed to load constructor standings. Please try again later.
                        </div>
                    </div>
                `;
            });
    }

    // Function to display constructor standings
    function displayConstructorStandings(standings) {
        if (standings.length === 0) {
            constructorsContainer.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-info" role="alert">
                        <i class="fas fa-info-circle"></i> No standings available at the moment.
                    </div>
                </div>
            `;
            return;
        }

        constructorsContainer.innerHTML = standings.map((constructor, index) => `
            <div class="col-md-6 col-lg-4 mb-4 fade-in" style="animation-delay: ${index * 0.1}s">
                <div class="card h-100">
                    <div class="card-body d-flex flex-column text-center">
                        <div class="position-absolute top-0 start-0 bg-success text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 40px; height: 40px; font-weight: bold;">
                            ${constructor.position}
                        </div>
                        <h5 class="card-title mt-3">${constructor.name}</h5>
                        <p class="card-text">
                            <strong>Nationality:</strong> ${constructor.nationality}<br>
                            <strong>Points:</strong> ${constructor.points}<br>
                            <strong>Wins:</strong> ${constructor.wins}
                        </p>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Load news and standings on page load
    loadNews();
    loadDriverStandings();  // Load driver standings immediately
    loadConstructorStandings();  // Load constructor standings immediately

    // Event listeners
    refreshNewsBtn.addEventListener('click', loadNews);
    refreshDriversBtn.addEventListener('click', loadDriverStandings);
    refreshConstructorsBtn.addEventListener('click', loadConstructorStandings);

    // Load standings when tabs are clicked (only if not already loaded)
    document.getElementById('drivers-tab').addEventListener('click', function() {
        if (driversContainer.innerHTML.trim() === '' ||
            driversContainer.querySelector('.loading') ||
            driversContainer.querySelector('.alert')) {
            loadDriverStandings();
        }
    });

    document.getElementById('constructors-tab').addEventListener('click', function() {
        if (constructorsContainer.innerHTML.trim() === '' ||
            constructorsContainer.querySelector('.loading') ||
            constructorsContainer.querySelector('.alert')) {
            loadConstructorStandings();
        }
    });

    // Auto-refresh news every 5 minutes
    setInterval(loadNews, 300000);
});
