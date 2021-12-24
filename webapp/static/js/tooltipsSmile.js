window.onload = function() {
    // Включаем подсказки
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })

    document.getElementById('button-smile').onclick = addsmiles;

    function addsmiles() {
        knop = document.getElementById('newMessage')
        if (document.getElementsByClassName('smile') != null) {
            for (let i = 0; i <= document.getElementsByClassName('smile').length - 1; i++) {
                document.getElementsByClassName('smile')[i].onclick = function() {
                    knop.value += this.innerHTML
                }
            }
        }
    }
}
