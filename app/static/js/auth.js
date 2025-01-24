function onSignIn(googleUser) {
    const id_token = googleUser.getAuthResponse().id_token;
    fetch('/api/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: id_token })
    }).then(response => response.json())
      .then(data => console.log(data));
}