const tg = window.Telegram.WebApp;
const user = tg.initDataUnsafe?.user;
const userDataDiv = document.getElementById('user-data');

let count = 0;

function increment() {
    count++;
    updateCounter();
}

function updateCounter() {
    document.getElementById('counter').textContent = count;
}

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
        const userAgent = navigator.userAgent.toLowerCase();
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