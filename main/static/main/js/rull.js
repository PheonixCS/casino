$(document).ready(function(){
    var parNames = document.querySelectorAll('.section-text-parName');
    var rullDiscriptions = document.querySelectorAll('.rullDiscription');
    parNames.forEach(function(parName, index) {
        parName.addEventListener('click', function() {
          // Проверяем, открыт ли уже соответствующий блок rullDiscription
          if (rullDiscriptions[index].style.maxHeight) {
            // Если блок уже открыт, то скрываем его
            rullDiscriptions[index].style.maxHeight = null;
          } else {
            // Если блок еще не открыт, то плавно выдвигаем его
            rullDiscriptions[index].style.maxHeight = rullDiscriptions[index].scrollHeight + 'px';
          }
        });
    });


    var parNameBlocks = document.querySelectorAll('.section-text.section-text-parName');
    // Перебираем полученные элементы
    parNameBlocks.forEach(function(block) {
        var blureBlock = block.querySelector('.section-text-blure');
        
        block.addEventListener('click', function() {
            if (blureBlock.style.display === 'none' || blureBlock.style.display === '') {
                blureBlock.style.display = 'block';
            } else {
                blureBlock.style.display = 'none';
            }
        });
    });
});