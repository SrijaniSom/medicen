var Longbtn= document.querySelector('.longbtn');
var Shortbtn=document.querySelector('.shbtn');
var Longtable=document.querySelector('.long');
var Shorttable=document.querySelector('.short');
var Heading=document.querySelector('.pathead');
Longbtn.addEventListener("click",()=>{
    Shorttable.style.display="none";
    Longtable.style.display="block";
    Heading.textContent="Long-term";});
Shortbtn.addEventListener("click",()=>{
    Shorttable.style.display="block";
    Longtable.style.display="none";
    Heading.textContent="Short-term";
});