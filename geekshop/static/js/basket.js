function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

inpEl = document.querySelectorAll('input[type="number"]');
window.addEventListener('DOMContentLoaded', () => {
    for (const i of inpEl) {
        i.addEventListener('click', event => {
            const clicked_input = event.target;
            fetch('/basket/edit/' + clicked_input.name + '/' + clicked_input.value + '/', {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                body: ''
            }).then(response => { return response.text() });
            event.preventDefault();
        });
    }
});

