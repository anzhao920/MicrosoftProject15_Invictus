const pwaAuth = document.querySelector("pwa-auth");
pwaAuth.addEventListener("signin-completed", ev => {
    const signIn = ev.detail;
    if (signIn.error) {
        console.error("Sign in failed", signIn.error);
    } else {
        window.location.replace(window.location.href + '/loggedIn.html');
        console.log("Email: ", signIn.email);
        console.log("Name: ", signIn.name);
        console.log(window.location.href);
    }
});