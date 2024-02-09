document.addEventListener("alpine:init", () => {
	Alpine.data("scrollToTop", () => ({
		showTopButton: false,
		init() {
			window.onscroll = () => {
				this.scrollFunction();
			};
		},

		scrollFunction() {
			if (
				document.body.scrollTop > 50 ||
				document.documentElement.scrollTop > 50
			) {
				this.showTopButton = true;
			} else {
				this.showTopButton = false;
			}
		},

		goToTop() {
			document.body.scrollTop = 0;
			document.documentElement.scrollTop = 0;
		},
	}));
});
