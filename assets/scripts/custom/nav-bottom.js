document.addEventListener("alpine:init", () => {
	Alpine.data("bottomNav", () => ({
		init() {
			const selector = document.querySelector(
				'.bottomNav ul a[href="' + window.location.pathname + '"]',
			);
			if (selector) {
				selector.classList.add("text-primary");
				const ul = selector.closest("ul.sub-menu");
				if (ul) {
					let ele = ul.closest("li.menu").querySelectorAll(".nav-link");
					if (ele) {
						ele = ele[0];
						setTimeout(() => {
							ele.click();
						});
					}
				}
			}
		},
	}));
});
