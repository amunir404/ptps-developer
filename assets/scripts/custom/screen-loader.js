window.addEventListener("load", function () {
	// screen loader
	const screen_loader = document.getElementsByClassName("screen_loader");
	if (screen_loader?.length) {
		screen_loader[0].classList.add("animate__fadeOut");
		setTimeout(() => {
			document.body.removeChild(screen_loader[0]);
		}, 200);
	}

	// set rtl layout
	Alpine.store("app").setRTLLayout();
});
