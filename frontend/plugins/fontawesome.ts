import { library } from "@fortawesome/fontawesome-svg-core";
// eslint-disable-next-line import/named
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import {
    faUser,
    faUserShield,
    faUserSecret,
    faCalendar,
    faGear,
    faGrip,
    faPlus,
    faMinus,
    faAngleDown,
    faUserSlash,
    faUserPlus,
    faTrash,
    faPen,
    faHouse,
    faArrowsSplitUpAndLeft,
    faAward,
    faPersonChalkboard,
    faTriangleExclamation,
    faMagnifyingGlass,
    faCircleQuestion,
    faCircleInfo,
    faBan,
    faCheck,
    faListCheck,
    faReceipt,
    faCat,
    faShieldCat,
    faCircleCheck,
    faCirclePlay,
    faCircleXmark,
    faGraduationCap,
    faArrowRight,
    faSkull,
    faCrown,
} from "@fortawesome/free-solid-svg-icons";

library.add(
    faUser,
    faUserShield,
    faUserSecret,
    faCalendar,
    faGear,
    faGrip,
    faPlus,
    faMinus,
    faAngleDown,
    faTrash,
    faUserSlash,
    faUserPlus,
    faPen,
    faHouse,
    faArrowsSplitUpAndLeft,
    faAward,
    faPersonChalkboard,
    faTriangleExclamation,
    faMagnifyingGlass,
    faCircleQuestion,
    faCircleInfo,
    faBan,
    faCheck,
    faListCheck,
    faReceipt,
    faCat,
    faShieldCat,
    faCircleCheck,
    faCirclePlay,
    faCircleXmark,
    faGraduationCap,
    faArrowRight,
    faSkull,
    faCrown
);

export default defineNuxtPlugin((nuxtApp) => {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore Somehow it doesn't get that a Component is a Component
    nuxtApp.vueApp.component("FontAwesomeIcon", FontAwesomeIcon);
});
