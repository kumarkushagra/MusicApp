// Global variables to manage player state
let songs = [];
let currentSongIndex = 0;
let isShuffleMode = false;

// Initialize the music player when the page loads
document.addEventListener('DOMContentLoaded', function() {
    fetchSongs();
    setupAudioPlayerControls();
    setupKeyboardControls();
    playSelectedSong();
});

// Fetch available songs from the backend
async function fetchSongs() {
    try {
        const response = await fetch('/songs');
        songs = await response.json();
        
        const songSelector = document.getElementById('songSelector');
        songSelector.innerHTML = ''; // Clear existing options
        
        songs.forEach((song, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = formatSongName(song);
            option.setAttribute('aria-label', `Select song: ${formatSongName(song)}`);
            option.addEventListener('dblclick', () => playSongFromList(index));
            songSelector.appendChild(option);
        });

        // Initial song load
        if (songs.length > 0) {
            updateSongDetails(0);
        }
    } catch (error) {
        console.error('Error fetching songs:', error);
        displayErrorMessage('Unable to load songs. Please refresh the page.');
    }
}

// Format song name for display (remove file extension, replace underscores)
function formatSongName(songFileName) {
    return songFileName
        .replace('.mp3', '')
        .replace(/_/g, ' ')
        .replace(/-/g, ' ')
        .replace(/128 ytshorts.savetube.me/g, ' ')
        .trim();
}

// Set up audio player controls
function setupAudioPlayerControls() {
    const audioPlayer = document.getElementById('audioPlayer');
    const progressBar = document.getElementById('progressBar');

    // Time update for progress bar
    audioPlayer.addEventListener('timeupdate', function() {
        if (audioPlayer.duration) {
            const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
            progressBar.style.width = `${progress}%`;
            progressBar.setAttribute('aria-valuenow', progress.toFixed(0));
            updateCurrentTimeDisplay();
        }
    });
    
    // Auto-play next song when current song ends
    audioPlayer.addEventListener('ended', function() {
        nextSong();
    });

    // Add click event to progress bar to seek
    const progressContainer = document.querySelector('.progress-container');
    progressContainer.addEventListener('click', function(e) {
        const audioPlayer = document.getElementById('audioPlayer');
        if (audioPlayer.duration) {
            const progressBarWidth = this.offsetWidth;
            const clickPosition = e.offsetX;
            const percentage = clickPosition / progressBarWidth;
            
            audioPlayer.currentTime = audioPlayer.duration * percentage;
        }
    });
}

// Setup keyboard controls for better accessibility
function setupKeyboardControls() {
    document.addEventListener('keydown', function(e) {
        const audioPlayer = document.getElementById('audioPlayer');

        // Skip handling if the user is typing in an input or textarea
        const activeElement = document.activeElement;
        if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA') {
            return;
        }

        if (e.code === 'Space') {
            e.preventDefault(); // Prevent page scrolling when Space is pressed
            if (audioPlayer.paused) {
                audioPlayer.play();
            } else {
                audioPlayer.pause();
            }
        }

        // Left/Right arrow keys for previous/next song
        if (e.code === 'ArrowLeft') {
            previousSong();
        }
        if (e.code === 'ArrowRight') {
            nextSong();
        }

        // Up/Down arrow keys for volume control
        if (e.code === 'ArrowUp') {
            e.preventDefault(); // Prevent page scrolling when Arrow Up is pressed
            audioPlayer.volume = Math.min(audioPlayer.volume + 0.05, 1); // Increase volume (max 1)
        }
        if (e.code === 'ArrowDown') {
            e.preventDefault(); // Prevent page scrolling when Arrow Down is pressed
            audioPlayer.volume = Math.max(audioPlayer.volume - 0.05, 0); // Decrease volume (min 0)
        }
    });
}


// Update current time display
function updateCurrentTimeDisplay() {
    const audioPlayer = document.getElementById('audioPlayer');
    const currentSongInfo = document.getElementById('currentSongInfo');
    
    if (audioPlayer.currentTime && audioPlayer.duration) {
        const songName = formatSongName(songs[currentSongIndex]);
        currentSongInfo.textContent = `Now Playing: ${songName} - ${formatTime(audioPlayer.currentTime)} / ${formatTime(audioPlayer.duration)}`;
    }
}

// Format time in minutes:seconds
function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Display error message to user
function displayErrorMessage(message) {
    const songMetadata = document.getElementById('songMetadata');
    songMetadata.innerHTML = `<p class="error">${message}</p>`;
}

