
	 let infdiv = document.getElementById("infbar");
         function infbar(inftext){
         if(infdiv.style.display === 'none'){
         let timer = setTimeout( () => infdiv.style.display = 'none', 2000);
         infdiv.style.display = 'block';
         infdiv.innerHTML = inftext;
         }
         
         else{
         infdiv.innerHTML = inftext;
         }
         
         }
