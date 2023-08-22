function refresh() {
    fetch('/extract', {
        method: 'POST'
    }).then((_res) => {
        window.location.href = "/extract";
    });
}

function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href = "/";
    })
}