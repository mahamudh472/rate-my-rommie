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