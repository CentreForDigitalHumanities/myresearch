import objectSupport from "dayjs/plugin/objectSupport";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
import localizedFormat from "dayjs/plugin/localizedFormat";
import "dayjs/locale/nl";
import "dayjs/locale/en-gb";
import dayjs, { extend, locale } from "dayjs";

// This plugin has (mostly) been copied from DIAPP!
// See: https://github.com/CentreForDigitalHumanities/DIAPP

export default defineNuxtPlugin(() => {
    extend(objectSupport);
    extend(isSameOrBefore);
    extend(localizedFormat);
    locale("en-gb");
    return {
        provide: {
            dayjs,
        },
    };
});
