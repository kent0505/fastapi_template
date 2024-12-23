const tg = window.Telegram.WebApp;
const user = tg.initDataUnsafe?.user;
const userDataDiv = document.getElementById('user-data');

let count = 0;

const image = document.querySelector('.click-image');
image.addEventListener('touchstart', () => {
    image.style.transform = 'scale(0.9)';
});
image.addEventListener('touchend', () => {
    image.style.transform = 'scale(1)';
});
image.addEventListener('touchmove', (e) => {
    e.preventDefault();
});
document.addEventListener('selectstart', (e) => {
    e.preventDefault();
});

function increment(amount) {
    count += amount;
    updateCounter();
}

function updateCounter() {
    document.getElementById('counter').textContent = count.toLocaleString();;
}

const imageElement = document.getElementById('click-image');

imageElement.addEventListener('touchstart', (event) => {
    const touchCount = event.touches.length; // Number of fingers touching
    increment(touchCount); // Increment by the number of touches
});

function isMobileDevice() {
    const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    const isSmallScreen = window.innerWidth <= 768;
    return isTouchDevice && isSmallScreen;
}

// async function saveUser(data) {
//     try {
//         const response = await fetch('/api/post-endpoint', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(data),
//         });
//         if (!response.ok) {
//             throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const result = await response.json();
//     } catch (error) {}
// }

// saveUser({
//     userId: user.id,
//     username: user.username || '',
//     name: `${user.first_name} ${user.last_name || ''}`,
// });

if (user) {
    function displayContent() {
        if (isMobileDevice()) {
            userDataDiv.innerHTML = `
            <p style="color: white;"><strong>User ID:</strong> ${user.id}</p>
            <p style="color: white;"><strong>Username:</strong> ${user.username || "N/A"}</p>
            <p style="color: white;"><strong>Name:</strong> ${user.first_name} ${user.last_name || ""}</p>
            `;
        } else {
            userDataDiv.innerHTML = '<p style="color: red;">Error: This page must be opened on a mobile device.</p>';
        }
    }
    displayContent();
}
