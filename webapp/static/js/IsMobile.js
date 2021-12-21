/* Скрипт, позволяющий переиспользовать окно вывода
    в десктопной и мобильной версии */

let isMobile = window.innerWidth <= 760;

function moveNewPlace(newPlaceName)
{
    let floatObject = document.getElementById('floatObject');
    floatObject.parentNode.removeChild(floatObject);
    let newPlace = document.getElementById(newPlaceName);
    newPlace.appendChild(floatObject);
}

function swapMobile()
{
    /* Если версия мобильная и было расширено */
    if(isMobile && window.innerWidth > 760)
    {
        /* Переключаем на десктоп версию */
        isMobile = false;
        moveNewPlace('outputPlace1');
        document.getElementById('closeBtn').click();
    }
    else if(!isMobile && window.innerWidth <= 760)
    {
        /* Иначе - переключаем на мобильную версию */
        isMobile = true;
        moveNewPlace('outputPlace2');
    }
}

function isMobileLoad()
{
    moveNewPlace('outputPlace2');
}

/* Вешаем обработчики */

window.onresize = swapMobile;

if(isMobile)
    document.body.onload = isMobileLoad;
