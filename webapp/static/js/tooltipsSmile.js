document.addEventListener("DOMContentLoaded", () => {
    // Включаем подсказки
	var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
    })
	
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })


    document.getElementById('button-smile').onclick = addsmiles;

    function addsmiles()
    {
        var knop = document.getElementById('newMessage');
        let smileList = document.getElementsByClassName('smile');
        if (smileList != null) {
            for (let i = 0; i <= smileList.length - 1; i++) {
                smileList[i].onclick = () => {
                    knop.value += smileList[i].innerHTML;
                    knop.focus();
                }
            }
        }
        document.getElementById('button-smile').onclick = null;
    }
});
