// Set a timeout and store the timeout ID
let timeoutId = setTimeout(() => {
    console.log('This will not run if clearTimeout is called before 3 seconds.');
}, 3000);

// Cancel the timeout
clearTimeout(timeoutId);

export const pollApi = (apiFunction, duration) => {
    let intervalId = setInterval(() => {
        console.log('This will not run if clearTimeout is called before 3 seconds.');
    }, 3000);
}