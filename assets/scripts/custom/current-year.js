// set current year in footer
const yearEle = document.querySelector("#footer-year");
if (yearEle) {
	yearEle.innerHTML = new Date().getFullYear();
}
