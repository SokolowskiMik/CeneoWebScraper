function refresh() {
    fetch('/extract', {
        method: 'POST'
    }).then((_res) => {
        window.location.href = "/extract";
    });
}