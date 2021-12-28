let i = setInterval(function() {
    if (document.querySelector("a.list-group-item.list-group-item-action.active.py-3.lh-tight")) {
        let title = document.querySelector("a.list-group-item.list-group-item-action.active.py-3.lh-tight").children[0].children[0].innerHTML
        let maintitle = document.getElementById('messenger-header')
        maintitle.innerHTML = '<b>' + title + '</b>'
        clearInterval(i)

    }
}, 1000);