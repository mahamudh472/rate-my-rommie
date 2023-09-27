const navbtn = document.getElementById('nav-btn');
const navinput = document.getElementById('nav-input');
const headtext = document.getElementById('head-text');
const headtext2 = document.getElementById('head-text2');
const headerinput = document.getElementById('header-input');

const cngNavElemets = (e) => {
    navbtn.innerText = e
    navinput.placeholder = `enter ${e}`
    navinput.name = e
}
const cngHeadText = () => {
    if (headtext.innerText == 'Welcome to Roommate Finder') {
        headtext.innerText = 'Welcome to Address Finder'
        headtext2.innerText = 'Find your perfect Roommate today!'
        headerinput.placeholder = 'Enter address name'
        headerinput.name = 'Address'
    }
    else {
        headtext.innerText = 'Welcome to Roommate Finder'
        headtext2.innerText = 'Find your perfect Address today!'
        headerinput.placeholder = 'Enter Roommate name'
        headerinput.name = 'Roommate'
    }

}

function add_attribute(){
    var element = document.getElementById("attr").value;
    var rate = document.getElementsByName("stars");
    var rating;
    for (let index = 0; index < rate.length; index++) {
        if (rate[index].checked == true) {
            rating = rate[index].value;
        }
        
    }
    var data, old_data;
    // get data from the element and store in localstorage
    if(localStorage.getItem('attr')==null){
        localStorage.setItem('attr','[]');
        data = [element, rating];
        old_data = JSON.parse(localStorage.getItem('attr'));
        old_data.push(data);
        localStorage.setItem('attr',JSON.stringify(old_data));

    }else{
        old_data = JSON.parse(localStorage.getItem('attr'));
        data = [element, rating];
        old_data.push(data);
        localStorage.setItem('attr',JSON.stringify(old_data));
    }
    var attrList = document.getElementById('attrList');
    attrList.value = localStorage.getItem('attr');
    display_data();
}
function display_data(){
    var data = JSON.parse(localStorage.getItem('attr'));
    var list = document.getElementById('list');
    list.innerHTML = '';
    for (let index = 0; index < data.length; index++) {
        list.innerHTML += `<li><b>${data[index][0]}</b> ${data[index][1]}</li>`
        
    }
    document.getElementById("attr").value="";
    document.getElementsByName("stars")[0].checked = true;
}
window.onload = function(){
    localStorage.clear();
}