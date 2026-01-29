import * as dayjs from "dayjs";
import { useNuxtApp } from "#app";

export default function useDayJS(value?: dayjs.ConfigType) {
    const nuxtApp = useNuxtApp();
    return nuxtApp.$dayjs(value);
}
