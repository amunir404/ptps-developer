import PerfectScrollbar from "perfect-scrollbar";
import Alpine from "alpinejs";
import collapse from "@alpinejs/collapse";
import persist from "@alpinejs/persist";
import focus from "@alpinejs/focus";
import "./custom/collapse.js";
import "./custom/scroll-top.js";
import "./custom/screen-loader.js";
import "./custom/nav-bottom.js";
import "./custom/current-year.js";

window.Alpine = Alpine;
Alpine.plugin(persist);
Alpine.plugin(focus);
Alpine.plugin(collapse);
Alpine.start();

// perfect scrollbar
const initPerfectScrollbar = () => {
	const container = document.querySelectorAll(".perfect-scrollbar");
	for (let i = 0; i < container.length; i++) {
		new PerfectScrollbar(container[i], {
			wheelPropagation: true,
			// suppressScrollX: true,
		});
	}
};
initPerfectScrollbar();
const $ = require("jquery");