// Play a song directly from the list
function playSongFromList(index) {
    const songSelector = document.getElementById('songSelector');
    const audioPlayer = document.getElementById('audioPlayer');
    
    currentSongIndex = index;
    songSelector.selectedIndex = currentSongIndex;
    
    updateSongDetails(index);
    audioPlayer.play();
}

// Update song details when a song is selected
function updateSongDetails(index = null) {
    const songSelector = document.getElementById('songSelector');
    const audioPlayer = document.getElementById('audioPlayer');
    const audioSource = document.getElementById('audioSource');
    const currentSongInfo = document.getElementById('currentSongInfo');
    
    // Use provided index or current selector index
    currentSongIndex = index !== null ? index : songSelector.selectedIndex;
    
    if (songs.length === 0) {
        currentSongInfo.textContent = 'No songs available';
        return;
    }

    const selectedSong = songs[currentSongIndex];
    const formattedSongName = formatSongName(selectedSong);
    
    // Remember if the song was playing
    const wasPlaying = !audioPlayer.paused;
    
    // Explicitly set the source and load
    audioSource.src = `/library/${selectedSong}`;
    audioPlayer.load();
    
    // Update song info
    currentSongInfo.textContent = `Selected: ${formattedSongName}`;
    
    // Update selector
    songSelector.selectedIndex = currentSongIndex;
    
    // Resume playing if it was playing before
    if (wasPlaying) {
        audioPlayer.play();
    }
}

// Play the selected song
function playSelectedSong() {
    const audioPlayer = document.getElementById('audioPlayer');
    const songSelector = document.getElementById('songSelector');
    
    // If no song is selected, play the first song
    if (songs.length > 0 && !audioPlayer.src) {
        songSelector.selectedIndex = 0;
        updateSongDetails(0);
    }
    
    audioPlayer.play();
}

// Move to the previous song
function previousSong() {
    const songSelector = document.getElementById('songSelector');
    const audioPlayer = document.getElementById('audioPlayer');
    
    // Decrement or wrap around to the last song
    currentSongIndex = (currentSongIndex - 1 + songs.length) % songs.length;
    
    songSelector.selectedIndex = currentSongIndex;
    updateSongDetails(currentSongIndex);
    audioPlayer.play();
}

// Move to the next song
function nextSong() {
    const songSelector = document.getElementById('songSelector');
    const audioPlayer = document.getElementById('audioPlayer');
    
    if (isShuffleMode) {
        // In shuffle mode, pick a random song
        currentSongIndex = Math.floor(Math.random() * songs.length);
    } else {
        // Normal sequential mode, wrap around using modulo
        currentSongIndex = (currentSongIndex + 1) % songs.length;
    }
    
    songSelector.selectedIndex = currentSongIndex;
    updateSongDetails(currentSongIndex);
    audioPlayer.play();
}

// Toggle shuffle mode
function toggleShuffle() {
    const shuffleButton = document.getElementById('shuffleButton');
    
    isShuffleMode = !isShuffleMode;
    shuffleButton.classList.toggle('active');
    shuffleButton.querySelector('i').classList.toggle('fa-random');
    
    if (isShuffleMode) {
        shuffleButton.querySelector('i').classList.toggle('fa-random');
        displayErrorMessage('Shuffle mode activated: Songs will play in random order');
    } else {
        shuffleButton.querySelector('i').classList.toggle('fa-sync');
        displayErrorMessage('Shuffle mode deactivated: Songs will play sequentially');
    }
}

// Filter songs based on search input
function filterSongs() {
    const searchInput = document.getElementById('songSearch');
    const songSelector = document.getElementById('songSelector');
    const filter = searchInput.value.toLowerCase();
    let visibleSongsCount = 0;
    
    for (let i = 0; i < songSelector.options.length; i++) {
        const option = songSelector.options[i];
        const text = option.textContent.toLowerCase();
        
        if (text.includes(filter)) {
            option.style.display = '';
            visibleSongsCount++;
        } else {
            option.style.display = 'none';
        }
    }

    // Provide feedback if no songs match
    const songMetadata = document.getElementById('songMetadata');
    if (visibleSongsCount === 0) {
        songMetadata.innerHTML = `<p class="info">No songs found matching "${searchInput.value}"</p>`;
    } else {
        songMetadata.innerHTML = `<p class="info">${visibleSongsCount} song(s) found</p>`;
    }
}